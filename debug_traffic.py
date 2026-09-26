import os
import sys
import numpy as np
import pandas as pd
import osmnx as ox

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from simulation.traffic import add_traffic_weights, simulate_traffic_change
from graph.routing import get_locations, calculate_matrices


print("=" * 60)
print("TRAFFIC MATRIX DIAGNOSTIC")
print("=" * 60)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

print("\n1. Loading road network...")

G = ox.load_graphml(
    os.path.join(PROJECT_ROOT, "data", "gachibowli_roads.graphml")
)

print(f"Road network loaded")
print(f"Nodes: {len(G.nodes)}")
print(f"Edges: {len(G.edges)}")


customers = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data", "customers.csv")
)

depot = pd.read_csv(
    os.path.join(PROJECT_ROOT, "data", "depot.csv")
)

print(f"Customers: {len(customers)}")


# ---------------------------------------------------------
# GET LOCATIONS
# ---------------------------------------------------------

locations = get_locations(customers, depot)

print("\n2. Locations:")
print(locations)


# ---------------------------------------------------------
# INITIAL TRAFFIC
# ---------------------------------------------------------

print("\n3. Applying initial traffic...")

G = add_traffic_weights(G)

print("Initial traffic applied.")


# ---------------------------------------------------------
# INITIAL MATRIX
# ---------------------------------------------------------

print("\n4. Calculating INITIAL traffic matrix...")

distance_matrix, time_matrix = calculate_matrices(
    G,
    locations
)

distance_matrix = np.asarray(distance_matrix, dtype=float)
time_matrix = np.asarray(time_matrix, dtype=float)

print("\nInitial distance matrix:")
print("Shape:", distance_matrix.shape)

print(
    "Finite values:",
    np.isfinite(distance_matrix).sum(),
    "/",
    distance_matrix.size
)

print(
    "Infinite values:",
    np.isinf(distance_matrix).sum()
)

print("\nInitial time matrix:")
print("Shape:", time_matrix.shape)

print(
    "Finite values:",
    np.isfinite(time_matrix).sum(),
    "/",
    time_matrix.size
)

print(
    "Infinite values:",
    np.isinf(time_matrix).sum()
)


# ---------------------------------------------------------
# TRAFFIC INCIDENT
# ---------------------------------------------------------

print("\n5. Simulating traffic incident...")

G = simulate_traffic_change(
    G,
    number_of_roads=20
)

print("Traffic incident applied.")


# ---------------------------------------------------------
# UPDATED MATRIX
# ---------------------------------------------------------

print("\n6. Calculating UPDATED traffic matrix...")

distance_matrix_after, time_matrix_after = calculate_matrices(
    G,
    locations
)

distance_matrix_after = np.asarray(
    distance_matrix_after,
    dtype=float
)

time_matrix_after = np.asarray(
    time_matrix_after,
    dtype=float
)


print("\nUPDATED distance matrix:")
print("Shape:", distance_matrix_after.shape)

print(
    "Finite values:",
    np.isfinite(distance_matrix_after).sum(),
    "/",
    distance_matrix_after.size
)

print(
    "Infinite values:",
    np.isinf(distance_matrix_after).sum()
)


print("\nUPDATED time matrix:")
print("Shape:", time_matrix_after.shape)

print(
    "Finite values:",
    np.isfinite(time_matrix_after).sum(),
    "/",
    time_matrix_after.size
)

print(
    "Infinite values:",
    np.isinf(time_matrix_after).sum()
)


# ---------------------------------------------------------
# CHECK NaN
# ---------------------------------------------------------

print("\n7. Checking NaN values...")

print(
    "Distance NaN:",
    np.isnan(distance_matrix_after).sum()
)

print(
    "Time NaN:",
    np.isnan(time_matrix_after).sum()
)


# ---------------------------------------------------------
# PRINT PROBLEMATIC PAIRS
# ---------------------------------------------------------

print("\n8. Checking unreachable locations...")

problem_found = False

for i in range(len(locations)):
    for j in range(len(locations)):

        if not np.isfinite(time_matrix_after[i, j]):

            print(
                f"UNREACHABLE: "
                f"{locations[i]} -> {locations[j]}"
            )

            problem_found = True


if not problem_found:
    print("GOOD: Every location can reach every other location.")


# ---------------------------------------------------------
# FINAL RESULT
# ---------------------------------------------------------

print("\n" + "=" * 60)

if (
    np.isfinite(time_matrix_after).all()
    and np.isfinite(distance_matrix_after).all()
):
    print("RESULT: MATRIX IS HEALTHY")
    print("The problem is probably inside QPSO input/decoding.")
else:
    print("RESULT: MATRIX HAS NON-FINITE VALUES")
    print("This is the likely cause of the dashboard failure.")

print("=" * 60)