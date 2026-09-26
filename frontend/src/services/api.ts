/**
 * Q-ROUTE AI - API Service Layer
 * 
 * Cleanly separates UI components from backend communication.
 * When the Python FastAPI service is running, toggle USE_MOCK to false
 * or set VITE_API_BASE_URL in your environment.
 */

import {
  ScenarioState,
  VehicleRoute,
  BenchmarkData,
  OptimizationMetrics
} from '../types';

import {
  INITIAL_SCENARIO_STATE,
  INCIDENT_ROAD_DATA,
  INCIDENT_METRICS,
  REOPTIMIZED_METRICS,
  REOPTIMIZED_VEHICLES,
  BENCHMARK_DATA,
  INITIAL_VEHICLES
} from './mockData';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';
const USE_MOCK = true; // Set to false when connecting to live Python FastAPI service

// Helper to simulate realistic async network latency for prototype feel
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Fetch initial scenario state (depot, customers, routes, metrics)
 */
export async function getScenario(): Promise<ScenarioState> {
  if (!USE_MOCK) {
    const res = await fetch(`${API_BASE_URL}/scenario`);
    if (!res.ok) throw new Error(`Failed to fetch scenario: ${res.statusText}`);
    return res.json();
  }

  await delay(150);
  return structuredClone(INITIAL_SCENARIO_STATE);
}

/**
 * Simulate dynamic traffic disruption / road incident
 */
export async function simulateTrafficIncident(): Promise<{
  status: 'INCIDENT';
  traffic_level: 'Heavy Congestion';
  active_incidents: number;
  incident_details: typeof INCIDENT_ROAD_DATA;
  metrics: OptimizationMetrics;
}> {
  if (!USE_MOCK) {
    const res = await fetch(`${API_BASE_URL}/incident/simulate`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`Failed to trigger traffic incident: ${res.statusText}`);
    return res.json();
  }

  await delay(400);
  return {
    status: 'INCIDENT',
    traffic_level: 'Heavy Congestion',
    active_incidents: 1,
    incident_details: INCIDENT_ROAD_DATA,
    metrics: INCIDENT_METRICS
  };
}

/**
 * Trigger QPSO route re-optimization with discrete CVRP constraints
 */
export async function optimizeRoutes(): Promise<{
  status: 'NORMAL';
  traffic_level: 'Low';
  active_incidents: number;
  metrics: OptimizationMetrics;
  vehicles: Record<string, VehicleRoute>;
  message: string;
}> {
  if (!USE_MOCK) {
    const res = await fetch(`${API_BASE_URL}/optimize`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`Optimization failed: ${res.statusText}`);
    return res.json();
  }

  // Latency is simulated progressively in UI for engineering demonstration
  return {
    status: 'NORMAL',
    traffic_level: 'Low',
    active_incidents: 0,
    metrics: REOPTIMIZED_METRICS,
    vehicles: REOPTIMIZED_VEHICLES,
    message: "Routes successfully re-optimized with Quantum Particle Swarm Optimization."
  };
}

/**
 * Fetch algorithm benchmark results (Baseline Greedy vs QPSO)
 */
export async function getBenchmark(): Promise<BenchmarkData> {
  if (!USE_MOCK) {
    const res = await fetch(`${API_BASE_URL}/benchmark`);
    if (!res.ok) throw new Error(`Failed to fetch benchmark: ${res.statusText}`);
    return res.json();
  }

  await delay(100);
  return BENCHMARK_DATA;
}

/**
 * Get detailed telemetry and geometry for a specific vehicle
 */
export async function getRouteDetails(vehicleId: string): Promise<VehicleRoute | null> {
  if (!USE_MOCK) {
    const res = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}/route`);
    if (!res.ok) throw new Error(`Failed to fetch vehicle route: ${res.statusText}`);
    return res.json();
  }

  await delay(50);
  return INITIAL_VEHICLES[vehicleId] || null;
}
