import os
import sys
import json

import osmnx as ox
import networkx as nx
import pandas as pd


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# FILES
# =========================================================

GRAPH_FILE = "data/gachibowli_roads.graphml"
CUSTOMERS_FILE = "data/customers.csv"
DEPOT_FILE = "data/depot.csv"


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    print("Loading road network...")

    G = ox.load_graphml(
        GRAPH_FILE
    )

    customers = pd.read_csv(
        CUSTOMERS_FILE
    )

    depot = pd.read_csv(
        DEPOT_FILE
    )

    return (
        G,
        customers,
        depot
    )


# =========================================================
# CREATE LOCATION DICTIONARY
# =========================================================

def create_location_dictionary(
    customers,
    depot
):

    locations = {}

    # -----------------------------------------------------
    # Depot
    # -----------------------------------------------------

    locations["Depot"] = int(
        depot.iloc[0]["node"]
    )


    # -----------------------------------------------------
    # Customers
    # -----------------------------------------------------

    for _, row in customers.iterrows():

        customer_id = str(
            row["id"]
        )

        locations[customer_id] = int(
            row["node"]
        )


    return locations


# =========================================================
# FIND ROAD PATH
# =========================================================

def get_road_path(
    G,
    start_node,
    end_node
):
    """
    Find the actual sequence of road nodes between
    two locations.

    Traffic-aware travel time is used when available.
    """

    try:

        path = nx.shortest_path(
            G,
            start_node,
            end_node,
            weight="traffic_time"
        )

        return path

    except (nx.NetworkXNoPath, nx.NodeNotFound):

        # Fallback to physical distance

        try:

            path = nx.shortest_path(
                G,
                start_node,
                end_node,
                weight="length"
            )

            return path

        except (
            nx.NetworkXNoPath,
            nx.NodeNotFound
        ):

            return []


# =========================================================
# CONVERT ROAD PATH TO COORDINATES
# =========================================================

def path_to_coordinates(
    G,
    path
):

    coordinates = []

    for node in path:

        node_data = G.nodes[node]

        latitude = float(
            node_data["y"]
        )

        longitude = float(
            node_data["x"]
        )

        coordinates.append([
            latitude,
            longitude
        ])


    return coordinates


# =========================================================
# CREATE ROUTE GEOMETRY
# =========================================================

def create_route_geometry(
    G,
    route,
    locations
):
    """
    Convert a route such as:

    Depot → C1 → C5 → C7 → Depot

    into actual road coordinates.
    """

    complete_coordinates = []


    for i in range(
        len(route) - 1
    ):

        start_location = route[i]
        end_location = route[i + 1]


        start_node = locations[
            start_location
        ]

        end_node = locations[
            end_location
        ]


        path = get_road_path(
            G,
            start_node,
            end_node
        )


        if not path:

            continue


        coordinates = path_to_coordinates(
            G,
            path
        )


        # -------------------------------------------------
        # Avoid duplicate coordinate at segment joins
        # -------------------------------------------------

        if complete_coordinates:

            coordinates = coordinates[1:]


        complete_coordinates.extend(
            coordinates
        )


    return complete_coordinates


# =========================================================
# CREATE ALL ROUTE GEOMETRIES
# =========================================================

def create_all_route_geometries(
    G,
    routes,
    locations
):

    route_geometries = {}


    for vehicle_id, route in routes.items():

        print(
            f"Creating geometry for {vehicle_id}..."
        )


        coordinates = create_route_geometry(
            G,
            route,
            locations
        )


        route_geometries[vehicle_id] = coordinates


        print(
            f"  Route nodes: "
            f"{len(coordinates)}"
        )


    return route_geometries


# =========================================================
# SAVE GEOMETRY
# =========================================================

def save_route_geometries(
    route_geometries,
    output_file="results/route_geometries.json"
):

    os.makedirs(
        "results",
        exist_ok=True
    )


    with open(
        output_file,
        "w"
    ) as file:

        json.dump(
            route_geometries,
            file,
            indent=2
        )


    print(
        f"\nRoute geometry saved to:"
    )

    print(
        output_file
    )


# =========================================================
# TEST ROUTE
# =========================================================

def main():

    print("\n")
    print("=" * 65)
    print("ROAD ROUTE GEOMETRY TEST")
    print("=" * 65)


    # -----------------------------------------------------
    # Load
    # -----------------------------------------------------

    (
        G,
        customers,
        depot
    ) = load_data()


    # -----------------------------------------------------
    # Locations
    # -----------------------------------------------------

    locations = create_location_dictionary(
        customers,
        depot
    )


    print(
        f"\nLocations loaded: "
        f"{len(locations)}"
    )


    # -----------------------------------------------------
    # Create a simple test route
    # -----------------------------------------------------

    customer_ids = (
        customers["id"]
        .astype(str)
        .tolist()
    )


    # Use first 3 customers for test
    test_route = (
        ["Depot"]
        +
        customer_ids[:3]
        +
        ["Depot"]
    )


    print(
        "\nTest route:"
    )

    print(
        " → ".join(test_route)
    )


    # -----------------------------------------------------
    # Generate geometry
    # -----------------------------------------------------

    geometry = create_route_geometry(
        G,
        test_route,
        locations
    )


    print(
        f"\nActual road coordinates generated: "
        f"{len(geometry)}"
    )


    if geometry:

        print(
            "\nFirst coordinate:"
        )

        print(
            geometry[0]
        )


        print(
            "\nLast coordinate:"
        )

        print(
            geometry[-1]
        )


        print(
            "\n✅ Road geometry successfully generated."
        )


    else:

        print(
            "\n❌ Could not generate route geometry."
        )


    # -----------------------------------------------------
    # Save test geometry
    # -----------------------------------------------------

    save_route_geometries({

        "TEST_ROUTE": geometry

    })


    print("\n")
    print("=" * 65)
    print("ROAD GEOMETRY TEST COMPLETED")
    print("=" * 65)


if __name__ == "__main__":

    main()