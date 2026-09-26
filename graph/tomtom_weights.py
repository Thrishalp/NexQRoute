import os
import sys
import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.tomtom_traffic import get_traffic


def update_traffic_weights(graph):
    """
    Update road travel-time weights using live TomTom traffic.
    """

    for u, v, key, data in graph.edges(keys=True, data=True):

        # Get midpoint of the road segment
        lat = (graph.nodes[u]["y"] + graph.nodes[v]["y"]) / 2
        lon = (graph.nodes[u]["x"] + graph.nodes[v]["x"]) / 2

        try:
            traffic = get_traffic(lat, lon)
            current_speed = traffic["current_speed"]

            if current_speed and current_speed > 0:
                distance = data.get("length", 0)

                # Travel time in seconds
                data["traffic_time"] = (distance / 1000) / current_speed * 3600

        except Exception:
            # Keep existing value if TomTom has no data
            pass

    return graph