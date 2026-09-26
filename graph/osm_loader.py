import osmnx as ox


def load_road_network():
    print("Downloading road network...")

    graph = ox.graph_from_point(
        (17.4401, 78.3489),
        dist=3000,
        network_type="drive"
    )

    print(f"Nodes: {len(graph.nodes)}")
    print(f"Edges: {len(graph.edges)}")

    return graph


def save_road_network(graph):
    ox.save_graphml(graph, "data/gachibowli_roads.graphml")
    print("Road network saved successfully.")


if __name__ == "__main__":
    G = load_road_network()
    save_road_network(G)