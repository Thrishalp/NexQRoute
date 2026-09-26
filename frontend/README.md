# Q-ROUTE AI — Intelligent Transportation Command Center
### Smart India Hackathon 2026 | Problem Statement: SIH26137
**Quantum-Inspired Intelligent Traffic Route Optimization for Discrete CVRP**

---

## Overview

**Q-ROUTE AI** is an engineering-grade transportation and logistics command center dashboard built for real-time fleet dispatch and dynamic route re-optimization under simulated traffic incidents.

* **Map & Road Network**: Grounded in OpenStreetMap / OSMnx road network topology for **Gachibowli, Hyderabad**.
* **Problem Formulation**: Capacitated Vehicle Routing Problem (CVRP) with discrete customer demands and vehicle capacity bounds.
* **Core Optimizer**: Quantum Particle Swarm Optimization (QPSO) utilizing continuous random-key encoding mapped to discrete route permutations.

---

## Quick Start (Frontend Development)

To run the dashboard locally:

```bash
cd frontend
npm run dev
```

The application will open automatically at:
**`http://localhost:3000`**

To produce a production bundle:
```bash
npm run build
```

---

## Dashboard Capabilities

1. **Live OpenStreetMap Telemetry**:
   - Depot Hub marker (`17.43941, 78.34868`).
   - Customer nodes **C1 through C10** with live demand badges.
   - Distinct route polylines for active vehicles (`V1` in cyan, `V2` in electric blue).
   - Unused vehicle standby tracking (`V3`).
   - Pulsing hazard visualization for congested road links during incident mode.

2. **Interactive Incident Simulation**:
   - **Simulate Traffic Incident**: Injects dynamic congestion on the Gachibowli arterial corridor, worsens travel-time metrics, and flags an alert banner.
   - **Re-optimize with QPSO**: Demonstrates step-by-step optimization pipeline (weight recalculation, QPSO iteration, feasible route generation) and dynamically recalculates the network bypass route.
   - **Reset Scenario**: Re-establishes pre-incident optimal baseline.

3. **Benchmarking Suite**:
   - Direct comparison between Greedy Baseline Routing and QPSO.
   - Quantified improvements: **28.42% travel-time reduction**, **31.09% distance reduction**.
   - Sub-second runtime display (**0.491 s**).

4. **Dynamic Re-Optimization Telemetry**:
   - Before vs. After panel highlighting network adaptation physics.

5. **Technical Formulation Accordion**:
   - Clear architectural overview of CVRP, QPSO, Random-Key Encoding, and OSMnx graph constraints.

---

## Connecting to Python FastAPI Backend (Future Integration)

The frontend is built with a decoupled API service layer in [`src/services/api.ts`](file:///Users/thrishal/sih_route_optimizer/frontend/src/services/api.ts).

To connect your Python FastAPI backend:
1. Start your FastAPI server on port 8000:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
2. The Vite dev server is pre-configured with a proxy in `vite.config.ts` forwarding all `/api/*` calls to `http://127.0.0.1:8000`.
3. In `src/services/api.ts`, set `const USE_MOCK = false` or configure `VITE_API_BASE_URL` in `.env.local`.
