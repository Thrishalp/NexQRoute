import os
import sys
import copy
import random
import json
import numpy as np
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
# IMPORT MODULES
# =========================================================

from graph.tomtom_matrix import build_live_matrix, get_route_geometry
from optimization.qpso import (
    qpso_optimize,
    get_customer_data,
    get_vehicle_data,
    calculate_solution_details
)

# =========================================================
# MAIN RE-OPTIMIZATION SCRIPT
# =========================================================

def main():
    print("\n" + "=" * 70)
    print("DYNAMIC TRAFFIC RE-OPTIMIZATION DEMO")
    print("=" * 70)

    # 1. Load Data
    depot_df = pd.read_csv("data/depot.csv").iloc[0]
    customers = pd.read_csv("data/customers.csv")
    vehicles = pd.read_csv("data/vehicles.csv")

    locations = [
        {
            "id": "depot",
            "latitude": depot_df["latitude"],
            "longitude": depot_df["longitude"]
        }
    ]

    for _, row in customers.iterrows():
        locations.append({
            "id": str(row["id"]),
            "latitude": row["latitude"],
            "longitude": row["longitude"]
        })

    # 2. Build Base Live Matrix
    print("Building LIVE TomTom travel-time matrix...")
    time_matrix, distance_matrix = build_live_matrix(locations)
    print("Live matrix created.")

    # Align labels with QPSO
    time_matrix.rename(index={"depot": "Depot"}, columns={"depot": "Depot"}, inplace=True)
    distance_matrix.rename(index={"depot": "Depot"}, columns={"depot": "Depot"}, inplace=True)

    customer_ids, demands = get_customer_data(customers)
    vehicle_ids, capacities = get_vehicle_data(vehicles)

    customer_ids = [str(x) for x in customer_ids]
    demands = {str(k): v for k, v in demands.items()}

    # 3. Simulate Traffic Incident on the Matrix
    print("\nSimulating major traffic incident on primary corridors...")
    incident_time_matrix = time_matrix.copy()

    # Penalize primary customer corridors by 15x
    target_stops = customer_ids[:5]
    for c in target_stops:
        for other in customer_ids:
            if c != other:
                incident_time_matrix.loc[c, other] *= 15.0
                incident_time_matrix.loc[other, c] *= 15.0
        incident_time_matrix.loc["Depot", c] *= 15.0
        incident_time_matrix.loc[c, "Depot"] *= 15.0

    print("Traffic incident penalties injected into travel-time matrix.")

    # 4. Run QPSO Re-Optimization
    print("\nStarting QPSO Re-Optimization under Incident conditions...")
    random.seed(101)
    np.random.seed(101)

    # best_position is the NumPy array, best_routes is the dict
    best_position, best_routes = qpso_optimize(
        customer_ids,
        demands,
        vehicle_ids,
        capacities,
        incident_time_matrix,
        distance_matrix
    )

    if best_routes is None:
        print("\nQPSO could not find a feasible solution.")
        sys.exit(1)

    # Calculate metrics by passing best_routes dictionary (NOT the numpy array)
    solution_details = calculate_solution_details(
        best_routes,
        incident_time_matrix,
        distance_matrix,
        demands,
        capacities
    )

    new_time = solution_details["total_time"]
    new_distance = solution_details["total_distance"]

    # 5. Generate Road Route Geometry via TomTom
    print("\nGenerating road-following geometry via TomTom...")
    location_lookup = {
        str(x["id"]): (x["latitude"], x["longitude"])
        for x in locations
    }

    route_geometry = {}

    for vehicle, route in best_routes.items():
        geometry = []
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]

            if start == "Depot":
                start = "depot"
            if end == "Depot":
                end = "depot"

            start_lat, start_lon = location_lookup[start]
            end_lat, end_lon = location_lookup[end]

            segment = get_route_geometry(
                start_lat,
                start_lon,
                end_lat,
                end_lon
            )

            if geometry and segment:
                geometry.extend(segment[1:])
            else:
                geometry.extend(segment)

        route_geometry[vehicle] = geometry

    # Save directly to results for the Leaflet dashboard
    output_geom_path = "results/optimized_route_geometry.json"
    os.makedirs("results", exist_ok=True)
    with open(output_geom_path, "w") as f:
        json.dump(route_geometry, f)

    print(f"Road route geometry saved to {output_geom_path}")

    # 6. Output for FastAPI stdout parsing
    print("\n" + "=" * 70)
    print("OPTIMIZATION RESULTS:")
    print(f"Best time: {new_time:.2f} min")
    print(f"Total distance: {new_distance:.2f} km")
    print(f"Routes: {best_routes}")
    print("=" * 70)


if __name__ == "__main__":
    main()