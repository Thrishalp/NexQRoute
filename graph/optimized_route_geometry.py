import os
import json
import osmnx as ox
import networkx as nx
import pandas as pd
from graph.routing import get_locations

GRAPH_FILE = "data/gachibowli_roads.graphml"
CUSTOMERS_FILE = "data/customers.csv"
DEPOT_FILE = "data/depot.csv"
OUTPUT_FILE = "results/optimized_route_geometry.json"


def generate_and_save_geometry(G, routes, locations, output_file=OUTPUT_FILE):
    """
    Given a network graph G, optimized routes, and location metadata,
    extracts road-following coordinates [lat, lon] for Leaflet and writes to JSON.
    """
    location_nodes = {loc["id"]: loc["node"] for loc in locations}
    route_geometry = {}

    for vehicle_id, route in routes.items():
        if len(route) <= 2 and route[0] == route[-1]:
            route_geometry[vehicle_id] = []
            continue

        vehicle_coords = []

        for i in range(len(route) - 1):
            start_name = route[i]
            end_name = route[i + 1]

            start_node = location_nodes.get(start_name)
            end_node = location_nodes.get(end_name)

            if start_node is None or end_node is None:
                continue

            try:
                weight_prop = "traffic_time" if "traffic_time" in next(iter(G.edges(data=True)))[2] else "length"
                path = nx.shortest_path(G, start_node, end_node, weight=weight_prop)

                for node_idx in range(len(path) - 1):
                    u = path[node_idx]
                    v = path[node_idx + 1]
                    edge_data = G.get_edge_data(u, v)

                    if edge_data and 0 in edge_data and "geometry" in edge_data[0]:
                        coords = list(edge_data[0]["geometry"].coords)
                        vehicle_coords.extend([[lat, lon] for lon, lat in coords])
                    else:
                        node_u = G.nodes[u]
                        node_v = G.nodes[v]
                        vehicle_coords.append([node_u["y"], node_u["x"]])
                        vehicle_coords.append([node_v["y"], node_v["x"]])

            except nx.NetworkXNoPath:
                continue

        deduped_coords = []
        for pt in vehicle_coords:
            if not deduped_coords or deduped_coords[-1] != pt:
                deduped_coords.append(pt)

        route_geometry[vehicle_id] = deduped_coords

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(route_geometry, f, indent=2)

    print(f"Road route geometry successfully saved to: {output_file}")
    return route_geometry


def main():
    pass


if __name__ == "__main__":
    main()