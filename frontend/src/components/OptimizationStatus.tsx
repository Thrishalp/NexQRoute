import React from 'react';
import { Atom } from 'lucide-react';
import { TrafficStatusType } from '../types';

interface OptimizationStatusProps {
  status: TrafficStatusType;
  bestTravelTime: number;
  bestDistance: number;
  runtimeSec: number;
  isOptimizing: boolean;
}

export const OptimizationStatus: React.FC<OptimizationStatusProps> = ({
  status,
  bestTravelTime,
  bestDistance,
  runtimeSec,
  isOptimizing
}) => {
  return (
    <div className="rounded-lg bg-[#0d1424]/90 border border-slate-800 p-4 shadow-[0_0_15px_rgba(0,0,0,0.2)]">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Atom className="h-4 w-4 text-cyan-400 animate-spin-slow" />
          <h3 className="text-xs font-bold uppercase tracking-wider font-mono text-slate-300">
            QPSO Optimization
          </h3>
        </div>
        <span className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded border ${
          isOptimizing
            ? 'bg-cyan-950 text-cyan-400 border-cyan-700 animate-pulse'
            : status === 'NORMAL'
            ? 'bg-emerald-950 text-emerald-400 border-emerald-700/60'
            : 'bg-amber-950 text-amber-400 border-amber-700/60'
        }`}>
          {isOptimizing ? 'SOLVING...' : status === 'NORMAL' ? 'OPTIMIZED' : 'RE-OPT NEEDED'}
        </span>
      </div>

      <div className="space-y-2.5 text-xs font-mono">
        <div className="flex items-center justify-between py-1 border-b border-slate-800/80">
          <span className="text-slate-400">Algorithm</span>
          <span className="font-semibold text-cyan-400">QPSO</span>
        </div>

        <div className="flex items-center justify-between py-1 border-b border-slate-800/80">
          <span className="text-slate-400">Problem Mode</span>
          <span className="font-semibold text-slate-200">Discrete CVRP</span>
        </div>

        <div className="flex items-center justify-between py-1 border-b border-slate-800/80">
          <span className="text-slate-400">Best Travel Time</span>
          <span className="font-bold text-slate-100">{bestTravelTime.toFixed(2)} min</span>
        </div>

        <div className="flex items-center justify-between py-1 border-b border-slate-800/80">
          <span className="text-slate-400">Best Distance</span>
          <span className="font-bold text-slate-100">{bestDistance.toFixed(2)} km</span>
        </div>

        <div className="flex items-center justify-between py-1">
          <span className="text-slate-400">Runtime</span>
          <span className="text-emerald-400 font-bold">{runtimeSec.toFixed(3)} s</span>
        </div>
      </div>
    </div>
  );
};
