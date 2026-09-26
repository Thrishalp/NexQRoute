import os
import sys

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

import osmnx as ox
import networkx as nx
import pandas as pd


GRAPH_FILE = "data/gachibowli_roads.graphml"
CUSTOMERS_FILE = "data/customers.csv"
DEPOT_FILE = "data/depot.csv"

DISTANCE_OUTPUT = "data/distance_matrix.csv"
TIME_OUTPUT = "data/travel_time_matrix.csv"


def load_data():
    print("Loading road network...")

    G = ox.load_graphml(GRAPH_FILE)

    customers = pd.read_csv(CUSTOMERS_FILE)
    depot = pd.read_csv(DEPOT_FILE)

    return G, customers, depot


def get_locations(customers, depot):
    """
    Create a single list containing:
    Depot + all customers
    """

    locations = []

    # Depot first
    locations.append({
        "id": "Depot",
        "node": int(depot.iloc[0]["node"])
    })

    # Customers
    for _, row in customers.iterrows():

        locations.append({
            "id": row["id"],
            "node": int(row["node"])
        })

    return locations


def calculate_matrices(G, locations):

    n = len(locations)

    distance_matrix = []
    time_matrix = []

    print("\nCalculating road matrices...")

    for i in range(n):

        distance_row = []
        time_row = []

        source = locations[i]["node"]

        # Shortest paths based on physical distance
        distance_paths = nx.single_source_dijkstra_path_length(
            G,
            source,
            weight="length"
        )

        # Shortest paths based on traffic travel time
        time_paths = nx.single_source_dijkstra_path_length(
            G,
            source,
            weight="traffic_time"
        )

        for j in range(n):

            target = locations[j]["node"]

            # Distance in km
            distance = distance_paths.get(
                target,
                float("inf")
            )

            distance_km = distance / 1000

            # Travel time in minutes
            travel_time = time_paths.get(
                target,
                float("inf")
            )

            distance_row.append(distance_km)
            time_row.append(travel_time)

        distance_matrix.append(distance_row)
        time_matrix.append(time_row)

        print(
            f"Processed {i + 1}/{n}"
        )

    return distance_matrix, time_matrix


def save_matrices(
    locations,
    distance_matrix,
    time_matrix
):

    labels = [
        location["id"]
        for location in locations
    ]

    distance_df = pd.DataFrame(
        distance_matrix,
        index=labels,
        columns=labels
    )

    time_df = pd.DataFrame(
        time_matrix,
        index=labels,
        columns=labels
    )

    distance_df.to_csv(
        DISTANCE_OUTPUT
    )

    time_df.to_csv(
        TIME_OUTPUT
    )

    print(
        "\nDistance matrix saved:"
    )

    print(
        DISTANCE_OUTPUT
    )

    print(
        "\nTraffic-aware travel time matrix saved:"
    )

    print(
        TIME_OUTPUT
    )


def main():

    G, customers, depot = load_data()

    locations = get_locations(
        customers,
        depot
    )

    print(
        f"\nTotal locations: {len(locations)}"
    )

    print(
        "Depot +",
        len(customers),
        "customers"
    )

    # -------------------------------------------------
    # Apply traffic conditions
    # -------------------------------------------------

    print(
        "\nApplying traffic conditions..."
    )

    from simulation.traffic import add_traffic_weights

    G = add_traffic_weights(G)

    # -------------------------------------------------
    # Calculate matrices
    # -------------------------------------------------

    distance_matrix, time_matrix = calculate_matrices(
        G,
        locations
    )

    # -------------------------------------------------
    # Save results
    # -------------------------------------------------

    save_matrices(
        locations,
        distance_matrix,
        time_matrix
    )

    print(
        "\nRouting matrix generation completed!"
    )


if __name__ == "__main__":
    main()