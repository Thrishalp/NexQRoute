import osmnx as ox
from graph.tomtom_weights import get_traffic


GRAPH_FILE = "data/gachibowli_roads.graphml"

G = ox.load_graphml(GRAPH_FILE)

# Take one road segment
u, v, key = list(G.edges(keys=True))[0]

lat = (G.nodes[u]["y"] + G.nodes[v]["y"]) / 2
lon = (G.nodes[u]["x"] + G.nodes[v]["x"]) / 2

traffic = get_traffic(lat, lon)

print("===== LIVE ROAD TRAFFIC =====")
print("Road location:", lat, lon)
print("Current speed:", traffic["current_speed"], "km/h")
print("Confidence:", traffic["confidence"])
print("=============================")