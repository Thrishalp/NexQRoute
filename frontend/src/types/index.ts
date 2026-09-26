export type LatLng = [number, number];

export interface Customer {
  id: string;
  node: number | string;
  lat: number;
  lng: number;
  demand: number;
}

export interface Depot {
  node: number | string;
  lat: number;
  lng: number;
  name: string;
}

export interface VehicleRoute {
  id: string;
  route: string[];
  distance_km: number;
  travel_time_min: number;
  demand: number;
  capacity: number;
  remaining_capacity: number;
  status: 'active' | 'unused';
  color: string;
  geometry: LatLng[];
}

export interface IncidentRoad {
  id: string;
  name: string;
  geometry: LatLng[];
  severity: 'moderate' | 'severe' | 'critical';
  added_delay_min: number;
  description: string;
}

export type TrafficStatusType = 'NORMAL' | 'INCIDENT';

export interface OptimizationMetrics {
  total_distance_km: number;
  total_time_min: number;
  active_vehicles: number;
  total_vehicles: number;
  customers_served: number;
  total_customers: number;
  runtime_sec: number;
}

export interface BenchmarkData {
  travel_time_baseline_min: number;
  travel_time_qpso_min: number;
  travel_time_improvement_pct: number;
  distance_baseline_km: number;
  distance_qpso_km: number;
  distance_improvement_pct: number;
  runtime_sec: number;
}

export interface ReoptimizationComparison {
  before: {
    distance_km: number;
    travel_time_min: number;
    active_vehicles: number;
  };
  after: {
    distance_km: number;
    travel_time_min: number;
    active_vehicles: number;
  };
  incident_impact: string;
  recovery_action: string;
}

export interface ScenarioState {
  traffic_status: TrafficStatusType;
  traffic_level: 'Low' | 'Moderate' | 'Heavy Congestion';
  active_incidents: number;
  incident_details?: IncidentRoad;
  metrics: OptimizationMetrics;
  vehicles: Record<string, VehicleRoute>;
  depot: Depot;
  customers: Customer[];
  benchmark: BenchmarkData;
  reoptimization: ReoptimizationComparison;
}
