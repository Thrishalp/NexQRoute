import os
import sys
import time
import random

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
    sys.path.insert(0, PROJECT_ROOT)


# =========================================================
# IMPORT OUR MODULES
# =========================================================

from optimization.vrp import (
    load_problem,
    get_customer_data,
    get_vehicle_data,
    create_baseline_solution,
    evaluate_solution
)

from optimization.qpso import (
    qpso_optimize,
    calculate_solution_details
)


# =========================================================
# MAIN EXPERIMENT
# =========================================================

def main():

    print("\n")
    print("=" * 70)
    print("BASELINE vs QPSO EXPERIMENT")
    print("=" * 70)

    # -----------------------------------------------------
    # Reproducibility
    # -----------------------------------------------------

    random.seed(42)
    np.random.seed(42)

    # -----------------------------------------------------
    # Load data
    # -----------------------------------------------------

    print("\nLoading problem data...")

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

    # =====================================================
    # BASELINE
    # =====================================================

    print("\nCreating baseline solution...")

    baseline_routes = create_baseline_solution(
        customer_ids,
        demands,
        vehicle_ids,
        capacities
    )

    baseline_solution = evaluate_solution(
        baseline_routes,
        demands,
        capacities,
        distance_matrix,
        time_matrix
    )

    baseline_time = float(
        baseline_solution["total_time_min"]
    )

    baseline_distance = float(
        baseline_solution["total_distance_km"]
    )

    # =====================================================
    # QPSO
    # =====================================================

    print("\nRunning QPSO...")

    start_time = time.perf_counter()

    # IMPORTANT:
    # qpso_optimize() returns:
    #
    #     best_position, best_routes
    #
    # The previous code incorrectly treated the first
    # returned value as the route dictionary.

    (
        best_position,
        qpso_routes
    ) = qpso_optimize(
        customer_ids,
        demands,
        vehicle_ids,
        capacities,
        time_matrix,
        distance_matrix
    )

    end_time = time.perf_counter()

    qpso_computation_time = (
        end_time - start_time
    )

    # -----------------------------------------------------
    # Safety check
    # -----------------------------------------------------

    if qpso_routes is None:

        raise RuntimeError(
            "QPSO did not return a valid route solution."
        )

    if not isinstance(qpso_routes, dict):

        raise TypeError(
            "QPSO returned an unexpected route format. "
            f"Expected dict, got {type(qpso_routes)}"
        )

    # =====================================================
    # CALCULATE QPSO DETAILS
    # =====================================================

    qpso_details = calculate_solution_details(
        qpso_routes,
        time_matrix,
        distance_matrix,
        demands,
        capacities
    )

    if qpso_details is None:

        raise RuntimeError(
            "Could not calculate QPSO solution details."
        )

    qpso_time = float(
        qpso_details["total_time"]
    )

    qpso_distance = float(
        qpso_details["total_distance"]
    )

    # =====================================================
    # IMPROVEMENTS
    # =====================================================

    if baseline_time > 0:

        time_improvement = (
            (baseline_time - qpso_time)
            / baseline_time
            * 100
        )

    else:

        time_improvement = 0.0


    if baseline_distance > 0:

        distance_improvement = (
            (baseline_distance - qpso_distance)
            / baseline_distance
            * 100
        )

    else:

        distance_improvement = 0.0

    # =====================================================
    # RESULTS
    # =====================================================

    print("\n")
    print("=" * 70)
    print("EXPERIMENT RESULTS")
    print("=" * 70)

    print(
        f"\n{'Metric':<25}"
        f"{'Baseline':>15}"
        f"{'QPSO':>15}"
    )

    print("-" * 70)

    print(
        f"{'Travel Time (min)':<25}"
        f"{baseline_time:>15.2f}"
        f"{qpso_time:>15.2f}"
    )

    print(
        f"{'Distance (km)':<25}"
        f"{baseline_distance:>15.2f}"
        f"{qpso_distance:>15.2f}"
    )

    print("-" * 70)

    print(
        f"\nTravel-time improvement: "
        f"{time_improvement:.2f}%"
    )

    print(
        f"Distance improvement: "
        f"{distance_improvement:.2f}%"
    )

    print(
        f"QPSO computation time: "
        f"{qpso_computation_time:.3f} seconds"
    )

    # =====================================================
    # BASELINE ROUTES
    # =====================================================

    print("\n")
    print("=" * 70)
    print("BASELINE ROUTES")
    print("=" * 70)

    for vehicle_id, route in baseline_routes.items():

        print(
            f"{vehicle_id}: "
            + " → ".join(route)
        )

    # =====================================================
    # QPSO ROUTES
    # =====================================================

    print("\n")
    print("=" * 70)
    print("QPSO ROUTES")
    print("=" * 70)

    for vehicle in qpso_details["vehicles"]:

        print(
            f"{vehicle['vehicle']}: "
            + " → ".join(
                vehicle["route"]
            )
        )

    # =====================================================
    # SAVE RESULTS
    # =====================================================

    results_directory = os.path.join(
        PROJECT_ROOT,
        "results"
    )

    os.makedirs(
        results_directory,
        exist_ok=True
    )

    results_df = pd.DataFrame({

        "Metric": [
            "Travel Time (minutes)",
            "Distance (km)",
            "Improvement (%)"
        ],

        "Baseline": [
            baseline_time,
            baseline_distance,
            0.0
        ],

        "QPSO": [
            qpso_time,
            qpso_distance,
            time_improvement
        ]

    })

    results_file = os.path.join(
        results_directory,
        "baseline_vs_qpso.csv"
    )

    results_df.to_csv(
        results_file,
        index=False
    )

    print("\nResults saved to:")

    print(results_file)

    print("\n")
    print("=" * 70)
    print("EXPERIMENT COMPLETED")
    print("=" * 70)


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    main()