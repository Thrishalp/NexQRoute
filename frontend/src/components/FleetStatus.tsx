import React from 'react';
import { Truck } from 'lucide-react';

interface FleetStatusProps {
  activeVehicles: number;
  availableVehicles: number;
  customersCount: number;
}

export const FleetStatus: React.FC<FleetStatusProps> = ({
  activeVehicles,
  availableVehicles,
  customersCount
}) => {
  return (
    <div className="rounded-lg bg-[#0d1424]/90 border border-slate-800 p-4 shadow-[0_0_15px_rgba(0,0,0,0.2)]">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Truck className="h-4 w-4 text-cyan-400" />
          <h3 className="text-xs font-bold uppercase tracking-wider font-mono text-slate-300">
            Fleet Deployment
          </h3>
        </div>
        <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded bg-slate-800 text-slate-400">
          Capacity Aware
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-slate-900/80 rounded p-2.5 border border-slate-800/80">
          <span className="text-[10px] uppercase font-mono text-slate-400 block mb-1">
            Active
          </span>
          <span className="text-xl font-bold font-mono text-cyan-400">
            {activeVehicles}
          </span>
        </div>

        <div className="bg-slate-900/80 rounded p-2.5 border border-slate-800/80">
          <span className="text-[10px] uppercase font-mono text-slate-400 block mb-1">
            Available
          </span>
          <span className="text-xl font-bold font-mono text-slate-200">
            {availableVehicles}
          </span>
        </div>

        <div className="bg-slate-900/80 rounded p-2.5 border border-slate-800/80">
          <span className="text-[10px] uppercase font-mono text-slate-400 block mb-1">
            Customers
          </span>
          <span className="text-xl font-bold font-mono text-emerald-400">
            {customersCount}
          </span>
        </div>
      </div>
    </div>
  );
};
