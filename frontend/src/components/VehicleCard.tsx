import React from 'react';
import { Truck, Navigation, Clock, Gauge } from 'lucide-react';
import { VehicleRoute } from '../types';

interface VehicleCardProps {
  vehicle: VehicleRoute;
  isHighlighted?: boolean;
}

export const VehicleCard: React.FC<VehicleCardProps> = ({
  vehicle,
  isHighlighted = false
}) => {
  const isUnused = vehicle.status === 'unused';
  const capacityPct = vehicle.capacity > 0 ? (vehicle.demand / vehicle.capacity) * 100 : 0;

  return (
    <div className={`rounded-lg p-3.5 border transition-all duration-200 ${
      isUnused
        ? 'bg-slate-900/40 border-slate-800/60 opacity-60'
        : isHighlighted
        ? 'bg-[#111c33] border-cyan-500/70 shadow-[0_0_15px_rgba(6,182,212,0.12)]'
        : 'bg-[#0e1628]/80 hover:bg-[#121c32] border-slate-800'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-2.5">
        <div className="flex items-center gap-2">
          <div
            className="w-3 h-3 rounded-full flex-shrink-0"
            style={{ backgroundColor: isUnused ? '#64748b' : vehicle.color }}
          />
          <h4 className="font-mono text-xs font-bold text-slate-100 flex items-center gap-1.5">
            <Truck className="h-3.5 w-3.5 text-slate-400" />
            Vehicle {vehicle.id}
          </h4>
        </div>
        <span className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded ${
          isUnused
            ? 'bg-slate-800 text-slate-400'
            : 'bg-cyan-950/80 text-cyan-400 border border-cyan-800/50'
        }`}>
          {isUnused ? 'UNUSED / STANDBY' : 'EN ROUTE'}
        </span>
      </div>

      {isUnused ? (
        <p className="text-xs text-slate-500 font-mono italic py-2 text-center">
          Vehicle on standby at Gachibowli Depot
        </p>
      ) : (
        <div className="space-y-2.5">
          {/* Stops / Route sequence */}
          <div>
            <span className="text-[10px] uppercase font-mono text-slate-400 block mb-1">
              Route Sequence
            </span>
            <div className="flex flex-wrap items-center gap-1 text-[11px] font-mono">
              {vehicle.route.map((stop, i) => (
                <React.Fragment key={i}>
                  <span className={`px-1.5 py-0.5 rounded ${
                    stop === 'Depot'
                      ? 'bg-blue-950/90 text-blue-300 font-semibold border border-blue-800/50'
                      : 'bg-slate-800/90 text-cyan-300 font-medium border border-slate-700/50'
                  }`}>
                    {stop}
                  </span>
                  {i < vehicle.route.length - 1 && (
                    <span className="text-slate-500 text-[10px]">→</span>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>

          {/* Metrics summary */}
          <div className="grid grid-cols-2 gap-2 text-xs font-mono pt-1">
            <div className="flex items-center gap-1.5 text-slate-300">
              <Navigation className="h-3.5 w-3.5 text-cyan-400 flex-shrink-0" />
              <span>{vehicle.distance_km.toFixed(2)} km</span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-300">
              <Clock className="h-3.5 w-3.5 text-emerald-400 flex-shrink-0" />
              <span>{vehicle.travel_time_min.toFixed(2)} min</span>
            </div>
          </div>

          {/* Capacity Progress Bar */}
          <div className="space-y-1 pt-0.5">
            <div className="flex items-center justify-between text-[11px] font-mono">
              <span className="text-slate-400 flex items-center gap-1">
                <Gauge className="h-3 w-3 text-slate-400" />
                Payload Capacity
              </span>
              <span className="text-slate-200 font-semibold">
                {vehicle.demand} / {vehicle.capacity} units
              </span>
            </div>
            <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: `${capacityPct}%`,
                  backgroundColor: capacityPct > 90 ? '#ef4444' : vehicle.color
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
