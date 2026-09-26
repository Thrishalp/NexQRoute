import React from 'react';
import { Route } from 'lucide-react';
import { VehicleRoute } from '../types';
import { VehicleCard } from './VehicleCard';

interface RouteSummaryProps {
  vehicles: Record<string, VehicleRoute>;
}

export const RouteSummary: React.FC<RouteSummaryProps> = ({ vehicles }) => {
  return (
    <div className="rounded-lg bg-[#0d1424]/90 border border-slate-800 p-4 space-y-3 shadow-[0_0_15px_rgba(0,0,0,0.2)]">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Route className="h-4 w-4 text-cyan-400" />
          <h3 className="text-xs font-bold uppercase tracking-wider font-mono text-slate-300">
            Route Assignments
          </h3>
        </div>
        <span className="text-[10px] font-mono text-slate-400">
          {Object.values(vehicles).filter(v => v.status === 'active').length} Active Routes
        </span>
      </div>

      <div className="space-y-3">
        {Object.values(vehicles).map((vehicle) => (
          <VehicleCard key={vehicle.id} vehicle={vehicle} />
        ))}
      </div>
    </div>
  );
};
