from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import sys
import json
import os

app = FastAPI(title="NexQRoute API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptimizeRequest(BaseModel):
    incident: bool = False

@app.get("/")
def root():
    return {"status": "online", "service": "NexQRoute"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/optimize")
def optimize(payload: dict = Body(default={"incident": False})):
    is_incident = payload.get("incident", False)
    target_module = "simulation.dynamic_reoptimization" if is_incident else "optimization.live_qpso"

    print(f"\n[TRIGGER] Running {target_module} (incident={is_incident})...")

    project_dir = os.path.dirname(os.path.abspath(__file__))

    result = subprocess.run(
        [sys.executable, "-m", target_module],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[ERROR] Subprocess failed:")
        print(result.stderr)

    geometry_file = os.path.join(
        project_dir,
        "results",
        "optimized_route_geometry.json"
    )

    geometry = {}
    if os.path.exists(geometry_file):
        with open(geometry_file, "r") as file:
            try:
                geometry = json.load(file)
            except Exception as e:
                print(f"[ERROR] Failed to load geometry: {e}")

    best_time = None
    distance = None
    routes = {}

    for line in result.stdout.splitlines():
        if "Best time:" in line:
            try:
                best_time = float(line.split("Best time:")[1].split("min")[0].strip())
            except Exception:
                pass
        if "Total distance:" in line:
            try:
                distance = float(line.split("Total distance:")[1].split("km")[0].strip())
            except Exception:
                pass
        if "Routes:" in line:
            try:
                raw_routes = line.split("Routes:")[1].strip()
                routes = eval(raw_routes)
            except Exception:
                pass

    return {
        "success": result.returncode == 0,
        "best_time": best_time,
        "distance": distance,
        "routes": routes,
        "route_geometry": geometry,
        "output": result.stdout,
        "error": result.stderr
    }
@app.post("/api/incident")
def trigger_incident():
    target_module = "simulation.dynamic_reoptimization"
    print(f"\n[TRIGGER] Force running {target_module}...")

    project_dir = os.path.dirname(os.path.abspath(__file__))

    result = subprocess.run(
        [sys.executable, "-m", target_module],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("[ERROR] Incident subprocess failed:")
        print(result.stderr)

    geometry_file = os.path.join(
        project_dir,
        "results",
        "optimized_route_geometry.json"
    )

    geometry = {}
    if os.path.exists(geometry_file):
        with open(geometry_file, "r") as file:
            try:
                geometry = json.load(file)
            except Exception as e:
                print(f"[ERROR] Failed to load geometry: {e}")

    best_time = None
    distance = None
    routes = {}

    for line in result.stdout.splitlines():
        if "Best time:" in line:
            try:
                best_time = float(line.split("Best time:")[1].split("min")[0].strip())
            except Exception:
                pass
        if "Total distance:" in line:
            try:
                distance = float(line.split("Total distance:")[1].split("km")[0].strip())
            except Exception:
                pass
        if "Routes:" in line:
            try:
                raw_routes = line.split("Routes:")[1].strip()
                routes = eval(raw_routes)
            except Exception:
                pass

    return {
        "success": result.returncode == 0,
        "best_time": best_time,
        "distance": distance,
        "routes": routes,
        "route_geometry": geometry,
        "output": result.stdout,
        "error": result.stderr
    }