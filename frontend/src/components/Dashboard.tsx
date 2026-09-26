import React, { useState } from 'react';
import {
  Navigation,
  Clock,
  Truck,
  Users
} from 'lucide-react';

import { ScenarioState } from '../types';
import {
  INITIAL_SCENARIO_STATE,
  INCIDENT_ROAD_DATA,
  INCIDENT_METRICS,
  REOPTIMIZED_METRICS,
  REOPTIMIZED_VEHICLES
} from '../services/mockData';

import { Header } from './Header';
import { MetricCard } from './MetricCard';
import { TrafficStatus } from './TrafficStatus';
import { FleetStatus } from './FleetStatus';
import { OptimizationStatus } from './OptimizationStatus';
import { ControlPanel } from './ControlPanel';
import { RouteSummary } from './RouteSummary';
import { MapView } from './MapView';
import { BenchmarkSection } from './BenchmarkSection';
import { BeforeAfterSection } from './BeforeAfterSection';
import { TrafficIncidentPanel } from './TrafficIncidentPanel';
import { OptimizationDetails } from './OptimizationDetails';

export const Dashboard: React.FC = () => {
  const [scenario, setScenario] = useState<ScenarioState>(INITIAL_SCENARIO_STATE);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizationStep, setOptimizationStep] = useState(0);
  const [isReoptimized, setIsReoptimized] = useState(false);

  // Action 1: Simulate Traffic Incident
  const handleSimulateIncident = () => {
    setScenario(prev => ({
      ...prev,
      traffic_status: 'INCIDENT',
      traffic_level: 'Heavy Congestion',
      active_incidents: 1,
      incident_details: INCIDENT_ROAD_DATA,
      metrics: INCIDENT_METRICS
    }));
  };

  // Action 2: Re-optimize with QPSO (Multi-step animation)
  const handleReoptimize = () => {
    setIsOptimizing(true);
    setOptimizationStep(0);

    const stepInterval = 750;

    // Step 0: "Updating road weights..."
    setTimeout(() => {
      setOptimizationStep(1); // "Recalculating travel-time matrix..."
    }, stepInterval);

    setTimeout(() => {
      setOptimizationStep(2); // "Running QPSO..."
    }, stepInterval * 2);

    setTimeout(() => {
      setOptimizationStep(3); // "Generating feasible routes..."
    }, stepInterval * 3);

    setTimeout(() => {
      setOptimizationStep(4); // "Routes successfully re-optimized."
    }, stepInterval * 4);

    setTimeout(() => {
      setIsOptimizing(false);
      setIsReoptimized(true);
      setScenario(prev => ({
        ...prev,
        traffic_status: 'NORMAL',
        traffic_level: 'Low',
        active_incidents: 0,
        incident_details: undefined,
        metrics: REOPTIMIZED_METRICS,
        vehicles: REOPTIMIZED_VEHICLES
      }));
    }, stepInterval * 5);
  };

  // Action 3: Reset Scenario
  const handleReset = () => {
    setIsOptimizing(false);
    setOptimizationStep(0);
    setIsReoptimized(false);
    setScenario(structuredClone(INITIAL_SCENARIO_STATE));
  };

  const { traffic_status, traffic_level, active_incidents, metrics, vehicles, depot, customers, benchmark, reoptimization, incident_details } = scenario;

  return (
    <div className="min-h-screen bg-[#070c18] text-slate-100 flex flex-col font-sans">
      
      {/* Top Navigation / Command Header */}
      <Header
        trafficStatus={traffic_status}
        onReset={handleReset}
        isOptimizing={isOptimizing}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-[1700px] w-full mx-auto px-4 lg:px-6 py-6 space-y-6">
        
        {/* Incident Alert Banner */}
        <TrafficIncidentPanel
          trafficStatus={traffic_status}
          isOptimizing={isOptimizing}
          optimizationStep={optimizationStep}
          onReoptimize={handleReoptimize}
        />

        {/* 1. Main Telemetry Metrics Section (4 Cards) */}
        <section className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <MetricCard
            label="Total Distance"
            value={metrics.total_distance_km.toFixed(2)}
            unit="km"
            icon={Navigation}
            subtext="OSMnx street graph network"
            variant="cyan"
            highlightChange={traffic_status === 'INCIDENT'}
          />

          <MetricCard
            label="Travel Time"
            value={metrics.total_time_min.toFixed(2)}
            unit="min"
            icon={Clock}
            subtext={traffic_status === 'INCIDENT' ? '+15.2m delayed by incident' : 'Optimal traffic-adjusted'}
            variant={traffic_status === 'INCIDENT' ? 'amber' : 'emerald'}
            highlightChange={traffic_status === 'INCIDENT'}
          />

          <MetricCard
            label="Active Vehicles"
            value={metrics.active_vehicles}
            unit={`/ ${metrics.total_vehicles}`}
            icon={Truck}
            subtext="Capacity-constrained fleet"
            variant="blue"
          />

          <MetricCard
            label="Customers Served"
            value={metrics.customers_served}
            unit={`/ ${metrics.total_customers}`}
            icon={Users}
            subtext="100% Demand satisfied"
            variant="cyan"
          />
        </section>

        {/* 2. Main Two-Column Layout */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* LEFT SIDEBAR / CONTROL PANEL (approx 33% width -> 4 of 12 cols) */}
          <div className="lg:col-span-4 space-y-4">
            {/* 1. Traffic Status Card */}
            <TrafficStatus
              status={traffic_status}
              level={traffic_level}
              activeIncidents={active_incidents}
            />

            {/* 2. Command Controls */}
            <ControlPanel
              trafficStatus={traffic_status}
              onSimulateIncident={handleSimulateIncident}
              onReoptimize={handleReoptimize}
              onReset={handleReset}
              isOptimizing={isOptimizing}
            />

            {/* 3. Fleet Status */}
            <FleetStatus
              activeVehicles={metrics.active_vehicles}
              availableVehicles={metrics.total_vehicles}
              customersCount={metrics.customers_served}
            />

            {/* 4. QPSO Optimization Status */}
            <OptimizationStatus
              status={traffic_status}
              bestTravelTime={metrics.total_time_min}
              bestDistance={metrics.total_distance_km}
              runtimeSec={metrics.runtime_sec}
              isOptimizing={isOptimizing}
            />

            {/* 5. Route Summary (Vehicle Cards V1, V2, V3) */}
            <RouteSummary vehicles={vehicles} />
          </div>

          {/* RIGHT MAIN PANEL (approx 67% width -> 8 of 12 cols) */}
          <div className="lg:col-span-8 space-y-6">
            
            {/* Large Interactive Leaflet Map */}
            <MapView
              depot={depot}
              customers={customers}
              vehicles={vehicles}
              trafficStatus={traffic_status}
              incidentDetails={incident_details}
            />

            {/* Algorithm Benchmark Section */}
            <BenchmarkSection benchmark={benchmark} />

            {/* Dynamic Re-Optimization (Before vs After) Section */}
            <BeforeAfterSection
              comparison={reoptimization}
              isReoptimized={isReoptimized}
            />

            {/* Technical Optimization Details Accordion */}
            <OptimizationDetails />
            
          </div>

        </section>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#070c18] py-4 px-6 text-center text-xs font-mono text-slate-500">
        <div className="max-w-[1700px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>
            <span className="font-semibold text-slate-400">SIH 2026</span> &bull; Problem Statement: <span className="text-cyan-400 font-semibold">SIH26137</span>
          </div>
          <div>
            Transportation &amp; Logistics &bull; Quantum-Inspired Intelligent Traffic Route Optimization
          </div>
          <div className="text-slate-600">
            Gachibowli OpenStreetMap Network
          </div>
        </div>
      </footer>

    </div>
  );
};
