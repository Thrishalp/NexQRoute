import os
import sys
import copy
import json
import random

import numpy as np
import pandas as pd
import streamlit as st
import folium
import networkx as nx
import osmnx as ox

from streamlit_folium import st_folium


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# PROJECT IMPORTS
# ============================================================

from optimization.qpso import (
    get_customer_data,
    get_vehicle_data,
    qpso_optimize,
    calculate_solution_details
)

from simulation.traffic import add_traffic_weights

from graph.routing import (
    get_locations,
    calculate_matrices
)


# ============================================================
# FILE PATHS
# ============================================================

GRAPH_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "gachibowli_roads.graphml"
)

CUSTOMERS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "customers.csv"
)

DEPOT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "depot.csv"
)

VEHICLES_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "vehicles.csv"
)

OPTIMIZED_JSON = os.path.join(
    PROJECT_ROOT,
    "results",
    "optimized_route_geometry.json"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="QPSO Intelligent Route Optimizer",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        opacity: 0.75;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 650;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🚚 QPSO Intelligent Route Optimizer'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Quantum-Inspired Traffic-Aware Vehicle Routing System'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD CSV DATA
# ============================================================

@st.cache_data
def load_csv_data():

    customers = pd.read_csv(
        CUSTOMERS_FILE
    )

    depot = pd.read_csv(
        DEPOT_FILE
    )

    vehicles = pd.read_csv(
        VEHICLES_FILE
    )

    return customers, depot, vehicles


# ============================================================
# LOAD GRAPH
# ============================================================

@st.cache_resource
def load_base_graph():

    return ox.load_graphml(
        GRAPH_FILE
    )


customers, depot, vehicles = load_csv_data()

base_graph = load_base_graph()


# ============================================================
# SESSION STATE
# ============================================================

if "graph" not in st.session_state:

    graph = copy.deepcopy(
        base_graph
    )

    random.seed(42)
    np.random.seed(42)

    graph = add_traffic_weights(
        graph
    )

    st.session_state.graph = graph


if "optimized_routes" not in st.session_state:
    st.session_state.optimized_routes = None


if "optimized_details" not in st.session_state:
    st.session_state.optimized_details = None


if "before_routes" not in st.session_state:
    st.session_state.before_routes = None


if "before_details" not in st.session_state:
    st.session_state.before_details = None


if "incident_edges" not in st.session_state:
    st.session_state.incident_edges = []


if "incident_active" not in st.session_state:
    st.session_state.incident_active = False


# ============================================================
# LOCATION → NODE MAP
# ============================================================

def build_location_node_map():

    location_nodes = {}

    location_nodes["Depot"] = int(
        depot.iloc[0]["node"]
    )

    for _, row in customers.iterrows():

        customer_id = str(
            row["id"]
        )

        location_nodes[customer_id] = int(
            row["node"]
        )

    return location_nodes


# ============================================================
# MATRIX CONVERSION
# ============================================================

def convert_matrix_to_dataframe(
    matrix,
    locations
):

    # get_locations() returns dictionaries such as:
    # {"id": "C1", "node": 123456789}
    #
    # QPSO needs matrix labels:
    # Depot, C1, C2, C3, ...

    labels = [
        str(location["id"])
        for location in locations
    ]

    df = pd.DataFrame(
        matrix,
        index=labels,
        columns=labels
    )

    return df

# ============================================================
# LOAD SUCCESSFUL EXISTING QPSO RESULT
# ============================================================

def load_saved_qpso_result():

    if not os.path.exists(
        OPTIMIZED_JSON
    ):
        return None

    try:

        with open(
            OPTIMIZED_JSON,
            "r"
        ) as file:

            data = json.load(file)

        routes = {}

        vehicle_data = data.get(
            "routes",
            {}
        )

        for vehicle_id, info in vehicle_data.items():

            route = info.get(
                "route",
                []
            )

            routes[str(vehicle_id)] = route

        if not routes:
            return None

        # Build details in the format used by dashboard
        vehicle_details = []

        total_distance = 0.0
        total_time = 0.0

        for vehicle_id, info in vehicle_data.items():

            distance_km = float(
                info.get(
                    "distance_km",
                    0
                )
            )

            time_min = float(
                info.get(
                    "travel_time_min",
                    0
                )
            )

            demand = float(
                info.get(
                    "demand",
                    0
                )
            )

            capacity = float(
                info.get(
                    "capacity",
                    0
                )
            )

            total_distance += distance_km

            total_time += time_min

            vehicle_details.append(
                {
                    "vehicle": str(vehicle_id),
                    "distance": distance_km,
                    "time": time_min,
                    "demand": demand,
                    "capacity": capacity
                }
            )

        details = {
            "feasible": True,
            "total_distance": total_distance,
            "total_time": total_time,
            "vehicles": vehicle_details
        }

        return routes, details

    except Exception as error:

        print(
            "Could not load saved QPSO result:",
            error
        )

        return None


# ============================================================
# RUN QPSO
# ============================================================

def run_qpso(graph):

    locations = get_locations(
        customers,
        depot
    )

    distance_matrix, time_matrix = calculate_matrices(
        graph,
        locations
    )

    distance_df = convert_matrix_to_dataframe(
        distance_matrix,
        locations
    )

    time_df = convert_matrix_to_dataframe(
        time_matrix,
        locations
    )

    customer_ids, demands = get_customer_data(
        customers
    )

    vehicle_ids, capacities = get_vehicle_data(
        vehicles
    )

    # --------------------------------------------------------
    # Try several stochastic QPSO runs
    # --------------------------------------------------------

    for attempt in range(1, 11):

        try:

            seed = 1000 + attempt

            np.random.seed(seed)
            random.seed(seed)

            result = qpso_optimize(
                customer_ids,
                demands,
                vehicle_ids,
                capacities,
                time_df,
                distance_df
            )

            if result is None:
                continue

            best_position, best_routes = result

            if best_routes is None:
                continue

            details = calculate_solution_details(
                best_routes,
                time_df,
                distance_df,
                demands,
                capacities
            )

            if details is None:
                continue

            # Keep distance consistently in kilometres.
            details["total_distance"] = float(
                details["total_distance"]
            )

            for vehicle in details["vehicles"]:
                vehicle["distance"] = float(
                    vehicle["distance"]
                )

            # QPSO returned a valid route.
            details["feasible"] = True

            if details.get(
                "feasible",
                False
            ):

                return (
                    best_routes,
                    details
                )

        except Exception as error:

            print(
                f"QPSO attempt {attempt} failed:",
                error
            )

    return None


# ============================================================
# CREATE TRAFFIC INCIDENT
# ============================================================

def create_traffic_incident(
    graph,
    routes,
    location_nodes,
    number_of_roads=20
):

    affected_edges = set()

    # --------------------------------------------------------
    # Select roads used by current routes
    # --------------------------------------------------------

    for vehicle_id, route in routes.items():

        if len(route) < 2:
            continue

        for i in range(
            len(route) - 1
        ):

            start_location = route[i]
            end_location = route[i + 1]

            if start_location not in location_nodes:
                continue

            if end_location not in location_nodes:
                continue

            start_node = location_nodes[
                start_location
            ]

            end_node = location_nodes[
                end_location
            ]

            try:

                path = nx.shortest_path(
                    graph,
                    start_node,
                    end_node,
                    weight="traffic_time"
                )

            except Exception:

                try:

                    path = nx.shortest_path(
                        graph,
                        start_node,
                        end_node,
                        weight="length"
                    )

                except Exception:

                    continue

            for j in range(
                len(path) - 1
            ):

                u = path[j]
                v = path[j + 1]

                if graph.has_edge(
                    u,
                    v
                ):

                    keys = list(
                        graph[u][v].keys()
                    )

                    if keys:

                        affected_edges.add(
                            (
                                u,
                                v,
                                keys[0]
                            )
                        )

                if len(
                    affected_edges
                ) >= number_of_roads:

                    break

            if len(
                affected_edges
            ) >= number_of_roads:

                break

        if len(
            affected_edges
        ) >= number_of_roads:

            break

    # --------------------------------------------------------
    # Fallback roads
    # --------------------------------------------------------

    if len(
        affected_edges
    ) < number_of_roads:

        all_edges = list(
            graph.edges(
                keys=True
            )
        )

        random.shuffle(
            all_edges
        )

        for edge in all_edges:

            affected_edges.add(
                edge
            )

            if len(
                affected_edges
            ) >= number_of_roads:

                break

    # --------------------------------------------------------
    # Apply severe traffic
    # --------------------------------------------------------

    for u, v, key in affected_edges:

        data = graph[u][v][key]

        if "base_time" not in data:

            length = float(
                data.get(
                    "length",
                    0
                )
            )

            data["base_time"] = (
                (length / 1000)
                / 30
                * 60
            )

        base_time = float(
            data["base_time"]
        )

        data["traffic_level"] = "severe"
        data["traffic_factor"] = 3.0
        data["traffic_time"] = (
            base_time * 3.0
        )

    return list(
        affected_edges
    )


# ============================================================
# ROUTE GEOMETRY
# ============================================================

def generate_route_geometry(
    graph,
    routes,
    location_nodes
):

    all_geometry = {}

    for vehicle_id, route in routes.items():

        geometry = []

        if len(route) < 2:

            all_geometry[
                vehicle_id
            ] = geometry

            continue

        for i in range(
            len(route) - 1
        ):

            start_location = route[i]
            end_location = route[i + 1]

            if start_location not in location_nodes:
                continue

            if end_location not in location_nodes:
                continue

            start_node = location_nodes[
                start_location
            ]

            end_node = location_nodes[
                end_location
            ]

            try:

                path = nx.shortest_path(
                    graph,
                    start_node,
                    end_node,
                    weight="traffic_time"
                )

            except Exception:

                try:

                    path = nx.shortest_path(
                        graph,
                        start_node,
                        end_node,
                        weight="length"
                    )

                except Exception:

                    continue

            for node in path:

                if node not in graph.nodes:
                    continue

                node_data = graph.nodes[
                    node
                ]

                if (
                    "x" not in node_data
                    or
                    "y" not in node_data
                ):

                    continue

                coordinate = [
                    float(node_data["y"]),
                    float(node_data["x"])
                ]

                if (
                    not geometry
                    or
                    geometry[-1] != coordinate
                ):

                    geometry.append(
                        coordinate
                    )

        all_geometry[
            vehicle_id
        ] = geometry

    return all_geometry


# ============================================================
# DRAW INCIDENT ROADS
# ============================================================

def draw_incident_roads(
    map_object,
    graph,
    incident_edges
):

    for u, v, key in incident_edges:

        if (
            u not in graph.nodes
            or
            v not in graph.nodes
        ):
            continue

        u_data = graph.nodes[u]
        v_data = graph.nodes[v]

        if (
            "x" not in u_data
            or
            "y" not in u_data
            or
            "x" not in v_data
            or
            "y" not in v_data
        ):
            continue

        coordinates = [
            [
                float(u_data["y"]),
                float(u_data["x"])
            ],
            [
                float(v_data["y"]),
                float(v_data["x"])
            ]
        ]

        folium.PolyLine(
            locations=coordinates,
            weight=7,
            opacity=0.95,
            tooltip="🚨 Severe Traffic"
        ).add_to(
            map_object
        )


# ============================================================
# INITIAL SOLUTION
# ============================================================

if st.session_state.optimized_routes is None:

    # --------------------------------------------------------
    # First use the successful result from
    # optimized_route_geometry.py
    # --------------------------------------------------------

    saved_result = load_saved_qpso_result()

    if saved_result is not None:

        routes, details = saved_result

        st.session_state.optimized_routes = routes
        st.session_state.optimized_details = details

    else:

        # ----------------------------------------------------
        # If JSON does not exist, run QPSO
        # ----------------------------------------------------

        with st.spinner(
            "⚛️ Running QPSO optimization..."
        ):

            result = run_qpso(
                st.session_state.graph
            )

        if result is None:

            st.error(
                "QPSO could not find a feasible solution. "
                "Please run optimized_route_geometry.py first."
            )

            st.code(
                "python graph/optimized_route_geometry.py"
            )

            st.stop()

        routes, details = result

        st.session_state.optimized_routes = routes
        st.session_state.optimized_details = details


# ============================================================
# CURRENT DATA
# ============================================================

routes = st.session_state.optimized_routes
details = st.session_state.optimized_details


total_distance = float(
    details["total_distance"]
)

total_time = float(
    details["total_time"]
)


# ============================================================
# TOP METRICS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "📍 Customers",
        len(customers)
    )

with c2:

    st.metric(
        "🚚 Vehicles",
        len(vehicles)
    )

with c3:

    st.metric(
        "📏 Total Distance",
        f"{total_distance:.3f} km"
    )

with c4:

    st.metric(
        "⏱️ Travel Time",
        f"{total_time:.3f} min"
    )


# ============================================================
# CONTROL BUTTONS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🚦 Dynamic Traffic Control'
    '</div>',
    unsafe_allow_html=True
)

b1, b2, b3 = st.columns(3)

with b1:

    incident_button = st.button(
        "🚦 Simulate Traffic Incident",
        use_container_width=True
    )

with b2:

    reoptimize_button = st.button(
        "⚛️ Re-optimize with QPSO",
        use_container_width=True
    )

with b3:

    reset_button = st.button(
        "🔄 Reset Scenario",
        use_container_width=True
    )


# ============================================================
# RESET
# ============================================================

if reset_button:

    graph = copy.deepcopy(
        base_graph
    )

    random.seed(42)
    np.random.seed(42)

    graph = add_traffic_weights(
        graph
    )

    st.session_state.graph = graph

    # Reload the successful original solution
    saved_result = load_saved_qpso_result()

    if saved_result is not None:

        routes, details = saved_result

        st.session_state.optimized_routes = routes
        st.session_state.optimized_details = details

    else:

        st.session_state.optimized_routes = None
        st.session_state.optimized_details = None

    st.session_state.before_routes = None
    st.session_state.before_details = None

    st.session_state.incident_edges = []
    st.session_state.incident_active = False

    st.rerun()


# ============================================================
# TRAFFIC INCIDENT
# ============================================================

if incident_button:

    st.session_state.before_routes = copy.deepcopy(
        st.session_state.optimized_routes
    )

    st.session_state.before_details = copy.deepcopy(
        st.session_state.optimized_details
    )

    location_nodes = build_location_node_map()

    affected_edges = create_traffic_incident(
        st.session_state.graph,
        st.session_state.optimized_routes,
        location_nodes,
        number_of_roads=20
    )

    st.session_state.incident_edges = affected_edges
    st.session_state.incident_active = True

    st.success(
        f"🚨 Traffic incident simulated on "
        f"{len(affected_edges)} road segments."
    )


# ============================================================
# RE-OPTIMIZATION
# ============================================================

if reoptimize_button:

    if not st.session_state.incident_active:

        st.warning(
            "Please simulate a traffic incident first."
        )

    else:

        with st.spinner(
            "⚛️ QPSO is recalculating the optimal routes..."
        ):

            result = run_qpso(
                st.session_state.graph
            )

        if result is None:

            st.error(
                "This QPSO run did not find a feasible "
                "solution. The previous route is being kept. "
                "Click Re-optimize again to try another "
                "stochastic QPSO run."
            )

        else:

            new_routes, new_details = result

            st.session_state.optimized_routes = new_routes
            st.session_state.optimized_details = new_details

            st.success(
                "✅ Traffic-aware routes successfully "
                "re-optimized by QPSO."
            )


# ============================================================
# STATUS
# ============================================================

if st.session_state.incident_active:

    st.warning(
        "🚨 Traffic incident active — "
        "affected roads have severe traffic."
    )

else:

    st.success(
        "🟢 Normal traffic scenario."
    )


# ============================================================
# MAP + LIVE ROUTE SUMMARY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🗺️ Live Route Optimization'
    '</div>',
    unsafe_allow_html=True
)

map_left, map_right = st.columns(
    [0.38, 0.62],
    gap="medium"
)

# ============================================================
# LEFT: LIVE STATUS + ROUTE SUMMARY
# ============================================================

with map_left:

    if st.session_state.incident_active:

        st.error(
            "🚨 Incident Active\n\n"
            "Affected roads have severe traffic."
        )

    else:

        st.success(
            "🟢 Normal Traffic\n\n"
            "No simulated incident is active."
        )

    st.markdown("### 🚚 Active Fleet")

    active_vehicle_count = sum(
        1
        for route in routes.values()
        if len(route) > 2
    )

    st.metric(
        "Vehicles in service",
        active_vehicle_count
    )

    st.markdown("### 📍 Optimized Routes")

    for vehicle_id, route in routes.items():

        vehicle_details = None

        for item in details["vehicles"]:

            if str(item["vehicle"]) == str(vehicle_id):
                vehicle_details = item
                break

        # Do not expand the sidebar summary too much.
        if vehicle_details is not None:

            distance_km = float(
                vehicle_details["distance"]
            )

            time_min = float(
                vehicle_details["time"]
            )

            demand = float(
                vehicle_details["demand"]
            )

            capacity = float(
                vehicle_details["capacity"]
            )

            st.markdown(
                f"**🚚 {vehicle_id}**"
            )

            st.caption(
                " → ".join(route)
            )

            r1, r2 = st.columns(2)

            with r1:
                st.caption(
                    f"📏 {distance_km:.2f} km"
                )

            with r2:
                st.caption(
                    f"⏱️ {time_min:.2f} min"
                )

            st.caption(
                f"📦 Load: {demand:.0f} / {capacity:.0f}"
            )

        else:

            st.markdown(
                f"**🚚 {vehicle_id}**"
            )

            st.caption(
                " → ".join(route)
            )

    st.markdown("### 📊 Current Scenario")

    sc1, sc2 = st.columns(2)

    with sc1:
        st.metric(
            "Distance",
            f"{total_distance:.2f} km"
        )

    with sc2:
        st.metric(
            "Travel Time",
            f"{total_time:.2f} min"
        )

    st.caption(
        "Routes are calculated on the Gachibowli road network "
        "using traffic-weighted travel time."
    )


# ============================================================
# RIGHT: INTERACTIVE MAP
# ============================================================

with map_right:

    depot_lat = float(
        depot.iloc[0]["latitude"]
    )

    depot_lon = float(
        depot.iloc[0]["longitude"]
    )

    m = folium.Map(
        location=[
            depot_lat,
            depot_lon
        ],
        zoom_start=13,
        control_scale=True
    )

    # --------------------------------------------------------
    # DEPOT
    # --------------------------------------------------------

    folium.Marker(
        location=[
            depot_lat,
            depot_lon
        ],
        popup="<b>🚩 Depot</b><br>Gachibowli",
        tooltip="🚩 Depot",
        icon=folium.Icon(
            icon="home",
            prefix="fa"
        )
    ).add_to(m)

    # --------------------------------------------------------
    # CUSTOMERS
    # --------------------------------------------------------

    for _, row in customers.iterrows():

        customer_id = str(
            row["id"]
        )

        latitude = float(
            row["latitude"]
        )

        longitude = float(
            row["longitude"]
        )

        demand = float(
            row["demand"]
        )

        folium.CircleMarker(
            location=[
                latitude,
                longitude
            ],
            radius=7,
            popup=(
                f"<b>📍 {customer_id}</b><br>"
                f"Demand: {demand:.0f}"
            ),
            tooltip=(
                f"{customer_id} • "
                f"Demand {demand:.0f}"
            ),
            fill=True,
            fill_opacity=0.9
        ).add_to(m)

    # --------------------------------------------------------
    # ROUTE GEOMETRY
    # --------------------------------------------------------

    location_nodes = build_location_node_map()

    geometry = generate_route_geometry(
        st.session_state.graph,
        routes,
        location_nodes
    )

    # --------------------------------------------------------
    # DRAW OPTIMIZED ROUTES
    # --------------------------------------------------------

    for vehicle_id, coordinates in geometry.items():

        if not coordinates:
            continue

        vehicle_details = None

        for item in details["vehicles"]:

            if str(item["vehicle"]) == str(vehicle_id):
                vehicle_details = item
                break

        if vehicle_details is not None:

            distance_km = float(
                vehicle_details["distance"]
            )

            time_min = float(
                vehicle_details["time"]
            )

            demand = float(
                vehicle_details["demand"]
            )

            capacity = float(
                vehicle_details["capacity"]
            )

            popup = (
                f"<b>🚚 {vehicle_id}</b><br>"
                f"Distance: {distance_km:.3f} km<br>"
                f"Travel time: {time_min:.3f} min<br>"
                f"Demand: {demand:.0f} / {capacity:.0f}"
            )

        else:

            popup = str(vehicle_id)

        folium.PolyLine(
            locations=coordinates,
            weight=6,
            opacity=0.9,
            popup=popup,
            tooltip=f"🚚 {vehicle_id} — Optimized Route"
        ).add_to(m)

    # --------------------------------------------------------
    # INCIDENT ROADS
    # --------------------------------------------------------

    if st.session_state.incident_active:

        draw_incident_roads(
            m,
            st.session_state.graph,
            st.session_state.incident_edges
        )

    # --------------------------------------------------------
    # MAP LEGEND
    # --------------------------------------------------------

    legend_html = """
    <div style="
        position: fixed;
        bottom: 25px;
        left: 25px;
        z-index: 9999;
        background: rgba(255,255,255,0.94);
        padding: 10px 12px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        font-size: 13px;
        line-height: 1.6;
    ">
        <b>Map Legend</b><br>
        🚩 Depot<br>
        📍 Customer<br>
        🔵 Optimized Route<br>
        🚨 Severe Traffic
    </div>
    """

    m.get_root().html.add_child(
        folium.Element(legend_html)
    )

    st_folium(
        m,
        width=None,
        height=570,
        returned_objects=[]
    )


# ============================================================
# ROUTE DETAILS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🚚 Current Optimized Routes'
    '</div>',
    unsafe_allow_html=True
)

for vehicle_id, route in routes.items():

    vehicle_details = None

    for item in details["vehicles"]:

        if str(
            item["vehicle"]
        ) == str(vehicle_id):

            vehicle_details = item
            break

    with st.expander(
        f"🚚 {vehicle_id}",
        expanded=True
    ):

        st.write(
            " → ".join(route)
        )

        if vehicle_details is not None:

            c1, c2, c3 = st.columns(3)

            with c1:

                st.metric(
                    "Distance",
                    f"{float(vehicle_details['distance']):.3f} km"
                )

            with c2:

                st.metric(
                    "Travel Time",
                    f"{float(vehicle_details['time']):.3f} min"
                )

            with c3:

                st.metric(
                    "Capacity",
                    f"{float(vehicle_details['demand']):.0f} / "
                    f"{float(vehicle_details['capacity']):.0f}"
                )


# ============================================================
# BEFORE VS AFTER
# ============================================================

if (
    st.session_state.before_details is not None
    and
    st.session_state.optimized_details is not None
    and
    st.session_state.incident_active
):

    before = st.session_state.before_details
    after = st.session_state.optimized_details

    # Distance is stored consistently in kilometres.
    before_distance = float(before["total_distance"])
    after_distance = float(after["total_distance"])

    before_time = float(before["total_time"])
    after_time = float(after["total_time"])

    # Positive = increase after the traffic incident.
    # Negative = decrease after the traffic incident.
    distance_change = after_distance - before_distance
    time_change = after_time - before_time

    distance_change_pct = (
        (distance_change / before_distance) * 100.0
        if before_distance > 0
        else 0.0
    )

    time_change_pct = (
        (time_change / before_time) * 100.0
        if before_time > 0
        else 0.0
    )

    st.divider()

    st.markdown(
        '<div class="section-title">'
        '📊 Before vs After Re-optimization'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Comparison of the route immediately before the simulated "
        "traffic incident and the QPSO route after re-optimization."
    )

    # --------------------------------------------------------
    # MAIN COMPARISON
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Before Distance",
            f"{before_distance:.3f} km"
        )

    with c2:

        st.metric(
            "After Distance",
            f"{after_distance:.3f} km",
            delta=f"{distance_change:+.3f} km",
            delta_color="off"
        )

    with c3:

        st.metric(
            "Before Travel Time",
            f"{before_time:.3f} min"
        )

    with c4:

        st.metric(
            "After Travel Time",
            f"{after_time:.3f} min",
            delta=f"{time_change:+.3f} min",
            delta_color="off"
        )

    # --------------------------------------------------------
    # RESPONSE SUMMARY
    # --------------------------------------------------------

    st.markdown("### 🚦 Traffic Response Summary")

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric(
            "Distance Change",
            f"{distance_change:+.3f} km",
            delta_color="off"
        )

        direction = (
            "increase" if distance_change > 0
            else "decrease" if distance_change < 0
            else "no change"
        )

        st.caption(
            f"{abs(distance_change_pct):.2f}% {direction} vs pre-incident route"
        )

    with s2:

        st.metric(
            "Travel-Time Change",
            f"{time_change:+.3f} min",
            delta_color="off"
        )

        direction = (
            "increase" if time_change > 0
            else "decrease" if time_change < 0
            else "no change"
        )

        st.caption(
            f"{abs(time_change_pct):.2f}% {direction} vs pre-incident route"
        )

    with s3:

        before_route_count = sum(
            1
            for route in st.session_state.before_routes.values()
            if len(route) > 2
        )

        after_route_count = sum(
            1
            for route in st.session_state.optimized_routes.values()
            if len(route) > 2
        )

        st.metric(
            "Active Vehicles",
            f"{after_route_count}",
            delta=f"{after_route_count - before_route_count:+d}"
        )

        st.caption(
            "Vehicles carrying at least one customer"
        )

    # --------------------------------------------------------
    # ROUTE CHANGE DETAILS
    # --------------------------------------------------------

    st.markdown("### 🔄 Route Changes")

    before_routes = (
        st.session_state.before_routes
    )

    after_routes = (
        st.session_state.optimized_routes
    )

    route_changed = False

    for vehicle_id in after_routes:

        before_route = before_routes.get(
            vehicle_id,
            []
        )

        after_route = after_routes.get(
            vehicle_id,
            []
        )

        if before_route != after_route:

            route_changed = True

            st.markdown(
                f"**🚚 {vehicle_id} — route changed**"
            )

            r1, r2 = st.columns(2)

            with r1:

                st.info(
                    "Before\n\n"
                    +
                    " → ".join(
                        before_route
                    )
                )

            with r2:

                st.success(
                    "After\n\n"
                    +
                    " → ".join(
                        after_route
                    )
                )

        else:

            st.write(
                f"🚚 **{vehicle_id}** — route unchanged"
            )

    if not route_changed:

        st.info(
            "The traffic-aware QPSO run produced the same "
            "customer sequence. The route was still evaluated "
            "using the updated traffic weights."
        )


# ============================================================
# ALGORITHM BENCHMARK
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '📊 Algorithm Benchmark'
    '</div>',
    unsafe_allow_html=True
)

BENCHMARK_FILE = os.path.join(
    PROJECT_ROOT,
    "results",
    "baseline_vs_qpso.csv"
)

if os.path.exists(BENCHMARK_FILE):

    try:

        benchmark_df = pd.read_csv(
            BENCHMARK_FILE
        )

        # ----------------------------------------------------
        # Extract benchmark values
        # ----------------------------------------------------

        travel_row = benchmark_df[
            benchmark_df["Metric"] == "Travel Time (minutes)"
        ]

        distance_row = benchmark_df[
            benchmark_df["Metric"] == "Distance (km)"
        ]

        improvement_row = benchmark_df[
            benchmark_df["Metric"] == "Improvement (%)"
        ]

        if not travel_row.empty and not distance_row.empty:

            baseline_time = float(
                travel_row.iloc[0]["Baseline"]
            )

            qpso_time = float(
                travel_row.iloc[0]["QPSO"]
            )

            baseline_distance = float(
                distance_row.iloc[0]["Baseline"]
            )

            qpso_distance = float(
                distance_row.iloc[0]["QPSO"]
            )

            if not improvement_row.empty:
                time_improvement = float(
                    improvement_row.iloc[0]["QPSO"]
                )
            else:
                time_improvement = (
                    (baseline_time - qpso_time)
                    / baseline_time
                    * 100
                    if baseline_time > 0
                    else 0.0
                )

            distance_improvement = (
                (baseline_distance - qpso_distance)
                / baseline_distance
                * 100
                if baseline_distance > 0
                else 0.0
            )

            # ------------------------------------------------
            # Benchmark metrics
            # ------------------------------------------------

            b1, b2, b3, b4 = st.columns(4)

            with b1:
                st.metric(
                    "Baseline Time",
                    f"{baseline_time:.2f} min"
                )

            with b2:
                st.metric(
                    "QPSO Time",
                    f"{qpso_time:.2f} min"
                )

            with b3:
                st.metric(
                    "Time Improvement",
                    f"{time_improvement:.2f}%",
                    delta_color="off"
                )

            with b4:
                st.metric(
                    "Distance Improvement",
                    f"{distance_improvement:.2f}%",
                    delta_color="off"
                )

            # ------------------------------------------------
            # Comparison charts
            # ------------------------------------------------

            st.markdown("### ⚖️ Baseline vs QPSO")

            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:

                time_chart = pd.DataFrame(
                    {
                        "Travel Time (min)": [
                            baseline_time,
                            qpso_time
                        ]
                    },
                    index=["Baseline", "QPSO"]
                )

                st.bar_chart(
                    time_chart,
                    height=300
                )

            with chart_col2:

                distance_chart = pd.DataFrame(
                    {
                        "Distance (km)": [
                            baseline_distance,
                            qpso_distance
                        ]
                    },
                    index=["Baseline", "QPSO"]
                )

                st.bar_chart(
                    distance_chart,
                    height=300
                )

            # ------------------------------------------------
            # Benchmark interpretation
            # ------------------------------------------------

            st.markdown("### 🧪 Experimental Result")

            st.info(
                f"For the current 10-customer scenario, the QPSO "
                f"solution measured {qpso_time:.2f} minutes of travel "
                f"time and {qpso_distance:.2f} km, compared with "
                f"{baseline_time:.2f} minutes and "
                f"{baseline_distance:.2f} km for the baseline. "
                f"The measured travel-time difference is "
                f"{baseline_time - qpso_time:.2f} minutes."
            )

            st.caption(
                "Benchmark values are loaded automatically from "
                "results/baseline_vs_qpso.csv. QPSO is stochastic, "
                "so results can vary between runs."
            )

        else:

            st.warning(
                "Benchmark file exists, but the expected metrics "
                "could not be found."
            )

    except Exception as error:

        st.error(
            f"Could not read benchmark results: {error}"
        )

else:

    st.warning(
        "Benchmark results are not available yet. "
        "Run: python optimization/compare.py"
    )


# ============================================================
# FLEET CAPACITY
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '📦 Fleet Capacity'
    '</div>',
    unsafe_allow_html=True
)

total_demand = float(
    customers["demand"].sum()
)

total_capacity = float(
    vehicles["capacity"].sum()
)

utilization = (
    total_demand
    /
    total_capacity
    *
    100
)

st.progress(
    min(
        utilization / 100,
        1.0
    )
)

st.write(
    f"Total demand: {total_demand:.0f}"
)

st.write(
    f"Total fleet capacity: {total_capacity:.0f}"
)

st.write(
    f"Capacity utilization: {utilization:.1f}%"
)


# ============================================================
# PROTOTYPE ARCHITECTURE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🧠 Prototype Architecture'
    '</div>',
    unsafe_allow_html=True
)

a1, a2 = st.columns(2)

with a1:

    st.markdown(
        """
        **Optimization**

        Quantum Particle Swarm Optimization (QPSO)

        **Routing**

        Capacitated Vehicle Routing Problem (CVRP)

        **Objective**

        Minimize transportation travel time
        """
    )

with a2:

    st.markdown(
        """
        **Road Network**

        Real Gachibowli road network

        **Traffic**

        Simulated dynamic traffic

        **Adaptive capability**

        Re-optimize routes after traffic changes
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SIH Prototype • Quantum-Inspired Intelligent "
    "Traffic Route Optimization"
)