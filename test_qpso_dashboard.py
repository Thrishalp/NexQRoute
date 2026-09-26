import os
import sys
import random

import numpy as np
import pandas as pd
import osmnx as ox


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(
    0,
    PROJECT_ROOT
)


# =========================================================
# PROJECT IMPORTS
# =========================================================

from simulation.traffic import (
    add_traffic_weights,
    simulate_traffic_change
)

from graph.routing import (
    get_locations,
    calculate_matrices
)

from optimization.qpso import (
    qpso_optimize,
    calculate_solution_details
)


# =========================================================
# FILE PATHS
# =========================================================

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


# =========================================================
# RANDOM SEED
# =========================================================

random.seed(42)
np.random.seed(42)


# =========================================================
# HEADER
# =========================================================

print()
print("=" * 65)
print("DIRECT DASHBOARD QPSO TEST")
print("=" * 65)


# =========================================================
# LOAD ROAD NETWORK
# =========================================================

print()
print("1. Loading road network...")

G = ox.load_graphml(
    GRAPH_FILE
)

print(
    "Road network loaded successfully."
)

print(
    f"Nodes: {len(G.nodes)}"
)

print(
    f"Edges: {len(G.edges)}"
)


# =========================================================
# LOAD DATA
# =========================================================

print()
print("2. Loading scenario data...")

customers = pd.read_csv(
    CUSTOMERS_FILE
)

depot = pd.read_csv(
    DEPOT_FILE
)

vehicles = pd.read_csv(
    VEHICLES_FILE
)

print(
    f"Customers: {len(customers)}"
)

print(
    f"Vehicles: {len(vehicles)}"
)


# =========================================================
# GET LOCATIONS
# =========================================================

print()
print("3. Building location list...")

# IMPORTANT:
# Do NOT convert this list to strings.
#
# calculate_matrices() expects:
#
# locations[i]["node"]

locations = get_locations(
    customers,
    depot
)

print(
    "Locations created successfully."
)

print()

for location in locations:

    print(
        location
    )


# =========================================================
# APPLY INITIAL TRAFFIC
# =========================================================

print()
print("4. Applying initial traffic conditions...")

G = add_traffic_weights(
    G
)

print(
    "Initial traffic applied."
)


# =========================================================
# SIMULATE TRAFFIC INCIDENT
# =========================================================

print()
print("5. Simulating traffic incident...")

G = simulate_traffic_change(
    G,
    number_of_roads=20
)

print(
    "Traffic incident applied to 20 road segments."
)


# =========================================================
# CALCULATE MATRICES
# =========================================================

print()
print("6. Calculating traffic-aware road matrices...")

distance_matrix, time_matrix = calculate_matrices(
    G,
    locations
)

print(
    "Road matrices calculated successfully."
)


# =========================================================
# CONVERT MATRICES TO NUMPY
# =========================================================

distance_matrix = np.asarray(
    distance_matrix,
    dtype=float
)

time_matrix = np.asarray(
    time_matrix,
    dtype=float
)


# =========================================================
# MATRIX VALIDATION
# =========================================================

print()
print("7. Validating matrices...")

print(
    f"Distance matrix shape: "
    f"{distance_matrix.shape}"
)

print(
    f"Time matrix shape: "
    f"{time_matrix.shape}"
)

print(
    "All distance values finite:",
    np.isfinite(distance_matrix).all()
)

print(
    "All time values finite:",
    np.isfinite(time_matrix).all()
)

print(
    "Distance NaN values:",
    np.isnan(distance_matrix).sum()
)

print(
    "Time NaN values:",
    np.isnan(time_matrix).sum()
)


# =========================================================
# CREATE MATRIX LABELS
# =========================================================

print()
print("8. Creating matrix labels...")

# get_locations() returns dictionaries.
#
# Example:
#
# {"id": "C1", "node": 12345}
#
# We need only the ID for the DataFrame labels.

location_labels = []

for location in locations:

    location_labels.append(
        str(location["id"])
    )

print(
    "Matrix labels:"
)

print(
    location_labels
)


# =========================================================
# CREATE DATAFRAMES
# =========================================================

distance_df = pd.DataFrame(
    distance_matrix,
    index=location_labels,
    columns=location_labels
)

time_df = pd.DataFrame(
    time_matrix,
    index=location_labels,
    columns=location_labels
)


print()
print(
    "Distance DataFrame created:"
)

print(
    distance_df.shape
)

print()
print(
    "Time DataFrame created:"
)

print(
    time_df.shape
)


# =========================================================
# CUSTOMER DATA
# =========================================================

print()
print("9. Preparing customer data...")


customer_ids = (
    customers["id"]
    .astype(str)
    .tolist()
)


# IMPORTANT:
# QPSO expects a dictionary:
#
# demands["C1"]
# demands["C2"]
#
# NOT a list.

demands = {

    str(row["id"]):
    float(row["demand"])

    for _, row
    in customers.iterrows()

}


# =========================================================
# VEHICLE DATA
# =========================================================

print()
print("10. Preparing vehicle data...")


if "id" in vehicles.columns:

    vehicle_id_column = "id"

elif "vehicle_id" in vehicles.columns:

    vehicle_id_column = "vehicle_id"

else:

    raise ValueError(
        "Could not find vehicle ID column."
    )


vehicle_ids = (
    vehicles[vehicle_id_column]
    .astype(str)
    .tolist()
)


# IMPORTANT:
# QPSO expects a dictionary:
#
# capacities["V1"]
# capacities["V2"]
#
# NOT a list.

capacities = {

    str(row[vehicle_id_column]):
    float(row["capacity"])

    for _, row
    in vehicles.iterrows()

}


# =========================================================
# PRINT INPUT
# =========================================================

print()
print("=" * 65)
print("QPSO INPUT")
print("=" * 65)

print()

print(
    "Customer IDs:"
)

print(
    customer_ids
)

print()

print(
    "Demands:"
)

print(
    demands
)

print()

print(
    "Vehicle IDs:"
)

print(
    vehicle_ids
)

print()

print(
    "Capacities:"
)

print(
    capacities
)

print()

print(
    "Total demand:",
    sum(demands.values())
)

print(
    "Total capacity:",
    sum(capacities.values())
)


# =========================================================
# BASIC FEASIBILITY CHECK
# =========================================================

print()
print("11. Checking basic feasibility...")

total_demand = sum(
    demands.values()
)

total_capacity = sum(
    capacities.values()
)


if total_demand <= total_capacity:

    print(
        "GOOD: Total demand fits within "
        "total vehicle capacity."
    )

else:

    print(
        "ERROR: Total demand exceeds "
        "vehicle capacity."
    )

    sys.exit(1)


# =========================================================
# CHECK INDIVIDUAL CUSTOMER DEMANDS
# =========================================================

maximum_capacity = max(
    capacities.values()
)

oversized_customers = []

for customer_id, demand in demands.items():

    if demand > maximum_capacity:

        oversized_customers.append(
            customer_id
        )


if len(oversized_customers) == 0:

    print(
        "GOOD: No customer exceeds "
        "maximum vehicle capacity."
    )

else:

    print(
        "ERROR: These customers are too large:"
    )

    print(
        oversized_customers
    )

    sys.exit(1)


# =========================================================
# CHECK MATRIX LABELS
# =========================================================

print()
print("12. Checking matrix labels...")

missing_labels = []

for location_id in location_labels:

    if location_id not in time_df.index:

        missing_labels.append(
            location_id
        )

    if location_id not in time_df.columns:

        missing_labels.append(
            location_id
        )


if len(missing_labels) == 0:

    print(
        "GOOD: All location labels exist "
        "in the matrices."
    )

else:

    print(
        "ERROR: Missing matrix labels:"
    )

    print(
        missing_labels
    )

    sys.exit(1)


# =========================================================
# CHECK MATRIX VALUES
# =========================================================

print()
print("13. Checking matrix values...")

matrix_problem = False


for start in location_labels:

    for end in location_labels:

        time_value = float(
            time_df.loc[start, end]
        )

        distance_value = float(
            distance_df.loc[start, end]
        )


        if not np.isfinite(time_value):

            print(
                f"Invalid time: "
                f"{start} -> {end}"
            )

            matrix_problem = True


        if not np.isfinite(distance_value):

            print(
                f"Invalid distance: "
                f"{start} -> {end}"
            )

            matrix_problem = True


if matrix_problem:

    print()
    print(
        "❌ Matrix validation failed."
    )

    sys.exit(1)


print(
    "GOOD: All matrix values are finite."
)


# =========================================================
# RUN QPSO
# =========================================================

print()
print("=" * 65)
print("RUNNING QPSO")
print("=" * 65)

print()

print(
    "Starting QPSO with traffic-updated matrices..."
)


try:

    result = qpso_optimize(

        customer_ids,

        demands,

        vehicle_ids,

        capacities,

        time_df,

        distance_df

    )

except Exception as error:

    print()
    print("=" * 65)
    print("QPSO EXECUTION ERROR")
    print("=" * 65)

    print()

    print(
        "Error type:",
        type(error).__name__
    )

    print(
        "Error:",
        str(error)
    )

    raise


# =========================================================
# CHECK RESULT
# =========================================================

print()
print("=" * 65)
print("QPSO RESULT")
print("=" * 65)


if result is None:

    print()
    print(
        "❌ QPSO returned None."
    )

    print()
    print(
        "The actual problem is inside "
        "qpso_optimize() / route decoding."
    )

    sys.exit(0)


best_position, best_routes = result


if best_routes is None:

    print()
    print(
        "❌ QPSO returned no routes."
    )

    sys.exit(0)


# =========================================================
# SUCCESS
# =========================================================

print()
print(
    "✅ QPSO FOUND A SOLUTION!"
)


# =========================================================
# PRINT ROUTES
# =========================================================

print()
print(
    "Optimized routes:"
)

print(
    "-" * 65
)


for vehicle_id, route in best_routes.items():

    print()

    print(
        f"{vehicle_id}:"
    )

    print(
        " -> ".join(route)
    )


# =========================================================
# CALCULATE DETAILS
# =========================================================

print()
print(
    "Calculating solution details..."
)


details = calculate_solution_details(

    best_routes,

    time_df,

    distance_df,

    demands,

    capacities

)


# =========================================================
# TOTAL RESULTS
# =========================================================

print()
print("=" * 65)
print("FINAL QPSO RESULTS")
print("=" * 65)

print()

print(
    f"Total travel time: "
    f"{details['total_time']:.2f} minutes"
)

print(
    f"Total distance: "
    f"{details['total_distance']:.2f} km"
)


# =========================================================
# VEHICLE RESULTS
# =========================================================

print()
print(
    "Vehicle details:"
)

print(
    "-" * 65
)


for vehicle in details["vehicles"]:

    print()

    print(
        f"Vehicle: "
        f"{vehicle['vehicle']}"
    )

    print(
        "Route: "
        +
        " -> ".join(
            vehicle["route"]
        )
    )

    print(
        f"Distance: "
        f"{vehicle['distance']:.2f} km"
    )

    print(
        f"Travel time: "
        f"{vehicle['time']:.2f} min"
    )

    print(
        f"Demand: "
        f"{vehicle['demand']:.0f} / "
        f"{vehicle['capacity']:.0f}"
    )

    print(
        f"Remaining capacity: "
        f"{vehicle['remaining']:.0f}"
    )


# =========================================================
# CUSTOMER COVERAGE
# =========================================================

print()
print(
    "Checking customer coverage..."
)


visited_customers = []

for route in best_routes.values():

    for location in route:

        if location != "Depot":

            visited_customers.append(
                location
            )


expected_customers = set(
    customer_ids
)

visited_customers = set(
    visited_customers
)


missing_customers = (
    expected_customers
    -
    visited_customers
)


extra_customers = (
    visited_customers
    -
    expected_customers
)


if (
    len(missing_customers) == 0
    and
    len(extra_customers) == 0
):

    print(
        "✅ All customers are correctly covered."
    )

else:

    print(
        "⚠️ Customer coverage issue."
    )

    print(
        "Missing:",
        missing_customers
    )

    print(
        "Unexpected:",
        extra_customers
    )


# =========================================================
# COMPLETE
# =========================================================

print()
print("=" * 65)
print("DIRECT DASHBOARD QPSO TEST COMPLETED")
print("=" * 65)

print()