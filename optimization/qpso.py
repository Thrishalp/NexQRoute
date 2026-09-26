import os
import sys
import random
import math
import copy

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

if PROJECT_ROOT not in sys.path:
    sys.path.insert(
        0,
        PROJECT_ROOT
    )


# =========================================================
# FILES
# =========================================================

CUSTOMERS_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "customers.csv"
)

VEHICLES_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "vehicles.csv"
)

DISTANCE_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "distance_matrix.csv"
)

TIME_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "travel_time_matrix.csv"
)


# =========================================================
# QPSO SETTINGS
# =========================================================

NUM_PARTICLES = 40

MAX_ITERATIONS = 150

ALPHA_START = 1.0

ALPHA_END = 0.5

RANDOM_SEED = 42


# =========================================================
# LOAD DATA
# =========================================================

def load_problem():

    customers = pd.read_csv(
        CUSTOMERS_FILE
    )

    vehicles = pd.read_csv(
        VEHICLES_FILE
    )

    distance_matrix = pd.read_csv(
        DISTANCE_FILE,
        index_col=0
    )

    time_matrix = pd.read_csv(
        TIME_FILE,
        index_col=0
    )

    distance_matrix.index = (
        distance_matrix.index.astype(str)
    )

    distance_matrix.columns = (
        distance_matrix.columns.astype(str)
    )

    time_matrix.index = (
        time_matrix.index.astype(str)
    )

    time_matrix.columns = (
        time_matrix.columns.astype(str)
    )

    return (
        customers,
        vehicles,
        distance_matrix,
        time_matrix
    )


# =========================================================
# CUSTOMER DATA
# =========================================================

def get_customer_data(customers):

    customer_ids = (
        customers["id"]
        .astype(str)
        .tolist()
    )

    demands = {}

    for _, row in customers.iterrows():

        customer_id = str(
            row["id"]
        )

        demands[customer_id] = float(
            row["demand"]
        )

    return (
        customer_ids,
        demands
    )


# =========================================================
# VEHICLE DATA
# =========================================================

def get_vehicle_data(vehicles):

    if "id" in vehicles.columns:

        id_column = "id"

    elif "vehicle_id" in vehicles.columns:

        id_column = "vehicle_id"

    else:

        id_column = vehicles.columns[0]


    if "capacity" in vehicles.columns:

        capacity_column = "capacity"

    else:

        capacity_column = vehicles.columns[-1]


    vehicle_ids = []

    capacities = {}


    for _, row in vehicles.iterrows():

        vehicle_id = str(
            row[id_column]
        )

        capacity = float(
            row[capacity_column]
        )

        vehicle_ids.append(
            vehicle_id
        )

        capacities[vehicle_id] = capacity


    return (
        vehicle_ids,
        capacities
    )


# =========================================================
# RANDOM KEY DECODING
# =========================================================

def position_to_permutation(
    position,
    customer_ids
):

    sorted_indices = np.argsort(
        position
    )

    permutation = [

        customer_ids[index]

        for index in sorted_indices

    ]

    return permutation


# =========================================================
# CAPACITY-AWARE ROUTE DECODING
# =========================================================

def permutation_to_routes(
    permutation,
    demands,
    vehicle_ids,
    capacities
):

    if not vehicle_ids:
        return None


    routes = {

        vehicle_id: [
            "Depot",
            "Depot"
        ]

        for vehicle_id in vehicle_ids

    }


    current_vehicle_index = 0

    current_load = 0.0


    for customer in permutation:

        if customer not in demands:

            return None


        demand = float(
            demands[customer]
        )


        # -------------------------------------------------
        # Find a vehicle that can accept this customer
        # -------------------------------------------------

        assigned = False


        while (
            current_vehicle_index
            <
            len(vehicle_ids)
        ):

            vehicle_id = vehicle_ids[
                current_vehicle_index
            ]

            capacity = float(
                capacities[vehicle_id]
            )


            if demand > capacity:

                current_vehicle_index += 1

                current_load = 0.0

                continue


            if (
                current_load + demand
                <= capacity
            ):

                routes[vehicle_id].insert(

                    len(
                        routes[vehicle_id]
                    ) - 1,

                    customer

                )

                current_load += demand

                assigned = True

                break


            current_vehicle_index += 1

            current_load = 0.0


        if not assigned:

            return None


    return routes


# =========================================================
# ROUTE TRAVEL TIME
# =========================================================

def calculate_route_time(
    route,
    time_matrix
):

    total_time = 0.0


    for i in range(
        len(route) - 1
    ):

        start = str(
            route[i]
        )

        end = str(
            route[i + 1]
        )


        try:

            value = float(
                time_matrix.loc[
                    start,
                    end
                ]
            )

        except (
            KeyError,
            TypeError,
            ValueError
        ):

            return float("inf")


        if not math.isfinite(value):

            return float("inf")


        total_time += value


    return total_time


# =========================================================
# ROUTE DISTANCE
# =========================================================

def calculate_route_distance(
    route,
    distance_matrix
):

    total_distance = 0.0


    for i in range(
        len(route) - 1
    ):

        start = str(
            route[i]
        )

        end = str(
            route[i + 1]
        )


        try:

            value = float(
                distance_matrix.loc[
                    start,
                    end
                ]
            )

        except (
            KeyError,
            TypeError,
            ValueError
        ):

            return float("inf")


        if not math.isfinite(value):

            return float("inf")


        total_distance += value


    return total_distance


# =========================================================
# EVALUATE ROUTES
# =========================================================

def evaluate_routes(
    routes,
    time_matrix,
    distance_matrix,
    demands
):

    if routes is None:

        return float("inf")


    total_time = 0.0


    for route in routes.values():

        # Empty vehicle is valid

        if len(route) <= 2:

            continue


        route_time = calculate_route_time(

            route,

            time_matrix

        )


        route_distance = calculate_route_distance(

            route,

            distance_matrix

        )


        if not math.isfinite(
            route_time
        ):

            return float("inf")


        if not math.isfinite(
            route_distance
        ):

            return float("inf")


        total_time += route_time


    return total_time


# =========================================================
# CHECK CAPACITY FEASIBILITY
# =========================================================

def check_capacity_feasibility(
    routes,
    demands,
    capacities
):

    if routes is None:

        return False


    for vehicle_id, route in routes.items():

        total_demand = 0.0


        for location in route:

            if location == "Depot":

                continue


            if location not in demands:

                return False


            total_demand += float(
                demands[location]
            )


        if total_demand > float(
            capacities[vehicle_id]
        ):

            return False


    return True


# =========================================================
# CHECK ALL CUSTOMERS
# =========================================================

def check_customer_coverage(
    routes,
    customer_ids
):

    if routes is None:

        return False


    found = []


    for route in routes.values():

        for location in route:

            if location != "Depot":

                found.append(
                    str(location)
                )


    expected = sorted(
        str(x)
        for x in customer_ids
    )

    actual = sorted(
        found
    )


    return expected == actual


# =========================================================
# SOLUTION DETAILS
# =========================================================

def calculate_solution_details(
    routes,
    time_matrix,
    distance_matrix,
    demands,
    capacities
):

    if routes is None:

        return None


    total_time = 0.0

    total_distance = 0.0

    vehicle_details = []


    for vehicle_id, route in routes.items():

        route_time = calculate_route_time(

            route,

            time_matrix

        )


        route_distance = calculate_route_distance(

            route,

            distance_matrix

        )


        demand = 0.0


        for location in route:

            if location != "Depot":

                demand += float(
                    demands[location]
                )


        capacity = float(
            capacities[vehicle_id]
        )


        remaining = (
            capacity
            -
            demand
        )


        total_time += route_time

        total_distance += route_distance


        vehicle_details.append({

            "vehicle": vehicle_id,

            "route": route,

            "distance": route_distance,

            "time": route_time,

            "demand": demand,

            "capacity": capacity,

            "remaining": remaining

        })


    return {

        "feasible": True,

        "total_time": total_time,

        "total_distance": total_distance,

        "vehicles": vehicle_details

    }


# =========================================================
# CREATE PARTICLE
# =========================================================

def create_particle(
    number_of_customers
):

    return np.random.uniform(

        0,

        1,

        number_of_customers

    )


# =========================================================
# INITIALIZE SWARM
# =========================================================

def initialize_swarm(
    number_of_particles,
    number_of_customers
):

    particles = []


    for _ in range(
        number_of_particles
    ):

        particles.append(

            create_particle(
                number_of_customers
            )

        )


    return np.array(
        particles
    )


# =========================================================
# CREATE FEASIBLE INITIAL PARTICLE
# =========================================================

def create_feasible_particle(
    customer_ids,
    demands,
    vehicle_ids,
    capacities,
    time_matrix,
    distance_matrix
):

    # Try many random permutations

    for _ in range(200):

        permutation = customer_ids.copy()

        random.shuffle(
            permutation
        )


        routes = permutation_to_routes(

            permutation,

            demands,

            vehicle_ids,

            capacities

        )


        if routes is None:

            continue


        if not check_capacity_feasibility(

            routes,

            demands,

            capacities

        ):

            continue


        if not check_customer_coverage(

            routes,

            customer_ids

        ):

            continue


        value = evaluate_routes(

            routes,

            time_matrix,

            distance_matrix,

            demands

        )


        if math.isfinite(value):

            return (
                permutation,
                routes,
                value
            )


    return (
        None,
        None,
        float("inf")
    )


# =========================================================
# QPSO OPTIMIZATION
# =========================================================

def qpso_optimize(
    customer_ids,
    demands,
    vehicle_ids,
    capacities,
    time_matrix,
    distance_matrix
):

    number_of_customers = len(
        customer_ids
    )


    if number_of_customers == 0:

        return (
            np.array([]),
            {
                vehicle_id: [
                    "Depot",
                    "Depot"
                ]

                for vehicle_id in vehicle_ids
            }
        )


    # -----------------------------------------------------
    # Normalize matrix labels
    # -----------------------------------------------------

    time_matrix = time_matrix.copy()

    distance_matrix = distance_matrix.copy()


    time_matrix.index = (
        time_matrix.index.astype(str)
    )

    time_matrix.columns = (
        time_matrix.columns.astype(str)
    )

    distance_matrix.index = (
        distance_matrix.index.astype(str)
    )

    distance_matrix.columns = (
        distance_matrix.columns.astype(str)
    )


    # =====================================================
    # INITIALIZE SWARM
    # =====================================================

    particles = initialize_swarm(

        NUM_PARTICLES,

        number_of_customers

    )


    # -----------------------------------------------------
    # Personal best
    # -----------------------------------------------------

    personal_best_positions = (
        particles.copy()
    )


    personal_best_values = np.full(

        NUM_PARTICLES,

        float("inf")

    )


    # -----------------------------------------------------
    # Global best
    # -----------------------------------------------------

    global_best_position = None

    global_best_value = float("inf")

    global_best_routes = None


    # =====================================================
    # FORCE AT LEAST ONE FEASIBLE STARTING SOLUTION
    # =====================================================

    (
        feasible_permutation,
        feasible_routes,
        feasible_value
    ) = create_feasible_particle(

        customer_ids,

        demands,

        vehicle_ids,

        capacities,

        time_matrix,

        distance_matrix

    )


    if feasible_routes is not None:

        # Create a position whose sorted order equals
        # the feasible permutation.

        customer_to_rank = {

            customer: index

            for index, customer
            in enumerate(
                feasible_permutation
            )

        }


        feasible_position = np.array([

            (
                customer_to_rank[customer]
                +
                0.5
            )
            /
            number_of_customers

            for customer in customer_ids

        ])


        feasible_position += (
            np.random.uniform(
                -0.001,
                0.001,
                number_of_customers
            )
        )


        feasible_position = np.clip(

            feasible_position,

            0,

            1

        )


        particles[0] = (
            feasible_position
        )


        personal_best_positions[0] = (
            feasible_position.copy()
        )


        personal_best_values[0] = (
            feasible_value
        )


        global_best_position = (
            feasible_position.copy()
        )


        global_best_value = (
            feasible_value
        )


        global_best_routes = (
            copy.deepcopy(
                feasible_routes
            )
        )


    # =====================================================
    # INITIAL POPULATION EVALUATION
    # =====================================================

    for i in range(
        NUM_PARTICLES
    ):

        permutation = (
            position_to_permutation(

                particles[i],

                customer_ids

            )
        )


        routes = permutation_to_routes(

            permutation,

            demands,

            vehicle_ids,

            capacities

        )


        if routes is None:

            continue


        if not check_capacity_feasibility(

            routes,

            demands,

            capacities

        ):

            continue


        if not check_customer_coverage(

            routes,

            customer_ids

        ):

            continue


        value = evaluate_routes(

            routes,

            time_matrix,

            distance_matrix,

            demands

        )


        if not math.isfinite(value):

            continue


        personal_best_values[i] = value


        personal_best_positions[i] = (
            particles[i].copy()
        )


        if value < global_best_value:

            global_best_value = value

            global_best_position = (
                particles[i].copy()
            )

            global_best_routes = (
                copy.deepcopy(
                    routes
                )
            )


    # =====================================================
    # FEASIBILITY CHECK
    # =====================================================

    if global_best_routes is None:

        print(
            "\nERROR: No feasible QPSO solution found."
        )

        print(
            "Check that all required route matrix "
            "entries are finite."
        )

        return (
            None,
            None
        )


    # =====================================================
    # QPSO ITERATIONS
    # =====================================================

    print(
        "\nStarting QPSO optimization..."
    )

    print(
        f"Particles: {NUM_PARTICLES}"
    )

    print(
        f"Iterations: {MAX_ITERATIONS}"
    )


    for iteration in range(
        MAX_ITERATIONS
    ):

        # -------------------------------------------------
        # Alpha
        # -------------------------------------------------

        progress = (
            iteration
            /
            MAX_ITERATIONS
        )


        alpha = (

            ALPHA_START

            -

            (
                ALPHA_START
                -
                ALPHA_END
            )

            *

            progress

        )


        # -------------------------------------------------
        # Mean best position
        # -------------------------------------------------

        mbest = np.mean(

            personal_best_positions,

            axis=0

        )


        # -------------------------------------------------
        # Update particles
        # -------------------------------------------------

        for i in range(
            NUM_PARTICLES
        ):

            # ---------------------------------------------
            # Random attractor
            # ---------------------------------------------

            phi = np.random.uniform(

                0,

                1,

                number_of_customers

            )


            attractor = (

                phi

                *

                personal_best_positions[i]

                +

                (
                    1 - phi
                )

                *

                global_best_position

            )


            # ---------------------------------------------
            # Random number
            # ---------------------------------------------

            u = np.random.uniform(

                0.000001,

                0.999999,

                number_of_customers

            )


            # ---------------------------------------------
            # Direction
            # ---------------------------------------------

            direction = np.where(

                np.random.random(
                    number_of_customers
                ) < 0.5,

                -1,

                1

            )


            # ---------------------------------------------
            # Distance from mbest
            # ---------------------------------------------

            distance_from_mbest = np.abs(

                mbest

                -

                particles[i]

            )


            # ---------------------------------------------
            # QPSO update
            # ---------------------------------------------

            particles[i] = (

                attractor

                +

                direction

                *

                alpha

                *

                distance_from_mbest

                *

                np.log(
                    1 / u
                )

            )


            # ---------------------------------------------
            # Keep numerical values bounded
            # ---------------------------------------------

            particles[i] = np.clip(

                particles[i],

                -5,

                5

            )


            # ---------------------------------------------
            # Decode
            # ---------------------------------------------

            permutation = (
                position_to_permutation(

                    particles[i],

                    customer_ids

                )
            )


            routes = (
                permutation_to_routes(

                    permutation,

                    demands,

                    vehicle_ids,

                    capacities

                )
            )


            if routes is None:

                continue


            if not check_capacity_feasibility(

                routes,

                demands,

                capacities

            ):

                continue


            if not check_customer_coverage(

                routes,

                customer_ids

            ):

                continue


            # ---------------------------------------------
            # Evaluate
            # ---------------------------------------------

            value = evaluate_routes(

                routes,

                time_matrix,

                distance_matrix,

                demands

            )


            if not math.isfinite(value):

                continue


            # ---------------------------------------------
            # Personal best
            # ---------------------------------------------

            if value < personal_best_values[i]:

                personal_best_values[i] = value

                personal_best_positions[i] = (
                    particles[i].copy()
                )


            # ---------------------------------------------
            # Global best
            # ---------------------------------------------

            if value < global_best_value:

                global_best_value = value

                global_best_position = (
                    particles[i].copy()
                )

                global_best_routes = (
                    copy.deepcopy(
                        routes
                    )
                )


        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        if (

            iteration == 0

            or

            (iteration + 1) % 10 == 0

        ):

            print(

                f"Iteration "
                f"{iteration + 1:3d}/"
                f"{MAX_ITERATIONS} "
                f"| Best time: "
                f"{global_best_value:.2f} min"

            )


    # =====================================================
    # FINAL VALIDATION
    # =====================================================

    if not check_capacity_feasibility(

        global_best_routes,

        demands,

        capacities

    ):

        print(
            "\nERROR: Final solution violates capacity."
        )

        return (
            None,
            None
        )


    if not check_customer_coverage(

        global_best_routes,

        customer_ids

    ):

        print(
            "\nERROR: Final solution does not contain "
            "all customers exactly once."
        )

        return (
            None,
            None
        )


    # =====================================================
    # RETURN
    # =====================================================

    return (

        global_best_position,

        global_best_routes

    )


# =========================================================
# PRINT RESULTS
# =========================================================

def print_results(
    routes,
    details
):

    print("\n")

    print(
        "=" * 65
    )

    print(
        "QPSO OPTIMIZED SOLUTION"
    )

    print(
        "=" * 65
    )


    print(

        f"\nTotal travel time: "
        f"{details['total_time']:.2f} minutes"

    )


    print(

        f"Total distance: "
        f"{details['total_distance']:.2f} km"

    )


    print(
        "\nVehicle routes:"
    )

    print(
        "-" * 65
    )


    for vehicle in details[
        "vehicles"
    ]:

        route_text = " → ".join(

            vehicle[
                "route"
            ]

        )


        print(
            f"\n{vehicle['vehicle']}"
        )


        print(
            f"Route: {route_text}"
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
# MAIN
# =========================================================

def main():

    random.seed(
        RANDOM_SEED
    )

    np.random.seed(
        RANDOM_SEED
    )


    print(
        "Loading optimization data..."
    )


    (
        customers,
        vehicles,
        distance_matrix,
        time_matrix
    ) = load_problem()


    (
        customer_ids,
        demands
    ) = get_customer_data(
        customers
    )


    (
        vehicle_ids,
        capacities
    ) = get_vehicle_data(
        vehicles
    )


    print(
        f"\nCustomers: "
        f"{len(customer_ids)}"
    )


    print(
        f"Vehicles: "
        f"{len(vehicle_ids)}"
    )


    (
        best_position,
        best_routes
    ) = qpso_optimize(

        customer_ids,

        demands,

        vehicle_ids,

        capacities,

        time_matrix,

        distance_matrix

    )


    if best_routes is None:

        print(
            "\n❌ QPSO failed to find "
            "a feasible solution."
        )

        return


    details = calculate_solution_details(

        best_routes,

        time_matrix,

        distance_matrix,

        demands,

        capacities

    )


    print_results(

        best_routes,

        details

    )


    print("\n")

    print(
        "=" * 65
    )

    print(
        "QPSO optimization completed!"
    )

    print(
        "=" * 65
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":

    main()