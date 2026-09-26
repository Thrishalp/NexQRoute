import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")

BASE_URL = "https://api.tomtom.com/routing/1/calculateRoute"


def get_live_route(origin_lat, origin_lon, dest_lat, dest_lon):
    locations = (
        f"{origin_lat},{origin_lon}:"
        f"{dest_lat},{dest_lon}"
    )

    params = {
        "traffic": "true",
        "travelMode": "car",
        "routeType": "fastest",
        "key": API_KEY
    }

    response = requests.get(
        f"{BASE_URL}/{locations}/json",
        params=params,
        timeout=15
    )

    response.raise_for_status()

    route = response.json()["routes"][0]

    summary = route["summary"]

    return {
        "distance_km": summary["lengthInMeters"] / 1000,
        "time_min": summary["travelTimeInSeconds"] / 60
    }


def get_route_geometry(origin_lat, origin_lon, dest_lat, dest_lon):
    locations = (
        f"{origin_lat},{origin_lon}:"
        f"{dest_lat},{dest_lon}"
    )

    params = {
        "traffic": "true",
        "travelMode": "car",
        "routeType": "fastest",
        "routeRepresentation": "polyline",
        "key": API_KEY
    }

    response = requests.get(
        f"{BASE_URL}/{locations}/json",
        params=params,
        timeout=15
    )

    response.raise_for_status()

    route = response.json()["routes"][0]

    geometry = []

    for leg in route.get("legs", []):
        for point in leg.get("points", []):
            geometry.append([
                point["latitude"],
                point["longitude"]
            ])

    return geometry


def build_live_matrix(locations):

    ids = [str(x["id"]) for x in locations]

    time_matrix = pd.DataFrame(
        0.0,
        index=ids,
        columns=ids
    )

    distance_matrix = pd.DataFrame(
        0.0,
        index=ids,
        columns=ids
    )

    for origin in locations:
        for destination in locations:

            if origin["id"] == destination["id"]:
                continue

            result = get_live_route(
                origin["latitude"],
                origin["longitude"],
                destination["latitude"],
                destination["longitude"]
            )

            time_matrix.loc[
                str(origin["id"]),
                str(destination["id"])
            ] = result["time_min"]

            distance_matrix.loc[
                str(origin["id"]),
                str(destination["id"])
            ] = result["distance_km"]

    return time_matrix, distance_matrix