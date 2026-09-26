# NexQRoute

### Quantum-Inspired Intelligent Traffic Route Optimization

NexQRoute is a traffic-aware vehicle routing system that uses **Hybrid Quantum Particle Swarm Optimization (QPSO)** to optimize vehicle routes under dynamic traffic conditions.

## Problem

Urban transportation networks face traffic congestion, inefficient route planning, and high operational costs. Traditional routing approaches can struggle with complex Vehicle Routing Problems (VRP), especially when traffic conditions change dynamically.

## Proposed Solution

NexQRoute models the transportation network as a **dynamic weighted road graph** and combines:

- Traffic and road-network data
- Traffic prediction
- Vehicle-Constrained VRP
- Hybrid QPSO optimization
- Local search
- Dijkstra / A* road-level routing
- Dynamic re-routing
- Route visualization and benchmarking

## Methodology

```text
Traffic & Road Data
        ↓
Traffic Prediction
        ↓
Dynamic Weighted Road Graph
        ↓
Vehicle-Constrained VRP
        ↓
Hybrid QPSO + Local Search
        ↓
Dijkstra / A* Routing
        ↓
Dynamic Re-Routing
        ↓
Dashboard & Evaluation
