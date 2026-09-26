import {
  Customer,
  Depot,
  VehicleRoute,
  IncidentRoad,
  OptimizationMetrics,
  BenchmarkData,
  ReoptimizationComparison,
  ScenarioState,
  LatLng
} from '../types';

export const DEFAULT_DEPOT: Depot = {
  node: "12632759800",
  lat: 17.43941,
  lng: 78.3486778,
  name: "Gachibowli Central Hub (Depot)"
};

export const DEFAULT_CUSTOMERS: Customer[] = [
  { id: "C1", node: "11486599539", lat: 17.4601382, lng: 78.3643709, demand: 10 },
  { id: "C2", node: "1306433171", lat: 17.430285, lng: 78.3668084, demand: 9 },
  { id: "C3", node: "701228141", lat: 17.4386039, lng: 78.3635185, demand: 5 },
  { id: "C4", node: "2245059806", lat: 17.4278049, lng: 78.3333306, demand: 9 },
  { id: "C5", node: "2231948962", lat: 17.4646394, lng: 78.3406728, demand: 8 },
  { id: "C6", node: "2228836707", lat: 17.4419962, lng: 78.3348248, demand: 5 },
  { id: "C7", node: "1318407376", lat: 17.4179705, lng: 78.368572, demand: 5 },
  { id: "C8", node: "13947454652", lat: 17.4184136, lng: 78.3589012, demand: 5 },
  { id: "C9", node: "1304477087", lat: 17.4420088, lng: 78.3660035, demand: 6 },
  { id: "C10", node: "12042856354", lat: 17.4416898, lng: 78.3555277, demand: 6 }
];

export const V1_GEOMETRY: LatLng[] = [
  [17.43941, 78.3486778], [17.4393574, 78.348655], [17.4393932, 78.3485218], [17.4394483, 78.3485459],
  [17.4447983, 78.3523521], [17.4450138, 78.3527246], [17.4451422, 78.3525755], [17.449126, 78.3484485],
  [17.4568311, 78.3397312], [17.460052, 78.3373754], [17.4601452, 78.3373063], [17.4602031, 78.3373953],
  [17.4621298, 78.3392027], [17.4627051, 78.3401604], [17.463116, 78.3408634], [17.4644179, 78.3413715],
  [17.4646394, 78.3406728], [17.4648062, 78.341573], [17.465296, 78.3417333], [17.4657186, 78.3417807],
  [17.4655491, 78.342777], [17.465366, 78.3434946], [17.4649125, 78.3444581], [17.4643337, 78.3454646],
  [17.4635018, 78.3472576], [17.462615, 78.3497282], [17.4622759, 78.3506108], [17.46179, 78.3517179],
  [17.4613309, 78.3526167], [17.4602172, 78.3546518], [17.4597488, 78.3556843], [17.4570904, 78.3606719],
  [17.4564884, 78.3618617], [17.4555611, 78.363879], [17.4565172, 78.3644942], [17.4573994, 78.3650176],
  [17.4583296, 78.3658518], [17.4591445, 78.3650624], [17.4598072, 78.3647758], [17.4601382, 78.3643709],
  [17.4596475, 78.3647753], [17.45903, 78.3662579], [17.4576552, 78.3655496], [17.4567686, 78.3649363],
  [17.4554207, 78.3641363], [17.4528318, 78.363766], [17.4515368, 78.3637295], [17.4506454, 78.3638072],
  [17.4496425, 78.3639678], [17.4488961, 78.3638063], [17.4482386, 78.36367], [17.4472041, 78.3635718],
  [17.445281, 78.3632201], [17.4442201, 78.363023], [17.443149, 78.3628219], [17.4423479, 78.3644803],
  [17.4418141, 78.3653634], [17.4420088, 78.3660035], [17.4414195, 78.3651327], [17.4407781, 78.3644267],
  [17.439997, 78.3641348], [17.4396619, 78.3636719], [17.4387582, 78.3639378], [17.4386039, 78.3635185],
  [17.4388291, 78.363255], [17.4396268, 78.3621097], [17.4405117, 78.3608161], [17.441194, 78.3597407],
  [17.4398939, 78.3594291], [17.4403035, 78.3582037], [17.4416898, 78.3555277], [17.4421809, 78.3546196],
  [17.4429435, 78.3541676], [17.4435526, 78.3545414], [17.4442333, 78.3537191], [17.444938, 78.3528134],
  [17.43941, 78.3486778]
];

export const V2_GEOMETRY: LatLng[] = [
  [17.43941, 78.3486778], [17.4393932, 78.3485218], [17.4447983, 78.3523521], [17.4450163, 78.352915],
  [17.4437963, 78.3544573], [17.4428302, 78.3564497], [17.4418481, 78.3587181], [17.4405919, 78.3609308],
  [17.4400177, 78.3619754], [17.4391297, 78.363336], [17.4387582, 78.3639378], [17.4381994, 78.3646082],
  [17.4371336, 78.3659181], [17.4358505, 78.3673717], [17.4345081, 78.368648], [17.4332862, 78.3697978],
  [17.4319275, 78.3713167], [17.4309535, 78.372813], [17.4300212, 78.3738525], [17.4304381, 78.3730265],
  [17.4316747, 78.3714338], [17.4328996, 78.3699713], [17.43256, 78.3687532], [17.4311828, 78.3674623],
  [17.430285, 78.3668084], [17.4310381, 78.3662005], [17.4324615, 78.3673184], [17.4329827, 78.3665987],
  [17.4338597, 78.3661085], [17.4343799, 78.3653846], [17.4352766, 78.3660088], [17.4375345, 78.364987],
  [17.4384444, 78.3637953], [17.43823, 78.363576], [17.4348589, 78.3613566], [17.4329329, 78.3602375],
  [17.4232496, 78.3575154], [17.4188576, 78.3582967], [17.4184017, 78.3608403], [17.4182722, 78.3620445],
  [17.4180491, 78.364946], [17.4180039, 78.3670755], [17.4179705, 78.368572], [17.4178764, 78.3682243],
  [17.4178981, 78.366988], [17.4179028, 78.3655745], [17.4178292, 78.3640929], [17.41808, 78.3622698],
  [17.4181752, 78.3594708], [17.4184136, 78.3589012], [17.4185288, 78.3579445], [17.4191784, 78.3553468],
  [17.4192601, 78.3549187], [17.4195372, 78.3537768], [17.4196491, 78.353101], [17.4197859, 78.3525225],
  [17.420234, 78.3506331], [17.4203898, 78.3500431], [17.4206432, 78.3495603], [17.4223885, 78.3500669],
  [17.4229697, 78.3487444], [17.4233063, 78.3472596], [17.4257909, 78.3410623], [17.4256813, 78.3403723],
  [17.4267898, 78.3355912], [17.4269959, 78.3339276], [17.4278049, 78.3333306], [17.4281968, 78.3327125],
  [17.4288195, 78.3326224], [17.429558, 78.3326457], [17.4310019, 78.3333331], [17.4325143, 78.3340032],
  [17.4330708, 78.3342469], [17.4345912, 78.334944], [17.4356718, 78.334423], [17.4362015, 78.3345921],
  [17.4368859, 78.3339435], [17.4371122, 78.3331775], [17.4375888, 78.3329335], [17.4378144, 78.3321646],
  [17.438002, 78.3317335], [17.4394219, 78.3321899], [17.4397686, 78.3323063], [17.4407591, 78.332627],
  [17.4414218, 78.3328328], [17.4416916, 78.333399], [17.4414426, 78.3342051], [17.4416015, 78.334701],
  [17.4419962, 78.3348248], [17.4409429, 78.334625], [17.4408238, 78.3335292], [17.4398293, 78.3323908],
  [17.4382763, 78.3480225], [17.4393932, 78.3485218], [17.43941, 78.3486778]
];

// Incident location on the arterial segment near C1 / C9 link
export const INCIDENT_ROAD_DATA: IncidentRoad = {
  id: "INCIDENT_GACHIBOWLI_01",
  name: "Gachibowli-Miyapur Corridor (Near C1/C9 Junction)",
  geometry: [
    [17.4570904, 78.3606719],
    [17.4564884, 78.3618617],
    [17.4555611, 78.363879],
    [17.4528318, 78.363766],
    [17.4496425, 78.3639678]
  ],
  severity: "critical",
  added_delay_min: 15.2,
  description: "Major waterlogging & multi-vehicle bottleneck on arterial link"
};

// Re-optimized bypass route geometry for V1 after incident
export const V1_REOPTIMIZED_GEOMETRY: LatLng[] = [
  [17.43941, 78.3486778], [17.4394483, 78.3485459], [17.4447983, 78.3523521], [17.449126, 78.3484485],
  [17.4568311, 78.3397312], [17.4621298, 78.3392027], [17.4646394, 78.3406728], [17.465296, 78.3417333],
  [17.4649125, 78.3444581], [17.4635018, 78.3472576], [17.4601382, 78.3643709],
  // Bypass detour path avoiding 17.45709 corridor via western bypass
  [17.4598072, 78.3647758], [17.456094, 78.364551], [17.4488961, 78.3638063], [17.4442201, 78.363023],
  [17.4420088, 78.3660035], [17.4386039, 78.3635185], [17.4405117, 78.3608161], [17.4416898, 78.3555277],
  [17.4442333, 78.3537191], [17.43941, 78.3486778]
];

export const INITIAL_VEHICLES: Record<string, VehicleRoute> = {
  V1: {
    id: "V1",
    route: ["Depot", "C5", "C1", "C9", "C3", "C10", "Depot"],
    distance_km: 13.04,
    travel_time_min: 35.25,
    demand: 35.0,
    capacity: 40.0,
    remaining_capacity: 5.0,
    status: "active",
    color: "#06b6d4", // Cyan
    geometry: V1_GEOMETRY
  },
  V2: {
    id: "V2",
    route: ["Depot", "C2", "C7", "C8", "C4", "C6", "Depot"],
    distance_km: 18.13,
    travel_time_min: 48.24,
    demand: 33.0,
    capacity: 40.0,
    remaining_capacity: 7.0,
    status: "active",
    color: "#3b82f6", // Blue
    geometry: V2_GEOMETRY
  },
  V3: {
    id: "V3",
    route: ["Depot"],
    distance_km: 0.0,
    travel_time_min: 0.0,
    demand: 0.0,
    capacity: 40.0,
    remaining_capacity: 40.0,
    status: "unused",
    color: "#64748b", // Slate
    geometry: [[17.43941, 78.3486778]]
  }
};

export const REOPTIMIZED_VEHICLES: Record<string, VehicleRoute> = {
  V1: {
    id: "V1",
    route: ["Depot", "C5", "C1", "C10", "C9", "C3", "Depot"],
    distance_km: 15.42,
    travel_time_min: 41.80,
    demand: 35.0,
    capacity: 40.0,
    remaining_capacity: 5.0,
    status: "active",
    color: "#06b6d4",
    geometry: V1_REOPTIMIZED_GEOMETRY
  },
  V2: {
    id: "V2",
    route: ["Depot", "C2", "C7", "C8", "C4", "C6", "Depot"],
    distance_km: 18.13,
    travel_time_min: 48.24,
    demand: 33.0,
    capacity: 40.0,
    remaining_capacity: 7.0,
    status: "active",
    color: "#3b82f6",
    geometry: V2_GEOMETRY
  },
  V3: {
    id: "V3",
    route: ["Depot"],
    distance_km: 0.0,
    travel_time_min: 0.0,
    demand: 0.0,
    capacity: 40.0,
    remaining_capacity: 40.0,
    status: "unused",
    color: "#64748b",
    geometry: [[17.43941, 78.3486778]]
  }
};

export const INITIAL_METRICS: OptimizationMetrics = {
  total_distance_km: 31.16,
  total_time_min: 83.48,
  active_vehicles: 2,
  total_vehicles: 3,
  customers_served: 10,
  total_customers: 10,
  runtime_sec: 0.491
};

export const INCIDENT_METRICS: OptimizationMetrics = {
  total_distance_km: 31.16,
  total_time_min: 98.68, // Worsened due to corridor blockage
  active_vehicles: 2,
  total_vehicles: 3,
  customers_served: 10,
  total_customers: 10,
  runtime_sec: 0.491
};

export const REOPTIMIZED_METRICS: OptimizationMetrics = {
  total_distance_km: 33.55, // Slightly higher distance due to bypass detour
  total_time_min: 90.04,    // Faster than sitting in the 98+ min traffic jam
  active_vehicles: 2,
  total_vehicles: 3,
  customers_served: 10,
  total_customers: 10,
  runtime_sec: 0.512
};

export const BENCHMARK_DATA: BenchmarkData = {
  travel_time_baseline_min: 116.63,
  travel_time_qpso_min: 83.48,
  travel_time_improvement_pct: 28.42,
  distance_baseline_km: 45.22,
  distance_qpso_km: 31.16,
  distance_improvement_pct: 31.09,
  runtime_sec: 0.491
};

export const REOPTIMIZATION_COMPARISON: ReoptimizationComparison = {
  before: {
    distance_km: 31.16,
    travel_time_min: 83.48,
    active_vehicles: 2
  },
  after: {
    distance_km: 33.55,
    travel_time_min: 90.04,
    active_vehicles: 2
  },
  incident_impact: "+15.2 min network delay induced by arterial incident",
  recovery_action: "QPSO diverted V1 around bottleneck, preserving 8.64 min versus delayed path"
};

export const INITIAL_SCENARIO_STATE: ScenarioState = {
  traffic_status: "NORMAL",
  traffic_level: "Low",
  active_incidents: 0,
  metrics: INITIAL_METRICS,
  vehicles: INITIAL_VEHICLES,
  depot: DEFAULT_DEPOT,
  customers: DEFAULT_CUSTOMERS,
  benchmark: BENCHMARK_DATA,
  reoptimization: REOPTIMIZATION_COMPARISON
};
