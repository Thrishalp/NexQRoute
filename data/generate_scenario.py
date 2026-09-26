import os
import random
import pandas as pd
import osmnx as ox
import networkx as nx


GRAPH_FILE = "data/gachibowli_roads.graphml"

CUSTOMERS_FILE = "data/customers.csv"
DEPOT_FILE = "data/depot.csv"
VEHICLES_FILE = "data/vehicles.csv"


def main():

    print("Loading road network...")

    G = ox.load_graphml(GRAPH_FILE)

    print(
        f"Original graph: {len(G.nodes)} nodes"
    )

    # ---------------------------------------------------------
    # Find largest strongly connected component
    # ---------------------------------------------------------

    print(
        "Finding largest strongly connected road network..."
    )

    components = nx.strongly_connected_components(G)

    largest_component = max(
        components,
        key=len
    )

    G_connected = G.subgraph(
        largest_component
    ).copy()

    print(
        f"Connected graph: {len(G_connected.nodes)} nodes"
    )

    # ---------------------------------------------------------
    # Select depot
    # ---------------------------------------------------------

    center_node = ox.distance.nearest_nodes(
        G_connected,
        X=78.3489,
        Y=17.4401
    )

    # ---------------------------------------------------------
    # Select customers
    # ---------------------------------------------------------

    random.seed(42)

    available_nodes = list(
        G_connected.nodes
    )

    available_nodes.remove(
        center_node
    )

    customer_nodes = random.sample(
        available_nodes,
        10
    )

    # ---------------------------------------------------------
    # Create customers
    # ---------------------------------------------------------

    customers = []

    for i, node in enumerate(
        customer_nodes,
        start=1
    ):

        node_data = G_connected.nodes[node]

        customers.append({
            "id": f"C{i}",
            "node": node,
            "latitude": node_data["y"],
            "longitude": node_data["x"],
            "demand": random.randint(5, 10)
        })

    customers_df = pd.DataFrame(
        customers
    )

    # ---------------------------------------------------------
    # Create depot
    # ---------------------------------------------------------

    depot_data = G_connected.nodes[
        center_node
    ]

    depot_df = pd.DataFrame([
        {
            "node": center_node,
            "latitude": depot_data["y"],
            "longitude": depot_data["x"]
        }
    ])

    # ---------------------------------------------------------
    # Create vehicles
    # ---------------------------------------------------------

    vehicles_df = pd.DataFrame([
        {
            "id": "V1",
            "capacity": 40
        },
        {
            "id": "V2",
            "capacity": 40
        },
        {
            "id": "V3",
            "capacity": 40
        }
    ])

    # ---------------------------------------------------------
    # Check total demand
    # ---------------------------------------------------------

    total_demand = customers_df[
        "demand"
    ].sum()

    total_capacity = vehicles_df[
        "capacity"
    ].sum()

    print(
        f"\nTotal demand: {total_demand}"
    )

    print(
        f"Total capacity: {total_capacity}"
    )

    if total_demand > total_capacity:

        print(
            "Demand exceeds vehicle capacity."
        )

        return

    # ---------------------------------------------------------
    # Save files
    # ---------------------------------------------------------

    customers_df.to_csv(
        CUSTOMERS_FILE,
        index=False
    )

    depot_df.to_csv(
        DEPOT_FILE,
        index=False
    )

    vehicles_df.to_csv(
        VEHICLES_FILE,
        index=False
    )

    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    print(
        "\nScenario generated successfully!"
    )

    print(
        "\nCustomers:"
    )

    print(
        customers_df.to_string(
            index=False
        )
    )

    print(
        "\nVehicles:"
    )

    print(
        vehicles_df.to_string(
            index=False
        )
    )

    print(
        "\nDepot:"
    )

    print(
        depot_df.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()