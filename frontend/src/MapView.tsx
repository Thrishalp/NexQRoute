import React, { useEffect, useMemo } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMap,
  CircleMarker,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix default Leaflet icon paths
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Custom depot marker icon
const depotIcon = L.divIcon({
  className: "custom-depot-marker",
  html: `<div style="background-color: #0f172a; color: #38bdf8; border: 2px solid #38bdf8; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 13px; box-shadow: 0 0 10px rgba(56,189,248,0.5);">D</div>`,
  iconSize: [32, 32],
  iconAnchor: [16, 16],
});

// Custom customer marker icon
const createCustomerIcon = (id: string) =>
  L.divIcon({
    className: "custom-customer-marker",
    html: `<div style="background-color: #ffffff; color: #0f172a; border: 2px solid #10b981; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 11px; box-shadow: 0 2px 4px rgba(0,0,0,0.15);">${id}</div>`,
    iconSize: [26, 26],
    iconAnchor: [13, 13],
  });

// Custom traffic incident warning icon
const incidentIcon = L.divIcon({
  className: "custom-incident-marker",
  html: `
    <div style="position: relative; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;">
      <div style="position: absolute; width: 36px; height: 36px; border-radius: 50%; background: rgba(239, 68, 68, 0.4); animation: pulse 1.5s infinite ease-out;"></div>
      <div style="background-color: #ef4444; color: #ffffff; border: 2px solid #ffffff; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; box-shadow: 0 0 12px rgba(239, 68, 68, 0.8); z-index: 10;">⚠️</div>
    </div>
  `,
  iconSize: [36, 36],
  iconAnchor: [18, 18],
});

const vehicleColors: Record<string, string> = {
  V1: "#10b981", // Emerald Green
  V2: "#3b82f6", // Blue
  V3: "#a855f7", // Purple
};

// Known Gachibowli locations for markers
const defaultDepot = { id: "depot", lat: 17.4435, lng: 78.3512, name: "Central Hub Depot" };
const defaultCustomers = [
  { id: "1", lat: 17.4399, lng: 78.3489, name: "Customer 1" },
  { id: "2", lat: 17.4475, lng: 78.3562, name: "Customer 2" },
  { id: "3", lat: 17.4412, lng: 78.3615, name: "Customer 3" },
  { id: "4", lat: 17.4521, lng: 78.3458, name: "Customer 4" },
  { id: "5", lat: 17.4367, lng: 78.3584, name: "Customer 5" },
  { id: "6", lat: 17.4312, lng: 78.3491, name: "Customer 6" },
  { id: "7", lat: 17.4489, lng: 78.3689, name: "Customer 7" },
  { id: "8", lat: 17.4563, lng: 78.3541, name: "Customer 8" },
  { id: "9", lat: 17.4381, lng: 78.3672, name: "Customer 9" },
  { id: "10", lat: 17.4448, lng: 78.3411, name: "Customer 10" },
];

// Affected road segment geometry (Depot <-> Customer 1 / Customer 2 corridor)
const incidentCorridor: [number, number][] = [
  [17.4435, 78.3512],
  [17.4418, 78.3501],
  [17.4399, 78.3489],
];

interface MapViewProps {
  routeGeometry: Record<string, [number, number][]> | null;
  incidentActive?: boolean;
}

function MapUpdater({ bounds }: { bounds: L.LatLngBoundsExpression | null }) {
  const map = useMap();
  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [40, 40] });
    }
  }, [bounds, map]);
  return null;
}

const MapView: React.FC<MapViewProps> = ({ routeGeometry, incidentActive = false }) => {
  const centerPosition: [number, number] = [17.4435, 78.3512];

  const bounds = useMemo(() => {
    if (!routeGeometry) return null;
    const allCoords = Object.values(routeGeometry).flat();
    if (allCoords.length === 0) return null;
    return L.latLngBounds(allCoords.map(([lat, lng]) => [lat, lng]));
  }, [routeGeometry]);

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      <MapContainer
        center={centerPosition}
        zoom={14}
        style={{ width: "100%", height: "100%", minHeight: "480px" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Depot Marker */}
        <Marker position={[defaultDepot.lat, defaultDepot.lng]} icon={depotIcon}>
          <Popup>
            <strong>{defaultDepot.name}</strong>
            <br />
            Dispatch Center
          </Popup>
        </Marker>

        {/* Customer Markers */}
        {defaultCustomers.map((c) => (
          <Marker
            key={c.id}
            position={[c.lat, c.lng]}
            icon={createCustomerIcon(c.id)}
          >
            <Popup>
              <strong>{c.name}</strong>
              <br />
              Stop #{c.id}
            </Popup>
          </Marker>
        ))}

        {/* Traffic Incident Visual Markers & Choked Link Highlight */}
        {incidentActive && (
          <>
            {/* Choked Segment Red Outline / Glow */}
            <Polyline
              positions={incidentCorridor}
              pathOptions={{
                color: "#ef4444",
                weight: 8,
                opacity: 0.85,
                dashArray: "6, 8",
              }}
            />

            {/* Warning Marker at the core incident hotspot */}
            <Marker position={[17.4418, 78.3501]} icon={incidentIcon}>
              <Popup>
                <div style={{ padding: "4px" }}>
                  <strong style={{ color: "#ef4444" }}>🚨 Traffic Incident</strong>
                  <br />
                  <span style={{ fontSize: "12px", color: "#334155" }}>
                    Severe delay (+15x penalty). Primary corridor blocked. QPSO dynamic rerouting applied.
                  </span>
                </div>
              </Popup>
            </Marker>

            {/* Pulse anchor circle */}
            <CircleMarker
              center={[17.4418, 78.3501]}
              radius={20}
              pathOptions={{
                color: "#ef4444",
                fillColor: "#ef4444",
                fillOpacity: 0.25,
                weight: 1,
              }}
            />
          </>
        )}

        {/* Optimized QPSO Vehicle Routes */}
        {routeGeometry &&
          Object.entries(routeGeometry).map(([vehicleId, coords]) => {
            if (!coords || coords.length === 0) return null;
            return (
              <Polyline
                key={vehicleId}
                positions={coords}
                pathOptions={{
                  color: vehicleColors[vehicleId] || "#22c55e",
                  weight: 5,
                  opacity: 0.9,
                }}
              />
            );
          })}

        <MapUpdater bounds={bounds} />
      </MapContainer>
    </div>
  );
};

export default MapView;