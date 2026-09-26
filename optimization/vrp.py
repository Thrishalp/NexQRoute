import os
import sys
import pandas as pd
import numpy as np


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


CUSTOMERS_FILE = "data/customers.csv"
VEHICLES_FILE = "data/vehicles.csv"
DEPOT_FILE = "data/depot.csv"

DISTANCE_FILE = "data/distance_matrix.csv"
TIME_FILE = "data/travel_time_matrix.csv"


# ---------------------------------------------------------
# Load problem data
# ---------------------------------------------------------

def load_problem():

    customers = pd.read_csv(CUSTOMERS_FILE)
    vehicles = pd.read_csv(VEHICLES_FILE)
    depot = pd.read_csv(DEPOT_FILE)

    distance_matrix = pd.read_csv(
        DISTANCE_FILE,
        index_col=0
    )

    time_matrix = pd.read_csv(
        TIME_FILE,
        index_col=0
    )

    return (
        customers,
        vehicles,
        depot,
        distance_matrix,
        time_matrix
    )


# ---------------------------------------------------------
# Get customer IDs and demands
# ---------------------------------------------------------

def get_customer_data(customers):

    customer_ids = customers["id"].astype(str).tolist()

    demands = {}

    for _, row in customers.iterrows():

        customer_id = str(row["id"])

        demands[customer_id] = float(
            row["demand"]
        )

    return customer_ids, demands


# ---------------------------------------------------------
# Get vehicle information
# ---------------------------------------------------------

def get_vehicle_data(vehicles):

    # Support common column names
    if "id" in vehicles.columns:
        vehicle_id_column = "id"

    elif "vehicle_id" in vehicles.columns:
        vehicle_id_column = "vehicle_id"

    else:
        vehicle_id_column = vehicles.columns[0]


    if "capacity" in vehicles.columns:
        capacity_column = "capacity"

    else:
        capacity_column = vehicles.columns[-1]


    vehicle_ids = []

    capacities = {}


    for _, row in vehicles.iterrows():

        vehicle_id = str(
            row[vehicle_id_column]
        )

        capacity = float(
            row[capacity_column]
        )

        vehicle_ids.append(
            vehicle_id
        )

        capacities[vehicle_id] = capacity


    return vehicle_ids, capacities


# ---------------------------------------------------------
# Calculate route distance
# ---------------------------------------------------------

def calculate_route_distance(
    route,
    distance_matrix
):

    total_distance = 0.0

    for i in range(len(route) - 1):

        start = route[i]
        end = route[i + 1]

        total_distance += float(
            distance_matrix.loc[start, end]
        )

    return total_distance


# ---------------------------------------------------------
# Calculate route travel time
# ---------------------------------------------------------

def calculate_route_time(
    route,
    time_matrix
):

    total_time = 0.0

    for i in range(len(route) - 1):

        start = route[i]
        end = route[i + 1]

        total_time += float(
            time_matrix.loc[start, end]
        )

    return total_time


# ---------------------------------------------------------
# Calculate route demand
# ---------------------------------------------------------

def calculate_route_demand(
    route,
    demands
):

    total_demand = 0.0

    for location in route:

        if location == "Depot":
            continue

        total_demand += demands.get(
            location,
            0
        )

    return total_demand


# ---------------------------------------------------------
# Check whether a route satisfies capacity
# ---------------------------------------------------------

def route_is_feasible(
    route,
    demands,
    vehicle_capacity
):

    route_demand = calculate_route_demand(
        route,
        demands
    )

    return route_demand <= vehicle_capacity


# ---------------------------------------------------------
# Calculate complete VRP solution
# ---------------------------------------------------------

def evaluate_solution(
    routes,
    demands,
    capacities,
    distance_matrix,
    time_matrix
):

    total_distance = 0.0
    total_time = 0.0

    total_demand = 0.0

    feasible = True

    vehicle_results = []


    for vehicle_id, route in routes.items():

        distance = calculate_route_distance(
            route,
            distance_matrix
        )

        travel_time = calculate_route_time(
            route,
            time_matrix
        )

        demand = calculate_route_demand(
            route,
            demands
        )

        capacity = capacities[vehicle_id]


        if demand > capacity:
            feasible = False


        total_distance += distance
        total_time += travel_time
        total_demand += demand


        vehicle_results.append({
            "vehicle": vehicle_id,
            "route": route,
            "distance_km": distance,
            "travel_time_min": travel_time,
            "demand": demand,
            "capacity": capacity,
            "remaining_capacity": capacity - demand,
            "feasible": demand <= capacity
        })


    return {
        "feasible": feasible,
        "total_distance_km": total_distance,
        "total_time_min": total_time,
        "total_demand": total_demand,
        "vehicles": vehicle_results
    }


# ---------------------------------------------------------
# Simple capacity-aware baseline
# ---------------------------------------------------------

def create_baseline_solution(
    customer_ids,
    demands,
    vehicle_ids,
    capacities
):

    routes = {}

    for vehicle_id in vehicle_ids:

        routes[vehicle_id] = [
            "Depot",
            "Depot"
        ]


    current_vehicle_index = 0


    for customer in customer_ids:

        demand = demands[customer]

        assigned = False


        # Try current vehicle first
        for attempt in range(
            len(vehicle_ids)
        ):

            vehicle_index = (
                current_vehicle_index + attempt
            ) % len(vehicle_ids)

            vehicle_id = vehicle_ids[
                vehicle_index
            ]

            route = routes[vehicle_id]

            current_demand = calculate_route_demand(
                route,
                demands
            )


            if (
                current_demand + demand
                <= capacities[vehicle_id]
            ):

                route.insert(
                    len(route) - 1,
                    customer
                )

                current_vehicle_index = vehicle_index

                assigned = True

                break


        if not assigned:

            raise ValueError(
                f"Customer {customer} could not "
                f"be assigned to a vehicle."
            )


    return routes


# ---------------------------------------------------------
# Print solution
# ---------------------------------------------------------

def print_solution(solution):

    print("\n")
    print("=" * 60)
    print("VRP BASELINE SOLUTION")
    print("=" * 60)


    print(
        f"\nFeasible: {solution['feasible']}"
    )

    print(
        f"Total distance: "
        f"{solution['total_distance_km']:.2f} km"
    )

    print(
        f"Total travel time: "
        f"{solution['total_time_min']:.2f} minutes"
    )

    print(
        f"Total demand: "
        f"{solution['total_demand']:.2f}"
    )


    print("\nVehicle routes:")
    print("-" * 60)


    for vehicle in solution["vehicles"]:

        route_text = " → ".join(
            vehicle["route"]
        )

        print(
            f"\n{vehicle['vehicle']}"
        )

        print(
            f"Route: {route_text}"
        )

        print(
            f"Distance: "
            f"{vehicle['distance_km']:.2f} km"
        )

        print(
            f"Travel time: "
            f"{vehicle['travel_time_min']:.2f} min"
        )

        print(
            f"Demand: "
            f"{vehicle['demand']:.0f} / "
            f"{vehicle['capacity']:.0f}"
        )

        print(
            f"Remaining capacity: "
            f"{vehicle['remaining_capacity']:.0f}"
        )

        print(
            f"Feasible: "
            f"{vehicle['feasible']}"
        )


    print("\n")
    print("=" * 60)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("Loading VRP data...")


    (
        customers,
        vehicles,
        depot,
        distance_matrix,
        time_matrix
    ) = load_problem()


    customer_ids, demands = get_customer_data(
        customers
    )


    vehicle_ids, capacities = get_vehicle_data(
        vehicles
    )


    print(
        f"\nCustomers: {len(customer_ids)}"
    )

    print(
        f"Vehicles: {len(vehicle_ids)}"
    )


    print("\nCustomer demands:")

    for customer in customer_ids:

        print(
            f"{customer}: "
            f"{demands[customer]:.0f}"
        )


    print("\nVehicle capacities:")

    for vehicle in vehicle_ids:

        print(
            f"{vehicle}: "
            f"{capacities[vehicle]:.0f}"
        )


    # -----------------------------------------------------
    # Create baseline
    # -----------------------------------------------------

    print(
        "\nCreating capacity-aware baseline..."
    )


    routes = create_baseline_solution(
        customer_ids,
        demands,
        vehicle_ids,
        capacities
    )


    # -----------------------------------------------------
    # Evaluate baseline
    # -----------------------------------------------------

    solution = evaluate_solution(
        routes,
        demands,
        capacities,
        distance_matrix,
        time_matrix
    )


    # -----------------------------------------------------
    # Display
    # -----------------------------------------------------

    print_solution(solution)


if __name__ == "__main__":
    main()