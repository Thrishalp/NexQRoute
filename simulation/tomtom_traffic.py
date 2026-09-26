import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")


def get_traffic(lat, lon):
    url = (
        "https://api.tomtom.com/traffic/services/4/"
        "flowSegmentData/absolute/10/json"
    )

    params = {
        "point": f"{lat},{lon}",
        "key": API_KEY
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    flow = response.json()["flowSegmentData"]

    return {
        "current_speed": flow.get("currentSpeed"),
        "free_flow_speed": flow.get("freeFlow"),
        "confidence": flow.get("confidence")
    }


if __name__ == "__main__":
    traffic = get_traffic(17.4401, 78.3489)

    print("========== TOMTOM LIVE TRAFFIC ==========")
    print("Current Speed     :", traffic["current_speed"], "km/h")
    print("Free Flow Speed   :", traffic["free_flow_speed"])
    print("Confidence        :", traffic["confidence"])
    print("=========================================")