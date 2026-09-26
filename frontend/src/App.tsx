import {
  useEffect,
  useState,
  type ReactNode,
} from "react";

import {
  Activity,
  Car,
  ChevronDown,
  Clock3,
  GitCompare,
  MapPin,
  Menu,
  Navigation,
  Play,
  Route,
  Settings,
  SlidersHorizontal,
  TrafficCone,
  User,
  X,
  Zap,
} from "lucide-react";

import "./App.css";
import MapView from "./MapView";
import { optimizeRoutes, triggerTrafficIncident } from "./services/api";
import type { OptimizationResponse } from "./services/api";

const defaultVehicles = [
  {
    id: "V1",
    status: "ACTIVE",
    route: "Depot → C4 → C8 → C7 → C2 → C9 → C3 → Depot",
    time: "51.7 min",
    distance: "18.4 km",
    load: "39 / 40",
  },
  {
    id: "V2",
    status: "ACTIVE",
    route: "Depot → C6 → C5 → C1 → C10 → Depot",
    time: "42.5 min",
    distance: "13.8 km",
    load: "29 / 40",
  },
  {
    id: "V3",
    status: "IDLE",
    route: "Depot → Depot",
    time: "—",
    distance: "—",
    load: "0 / 40",
  },
];

const algorithms = [
  {
    name: "PSO",
    fullName: "Particle Swarm Optimization",
    time: "—",
    distance: "—",
    runtime: "—",
    status: "NOT RUN",
  },
  {
    name: "GA",
    fullName: "Genetic Algorithm",
    time: "—",
    distance: "—",
    runtime: "—",
    status: "NOT RUN",
  },
  {
    name: "QPSO",
    fullName: "Quantum Particle Swarm Optimization",
    time: "94.25 min",
    distance: "32.2 km",
    runtime: "0.49 s*",
    status: "AVAILABLE",
  },
];

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [trafficMode, setTrafficMode] = useState("LIVE");
  const [incident, setIncident] = useState(false);
  const [activeSection, setActiveSection] = useState("Operations");
  const [showAlgorithms, setShowAlgorithms] = useState(false);

  const [optimizing, setOptimizing] = useState(false);
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResponse | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      setSidebarOpen(false);
    }, 500);

    const handleMouseMove = (event: MouseEvent) => {
      if (event.clientX <= 25) {
        setSidebarOpen(true);
      }
    };

    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      clearTimeout(timer);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  const selectSection = (section: string) => {
    setActiveSection(section);
    setSidebarOpen(false);

    const element = document.getElementById(section.toLowerCase());
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  };

  const runOptimization = async () => {
    setOptimizing(true);
    try {
      const data = await optimizeRoutes(false);
      setOptimizationResult(data);
      localStorage.setItem("nexqroute_optimization", JSON.stringify(data));
    } catch (error) {
      console.error("Optimization failed:", error);
      alert("Failed to connect to backend optimization service. Make sure FastAPI is running.");
    } finally {
      setOptimizing(false);
    }
  };

  const simulateIncident = async () => {
    const nextIncident = !incident;
    setIncident(nextIncident);
    setTrafficMode(nextIncident ? "INCIDENT" : "LIVE");
    setOptimizing(true);
    try {
      const data = nextIncident
        ? await triggerTrafficIncident()
        : await optimizeRoutes(false);
      setOptimizationResult(data);
      localStorage.setItem("nexqroute_optimization", JSON.stringify(data));
    } catch (error) {
      console.error("Incident operation failed:", error);
      alert("Failed to execute traffic incident re-optimization.");
    } finally {
      setOptimizing(false);
    }
  };

  const getActiveVehicleCount = () => {
    if (!optimizationResult?.routes) return "2";
    return Object.values(optimizationResult.routes).filter((route) => route.length > 2).length.toString();
  };

  const getDynamicFleet = () => {
    if (!optimizationResult?.routes) return defaultVehicles;

    return Object.entries(optimizationResult.routes).map(([id, route]) => ({
      id,
      status: route.length > 2 ? "ACTIVE" : "IDLE",
      route: route.join(" → "),
      time: route.length > 2 ? "Calculated" : "—",
      distance: route.length > 2 ? "Calculated" : "—",
      load: route.length > 2 ? "Optimal" : "0",
    }));
  };

  const displayTime = optimizationResult?.best_time ? optimizationResult.best_time.toFixed(1) : "94.2";
  const displayDistance = optimizationResult?.distance ? optimizationResult.distance.toFixed(1) : "32.2";
  const activeVehicles = getActiveVehicleCount();
  const fleetData = getDynamicFleet();

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
        <div className="brand">
          <div className="brand-wordmark">
            Nex<span>Q</span>Route
          </div>
          <div className="brand-caption">INTELLIGENT ROUTING</div>
        </div>

        <div className="sidebar-section-title">OPERATIONS</div>

        <nav className="sidebar-nav">
          <button
            className={`sidebar-button ${activeSection === "Operations" ? "selected" : ""}`}
            onClick={() => selectSection("Operations")}
          >
            <Activity size={18} />
            <span>Operations</span>
          </button>

          <button
            className={`sidebar-button ${activeSection === "Routes" ? "selected" : ""}`}
            onClick={() => selectSection("Routes")}
          >
            <Route size={18} />
            <span>Routes</span>
          </button>

          <button
            className={`sidebar-button ${activeSection === "Fleet" ? "selected" : ""}`}
            onClick={() => selectSection("Fleet")}
          >
            <Car size={18} />
            <span>Fleet</span>
          </button>

          <button
            className={`sidebar-button ${activeSection === "Traffic" ? "selected" : ""}`}
            onClick={() => selectSection("Traffic")}
          >
            <TrafficCone size={18} />
            <span>Traffic</span>
          </button>
        </nav>

        <div className="sidebar-section-title system-title">SYSTEM</div>

        <button className="sidebar-button" onClick={() => setSidebarOpen(false)}>
          <SlidersHorizontal size={18} />
          <span>Configuration</span>
        </button>

        <div className="sidebar-bottom">
          <button className="bottom-icon-button">
            <Settings size={18} />
            <span>Settings</span>
          </button>
          <button className="bottom-icon-button">
            <User size={18} />
            <span>User</span>
          </button>
          <div className="system-state">
            <span />
            System Online
          </div>
        </div>
      </aside>

      <button
        className={`sidebar-toggle ${sidebarOpen ? "sidebar-toggle-open" : ""}`}
        onClick={() => setSidebarOpen(!sidebarOpen)}
      >
        {sidebarOpen ? <X size={17} /> : <Menu size={19} />}
      </button>

      <main className="main">
        <header className="header">
          <div>
            <div className="eyebrow">FLEET OPERATIONS · GACHIBOWLI</div>
            <h1>NexQRoute</h1>
            <p>Quantum-inspired intelligent traffic route optimization</p>
          </div>
          <div className="header-actions">
            <div className="live-pill">
              <span /> TOMTOM LIVE
            </div>
            <button className="header-button">
              <Clock3 size={17} /> Live
            </button>
          </div>
        </header>

        <section className="kpi-grid">
          <KPI
            label="TRAVEL TIME"
            value={displayTime}
            unit="min"
            icon={<Clock3 size={20} />}
            className="blue"
          />
          <KPI
            label="TOTAL DISTANCE"
            value={displayDistance}
            unit="km"
            icon={<Navigation size={20} />}
            className="green"
          />
          <KPI
            label="ACTIVE VEHICLES"
            value={activeVehicles}
            unit="/ 3"
            icon={<Car size={20} />}
            className="purple"
          />
          <KPI
            label="CUSTOMERS SERVED"
            value="10"
            unit="/ 10"
            icon={<MapPin size={20} />}
            className="orange"
          />
        </section>

        <section className="operations-layout">
          <div className="side-column">
            <section className="glass-card" id="traffic">
              <div className="card-title-row">
                <div>
                  <div className="eyebrow">TRAFFIC INTELLIGENCE</div>
                  <h2>Live Traffic</h2>
                </div>
                <div className={`traffic-pill ${incident ? "danger" : ""}`}>
                  <span />
                  {trafficMode}
                </div>
              </div>

              <div className="speed-display">
                <strong>{incident ? "18" : "29"}</strong>
                <div>
                  km/h
                  <small>current road speed</small>
                </div>
              </div>

              <div className="info-list">
                <InfoRow label="Provider" value="TomTom" />
                <InfoRow label="Confidence" value="High" />
                <InfoRow label="Network" value="Gachibowli" />
                <InfoRow label="Mode" value="Real-time" />
              </div>

              <button className="secondary-button" onClick={simulateIncident} disabled={optimizing}>
                <TrafficCone size={16} />
                {incident ? "Clear Traffic Incident" : "Simulate Traffic Incident"}
              </button>
            </section>

            <section className="glass-card">
              <div className="eyebrow">OPTIMIZATION ENGINE</div>
              <div className="engine-heading">
                <div className="engine-icon">
                  <Zap size={20} />
                </div>
                <div>
                  <h2>QPSO</h2>
                  <p>Discrete CVRP optimization</p>
                </div>
              </div>

              <div className="engine-stats">
                <InfoRow label="Particles" value="40" />
                <InfoRow label="Iterations" value="150" />
                <InfoRow label="Vehicles" value="3" />
                <InfoRow label="Customers" value="10" />
              </div>

              <button
                className="primary-button"
                onClick={runOptimization}
                disabled={optimizing}
              >
                {optimizing ? (
                  <>
                    <Activity className="spin" size={17} />
                    SEARCHING ROUTES...
                  </>
                ) : (
                  <>
                    <Play size={17} />
                    RUN QPSO OPTIMIZATION
                  </>
                )}
              </button>
            </section>
          </div>

          <div className="map-card">
            <div className="card-header">
              <div>
                <div className="eyebrow">LIVE NETWORK</div>
                <h2>Gachibowli Transportation Network</h2>
              </div>
              <div className="network-status">
                <span />
                LIVE NETWORK
              </div>
            </div>

            {/* MapView with incidentActive prop */}
            <MapView
              routeGeometry={optimizationResult?.route_geometry || null}
              incidentActive={incident}
            />
          </div>
        </section>

        <section className="status-card" id="routes">
          <div className="status-left">
            <div className="eyebrow">OPTIMIZATION STATUS</div>
            <h2>
              {optimizing
                ? "Searching for improved route..."
                : optimizationResult ? "Optimized solution available" : "System Ready"}
            </h2>
            <div className="progress">
              <div style={{ width: optimizing ? "100%" : "0%", transition: "width 2s ease" }} />
            </div>
          </div>
          <div className="status-metrics">
            <Metric label="BEST TIME" value={`${displayTime} min`} />
            <Metric label="DISTANCE" value={`${displayDistance} km`} />
            <Metric label="VEHICLES" value={`${activeVehicles} / 3`} />
            <Metric label="STATUS" value={optimizationResult ? "FEASIBLE" : "PENDING"} />
          </div>
        </section>

        <section className="glass-card fleet-card" id="fleet">
          <div className="card-header">
            <div>
              <div className="eyebrow">FLEET DISPATCH</div>
              <h2>Optimized Vehicle Routes</h2>
            </div>
            <div className="fleet-count">3 VEHICLES · 10 CUSTOMERS</div>
          </div>

          <div className="fleet-table">
            <div className="fleet-header">
              <span>VEHICLE</span>
              <span>STATUS</span>
              <span>ROUTE</span>
              <span>TIME</span>
              <span>DISTANCE</span>
              <span>LOAD</span>
            </div>

            {fleetData.map((vehicle) => (
              <div className="fleet-row" key={vehicle.id}>
                <div className="vehicle-name">
                  <Car size={17} />
                  <strong>{vehicle.id}</strong>
                </div>

                <div>
                  <span className={`status-tag ${vehicle.status === "IDLE" ? "idle" : ""}`}>
                    {vehicle.status}
                  </span>
                </div>

                <div className="route-text" title={vehicle.route}>{vehicle.route}</div>
                <strong className="table-number">{vehicle.time}</strong>
                <strong className="table-number">{vehicle.distance}</strong>

                <div>
                  <span className="load-value">{vehicle.load}</span>
                  <div className="load-bar">
                    <div style={{ width: vehicle.status === "ACTIVE" ? "80%" : "0%" }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="comparison-section">
          <div className="comparison-header">
            <div>
              <div className="eyebrow">ALGORITHM BENCHMARK</div>
              <h2>Optimization Algorithm Comparison</h2>
              <p>Compare classical and quantum-inspired optimization approaches.</p>
            </div>
            <button
              className="compare-button"
              onClick={() => setShowAlgorithms(!showAlgorithms)}
            >
              <GitCompare size={17} />
              {showAlgorithms ? "Hide comparison" : "View comparison"}
              <ChevronDown size={16} className={showAlgorithms ? "rotate" : ""} />
            </button>
          </div>

          {showAlgorithms && (
            <div className="algorithm-grid">
              {algorithms.map((algorithm) => (
                <div
                  className={`algorithm-card ${algorithm.name === "QPSO" ? "featured" : ""}`}
                  key={algorithm.name}
                >
                  <div className="algorithm-top">
                    <div className="algorithm-name">{algorithm.name}</div>
                    <span>{algorithm.status}</span>
                  </div>
                  <p>{algorithm.fullName}</p>
                  <div className="algorithm-values">
                    <Metric
                      label="TRAVEL TIME"
                      value={algorithm.name === "QPSO" ? `${displayTime} min` : algorithm.time}
                    />
                    <Metric
                      label="DISTANCE"
                      value={algorithm.name === "QPSO" ? `${displayDistance} km` : algorithm.distance}
                    />
                    <Metric label="RUNTIME" value={algorithm.runtime} />
                  </div>
                </div>
              ))}
            </div>
          )}
          <div className="comparison-note">
            * QPSO runtime shown from the current prototype benchmark. PSO and GA values will populate when their implementations are connected.
          </div>
        </section>

        <section className="statistics-section">
          <div className="eyebrow">SYSTEM STATISTICS</div>
          <h2>Routing Performance</h2>
          <div className="statistics-grid">
            <StatCard title="CUSTOMER COVERAGE" value="100%" detail="10 of 10 customers served" />
            <StatCard title="FLEET UTILIZATION" value={`${((Number(activeVehicles) / 3) * 100).toFixed(1)}%`} detail={`${activeVehicles} of 3 vehicles active`} />
            <StatCard title="QPSO ITERATIONS" value="150" detail="Completed optimization cycles" />
            <StatCard title="TRAFFIC SOURCE" value="LIVE" detail="TomTom traffic intelligence" />
          </div>
        </section>

        <footer className="footer">
          <span>NexQRoute · Quantum-Inspired Intelligent Routing</span>
          <span>OSM · TomTom · CVRP · QPSO</span>
        </footer>
      </main>
    </div>
  );
}

function KPI({ label, value, unit, icon, className }: { label: string; value: string; unit: string; icon: ReactNode; className: string; }) {
  return (
    <div className={`kpi-card ${className}`}>
      <div className="kpi-icon">{icon}</div>
      <div>
        <span>{label}</span>
        <strong>
          {value}
          {unit && <small>{unit}</small>}
        </strong>
      </div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string; }) {
  return (
    <div className="info-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string; }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function StatCard({ title, value, detail }: { title: string; value: string; detail: string; }) {
  return (
    <div className="stat-card">
      <span>{title}</span>
      <strong>{value}</strong>
      <p>{detail}</p>
    </div>
  );
}

export default App;