import os
import random
import osmnx as ox


TRAFFIC_FACTORS = {
    "normal": 1.0,
    "moderate": 1.4,
    "heavy": 2.0,
    "severe": 3.0
}


def add_traffic_weights(G, traffic_distribution=None):
    """
    Apply traffic conditions to every road in the graph.

    Each road receives a traffic level:
        normal   -> 1.0
        moderate -> 1.4
        heavy    -> 2.0
        severe   -> 3.0

    Travel time is calculated using:
        average speed = 30 km/h
    """

    if traffic_distribution is None:

        traffic_distribution = {
            "normal": 0.50,
            "moderate": 0.25,
            "heavy": 0.15,
            "severe": 0.10
        }

    traffic_levels = list(traffic_distribution.keys())
    probabilities = list(traffic_distribution.values())

    for u, v, key, data in G.edges(keys=True, data=True):

        length = float(data.get("length", 0))

        # Base travel time assuming 30 km/h
        base_time = (length / 1000) / 30 * 60

        # Random traffic condition for this road
        traffic_level = random.choices(
            traffic_levels,
            weights=probabilities,
            k=1
        )[0]

        factor = TRAFFIC_FACTORS[traffic_level]

        # Traffic-adjusted travel time
        traffic_time = base_time * factor

        data["base_time"] = base_time
        data["traffic_time"] = traffic_time
        data["traffic_level"] = traffic_level
        data["traffic_factor"] = factor

    return G


def traffic_summary(G):
    """
    Count how many roads belong to each traffic category.
    """

    summary = {
        "normal": 0,
        "moderate": 0,
        "heavy": 0,
        "severe": 0
    }

    for u, v, key, data in G.edges(keys=True, data=True):

        level = data.get("traffic_level", "normal")

        if level in summary:
            summary[level] += 1

    return summary


def simulate_traffic_change(G, number_of_roads=20):
    """
    Simulate a traffic incident.

    A number of random roads are selected and their
    traffic condition is changed.

    This represents a new traffic event such as:
        accident
        congestion
        road blockage
        sudden traffic increase
    """

    edges = list(G.edges(keys=True))

    selected_edges = random.sample(
        edges,
        min(number_of_roads, len(edges))
    )

    for u, v, key in selected_edges:

        data = G[u][v][key]

        current_level = data.get(
            "traffic_level",
            "normal"
        )

        # Increase traffic severity
        if current_level == "normal":
            new_level = "moderate"

        elif current_level == "moderate":
            new_level = "heavy"

        elif current_level == "heavy":
            new_level = "severe"

        else:
            new_level = "severe"

        factor = TRAFFIC_FACTORS[new_level]

        base_time = float(
            data.get("base_time", 0)
        )

        traffic_time = base_time * factor

        data["traffic_level"] = new_level
        data["traffic_factor"] = factor
        data["traffic_time"] = traffic_time

    return G


def print_traffic_summary(G):

    summary = traffic_summary(G)

    print("\nTraffic distribution:")

    for level, count in summary.items():

        print(
            f"{level.capitalize():10s}: {count} roads"
        )


if __name__ == "__main__":

    print("Loading road network...")

    G = ox.load_graphml(
        "data/gachibowli_roads.graphml"
    )

    print("Applying initial traffic conditions...")

    G = add_traffic_weights(G)

    print_traffic_summary(G)

    print("\nExample roads:")

    edges = list(
        G.edges(data=True, keys=True)
    )

    for i, (u, v, key, data) in enumerate(edges[:5]):

        print(
            f"\nRoad {i + 1}"
        )

        print(
            "Distance:",
            round(
                float(data["length"]),
                2
            ),
            "meters"
        )

        print(
            "Traffic:",
            data["traffic_level"]
        )

        print(
            "Base time:",
            round(
                data["base_time"],
                3
            ),
            "minutes"
        )

        print(
            "Traffic time:",
            round(
                data["traffic_time"],
                3
            ),
            "minutes"
        )

    print("\nSimulating traffic incident...")

    G = simulate_traffic_change(
        G,
        number_of_roads=20
    )

    print_traffic_summary(G)

    print(
        "\nDynamic traffic simulation completed!"
    )