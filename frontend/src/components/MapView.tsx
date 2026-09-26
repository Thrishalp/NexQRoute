import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { RotateCcw, AlertTriangle } from 'lucide-react';
import { Customer, Depot, VehicleRoute, IncidentRoad, TrafficStatusType } from '../types';
import { Legend } from './Legend';

interface MapViewProps {
  depot: Depot;
  customers: Customer[];
  vehicles: Record<string, VehicleRoute>;
  trafficStatus: TrafficStatusType;
  incidentDetails?: IncidentRoad;
}

export const MapView: React.FC<MapViewProps> = ({
  depot,
  customers,
  vehicles,
  trafficStatus,
  incidentDetails
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const routeLayersRef = useRef<L.LayerGroup | null>(null);
  const markerLayersRef = useRef<L.LayerGroup | null>(null);
  const incidentLayersRef = useRef<L.LayerGroup | null>(null);

  // Initialize Leaflet Map once
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Create Map centered at Gachibowli Depot
    const map = L.map(mapContainerRef.current, {
      center: [depot.lat, depot.lng],
      zoom: 13,
      zoomControl: false,
      attributionControl: false
    });

    // Custom dark themed tile layer from CartoDB
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      subdomains: 'abcd',
    }).addTo(map);

    // Zoom controls positioned top-right
    L.control.zoom({ position: 'topright' }).addTo(map);

    // Layer groups for clean updates
    routeLayersRef.current = L.layerGroup().addTo(map);
    markerLayersRef.current = L.layerGroup().addTo(map);
    incidentLayersRef.current = L.layerGroup().addTo(map);

    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, [depot.lat, depot.lng]);

  // Update Markers (Depot & Customers)
  useEffect(() => {
    const map = mapInstanceRef.current;
    const markerGroup = markerLayersRef.current;
    if (!map || !markerGroup) return;

    markerGroup.clearLayers();

    // 1. Depot Marker
    const depotIcon = L.divIcon({
      className: 'custom-depot-icon',
      html: `
        <div class="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-tr from-blue-700 to-cyan-500 border-2 border-cyan-200 shadow-[0_0_15px_rgba(6,182,212,0.8)] text-white font-bold text-xs font-mono">
          DEPOT
        </div>
      `,
      iconSize: [44, 44],
      iconAnchor: [22, 22]
    });

    L.marker([depot.lat, depot.lng], { icon: depotIcon })
      .addTo(markerGroup)
      .bindPopup(`
        <div class="p-1 font-mono text-xs text-slate-100">
          <div class="font-bold text-cyan-400 text-sm mb-0.5">DEPOT</div>
          <div class="text-slate-300">${depot.name}</div>
          <div class="text-slate-400 text-[10px] mt-1">Lat: ${depot.lat.toFixed(5)}, Lng: ${depot.lng.toFixed(5)}</div>
        </div>
      `);

    // 2. Customer Markers (C1 - C10)
    customers.forEach((cust) => {
      const custIcon = L.divIcon({
        className: 'custom-customer-icon',
        html: `
          <div class="flex flex-col items-center justify-center w-8 h-8 rounded-lg bg-[#0b1324] border border-cyan-400 shadow-[0_0_8px_rgba(6,182,212,0.4)] text-cyan-300 font-mono font-bold text-[11px] hover:scale-110 transition-transform">
            <span>${cust.id}</span>
            <span class="text-[8px] text-slate-400 font-normal leading-none">d:${cust.demand}</span>
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      L.marker([cust.lat, cust.lng], { icon: custIcon })
        .addTo(markerGroup)
        .bindPopup(`
          <div class="p-1 font-mono text-xs text-slate-100">
            <div class="font-bold text-cyan-300 text-sm mb-1">${cust.id} - Customer Node</div>
            <div class="flex items-center justify-between text-slate-300">
              <span>Demand:</span>
              <span class="font-bold text-cyan-400">${cust.demand} units</span>
            </div>
            <div class="text-[10px] text-slate-400 mt-1">Node ID: ${cust.node}</div>
          </div>
        `);
    });
  }, [depot, customers]);

  // Update Route Polylines
  useEffect(() => {
    const map = mapInstanceRef.current;
    const routeGroup = routeLayersRef.current;
    if (!map || !routeGroup) return;

    routeGroup.clearLayers();

    Object.values(vehicles).forEach((vehicle) => {
      if (vehicle.status !== 'active' || vehicle.geometry.length < 2) return;

      // Glow background line
      L.polyline(vehicle.geometry, {
        color: vehicle.color,
        weight: 7,
        opacity: 0.25,
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(routeGroup);

      // Core crisp polyline
      const poly = L.polyline(vehicle.geometry, {
        color: vehicle.color,
        weight: 3.5,
        opacity: 0.9,
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(routeGroup);

      poly.bindPopup(`
        <div class="p-1 font-mono text-xs text-slate-100">
          <div class="font-bold text-sm mb-1" style="color: ${vehicle.color}">
            Vehicle ${vehicle.id} Route
          </div>
          <div>Distance: <b>${vehicle.distance_km.toFixed(2)} km</b></div>
          <div>Travel Time: <b>${vehicle.travel_time_min.toFixed(2)} min</b></div>
          <div>Load: <b>${vehicle.demand} / ${vehicle.capacity} units</b></div>
        </div>
      `);
    });
  }, [vehicles]);

  // Update Traffic Incident Visualization
  useEffect(() => {
    const map = mapInstanceRef.current;
    const incidentGroup = incidentLayersRef.current;
    if (!map || !incidentGroup) return;

    incidentGroup.clearLayers();

    if (trafficStatus === 'INCIDENT' && incidentDetails && incidentDetails.geometry.length > 0) {
      // Pulsing red dashed corridor
      L.polyline(incidentDetails.geometry, {
        color: '#ef4444',
        weight: 8,
        opacity: 0.4,
        lineCap: 'round'
      }).addTo(incidentGroup);

      L.polyline(incidentDetails.geometry, {
        color: '#f87171',
        weight: 4,
        dashArray: '8, 8',
        opacity: 1
      }).addTo(incidentGroup);

      // Warning marker at mid-point of incident road
      const midCoord = incidentDetails.geometry[Math.floor(incidentDetails.geometry.length / 2)];
      const incidentIcon = L.divIcon({
        className: 'incident-hazard-icon',
        html: `
          <div class="flex items-center justify-center w-8 h-8 rounded-full bg-red-600 border-2 border-white shadow-[0_0_20px_rgba(239,68,68,0.9)] animate-pulse text-white">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 2L1 21h22L12 2zm0 3.5L20.3 19H3.7L12 5.5zM11 10v4h2v-4h-2zm0 6v2h2v-2h-2z"/></svg>
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      L.marker(midCoord, { icon: incidentIcon })
        .addTo(incidentGroup)
        .bindPopup(`
          <div class="p-1 font-mono text-xs text-slate-100">
            <div class="font-bold text-red-400 text-sm mb-1">TRAFFIC INCIDENT DETECTED</div>
            <div class="text-slate-300 font-semibold">${incidentDetails.name}</div>
            <div class="text-slate-400 text-[11px] mt-1">${incidentDetails.description}</div>
            <div class="text-amber-400 font-bold mt-1.5">Estimated Delay: +${incidentDetails.added_delay_min} min</div>
          </div>
        `)
        .openPopup();
    }
  }, [trafficStatus, incidentDetails]);

  // Recenter Handler
  const handleRecenter = () => {
    if (mapInstanceRef.current) {
      mapInstanceRef.current.flyTo([depot.lat, depot.lng], 13, {
        duration: 1.2
      });
    }
  };

  return (
    <div className="relative w-full rounded-xl overflow-hidden border border-slate-800 bg-[#070c18] shadow-2xl flex flex-col h-[520px] lg:h-[620px]">
      
      {/* Top Map Header Bar */}
      <div className="absolute top-3 left-3 z-10 flex items-center gap-2">
        <div className="bg-[#0b1220]/90 backdrop-blur-md border border-slate-800 rounded-md px-3 py-1.5 flex items-center gap-2 shadow-lg">
          <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <span className="text-xs font-mono text-slate-200 font-semibold">
            Live OpenStreetMap Telemetry Layer
          </span>
          <span className="text-[10px] font-mono text-slate-500 border-l border-slate-700 pl-2">
            Gachibowli, Hyderabad
          </span>
        </div>

        {trafficStatus === 'INCIDENT' && (
          <div className="bg-red-950/90 backdrop-blur-md border border-red-600 rounded-md px-3 py-1.5 flex items-center gap-1.5 shadow-[0_0_15px_rgba(239,68,68,0.3)] animate-pulse">
            <AlertTriangle className="h-3.5 w-3.5 text-red-400" />
            <span className="text-xs font-mono text-red-300 font-bold">
              ACTIVE INCIDENT VISUALIZED
            </span>
          </div>
        )}
      </div>

      {/* Recenter Button */}
      <div className="absolute top-3 right-12 z-10">
        <button
          onClick={handleRecenter}
          className="bg-[#0b1220]/90 hover:bg-slate-800 active:bg-slate-900 backdrop-blur-md border border-slate-800 text-slate-300 hover:text-white rounded-md px-2.5 py-1.5 flex items-center gap-1.5 text-xs font-mono transition-colors shadow-lg cursor-pointer"
          title="Recenter map on Depot"
        >
          <RotateCcw className="h-3.5 w-3.5 text-cyan-400" />
          <span className="hidden sm:inline">Recenter Hub</span>
        </button>
      </div>

      {/* Leaflet Map Canvas */}
      <div ref={mapContainerRef} className="w-full h-full z-0" />

      {/* Embedded Bottom Legend */}
      <div className="absolute bottom-3 left-3 right-3 z-10">
        <Legend trafficStatus={trafficStatus} />
      </div>

    </div>
  );
};
