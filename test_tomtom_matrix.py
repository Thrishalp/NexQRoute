import pandas as pd
from graph.tomtom_matrix import get_live_route

depot = pd.read_csv("data/depot.csv").iloc[0]
customer = pd.read_csv("data/customers.csv").iloc[0]

result = get_live_route(
    depot["latitude"],
    depot["longitude"],
    customer["latitude"],
    customer["longitude"]
)

print("===== TOMTOM LIVE ROUTE =====")
print("Distance :", round(result["distance_km"], 3), "km")
print("Time     :", round(result["time_min"], 2), "minutes")
print("=============================")