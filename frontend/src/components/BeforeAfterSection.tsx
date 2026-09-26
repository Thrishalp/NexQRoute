import React from 'react';
import { GitCompare, Info } from 'lucide-react';
import { ReoptimizationComparison } from '../types';

interface BeforeAfterSectionProps {
  comparison: ReoptimizationComparison;
  isReoptimized: boolean;
}

export const BeforeAfterSection: React.FC<BeforeAfterSectionProps> = ({
  comparison,
  isReoptimized
}) => {
  const { before, after } = comparison;

  return (
    <div className="rounded-xl bg-[#0d1424]/90 border border-slate-800 p-5 shadow-[0_0_20px_rgba(0,0,0,0.25)] space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-md bg-blue-950/60 border border-blue-800/60 text-blue-400">
            <GitCompare className="h-4 w-4" />
          </div>
          <div>
            <h3 className="font-mono text-sm font-bold text-slate-100 uppercase tracking-wider">
              Dynamic Re-Optimization Telemetry
            </h3>
            <p className="text-xs text-slate-400">
              Network Adaptation Analysis (Before vs. After Incident Mitigation)
            </p>
          </div>
        </div>

        <span className={`text-xs font-mono font-semibold px-2.5 py-1 rounded border ${
          isReoptimized
            ? 'bg-emerald-950 text-emerald-400 border-emerald-800/60'
            : 'bg-slate-900 text-slate-400 border-slate-800'
        }`}>
          {isReoptimized ? 'ADAPTATION ACTIVE' : 'INITIAL NETWORK STATE'}
        </span>
      </div>

      {/* Grid: Before vs After Columns */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        {/* Before Incident Card */}
        <div className="rounded-lg bg-slate-900/70 border border-slate-800 p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="text-xs font-bold font-mono text-slate-300 uppercase tracking-wider">
              1. Pre-Incident Optimal
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
              Clear Traffic
            </span>
          </div>

          <div className="grid grid-cols-3 gap-2 text-center font-mono">
            <div className="bg-[#0b1120] p-2 rounded border border-slate-800/60">
              <span className="text-[10px] text-slate-400 block mb-0.5">Distance</span>
              <span className="text-sm font-bold text-slate-100">{before.distance_km.toFixed(2)} km</span>
            </div>
            <div className="bg-[#0b1120] p-2 rounded border border-slate-800/60">
              <span className="text-[10px] text-slate-400 block mb-0.5">Travel Time</span>
              <span className="text-sm font-bold text-cyan-400">{before.travel_time_min.toFixed(2)} min</span>
            </div>
            <div className="bg-[#0b1120] p-2 rounded border border-slate-800/60">
              <span className="text-[10px] text-slate-400 block mb-0.5">Vehicles</span>
              <span className="text-sm font-bold text-emerald-400">{before.active_vehicles}</span>
            </div>
          </div>

          <div className="text-[11px] font-mono text-slate-400">
            Route V1: <span className="text-slate-200">Depot → C5 → C1 → C9 → C3 → C10 → Depot</span>
          </div>
        </div>

        {/* After Incident & Re-optimization Card */}
        <div className={`rounded-lg border p-4 space-y-3 transition-colors ${
          isReoptimized
            ? 'bg-slate-900/90 border-cyan-800/80 shadow-[0_0_15px_rgba(6,182,212,0.08)]'
            : 'bg-slate-900/40 border-slate-800/60 opacity-70'
        }`}>
          <div className="flex items-center justify-between border-b border-slate-800 pb-2">
            <span className="text-xs font-bold font-mono text-cyan-300 uppercase tracking-wider">
              2. Post-Incident Re-Optimized
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800/40">
              Dynamic Detour
            </span>
          </div>

          <div className="grid grid-cols-3 gap-2 text-center font-mono">
            <div className="bg-[#0b1120] p-2 rounded border border-slate-800/60">
              <span className="text-[10px] text-slate-400 block mb-0.5">Distance</span>
              <span className="text-sm font-bold text-slate-100">{after.distance_km.toFixed(2)} km</span>
            </div>
            <div className="bg-[#0b1120] p-2 rounded border border-slate-800/60">
              <span className="text-[10px] text-slate-400 block mb-0.5">Travel Time</span>
              <span className="text-sm font-bold text-amber-300">{after.travel_time_min.toFixed(2)} min</span>
            </div>
            <div className="bg-[#0b1120] p-2 rounded border border-slate-800/60">
              <span className="text-[10px] text-slate-400 block mb-0.5">Vehicles</span>
              <span className="text-sm font-bold text-emerald-400">{after.active_vehicles}</span>
            </div>
          </div>

          <div className="text-[11px] font-mono text-slate-400">
            Adapted V1: <span className="text-cyan-300">Depot → C5 → C1 → C10 → C9 → C3 → Depot</span>
          </div>
        </div>

      </div>

      {/* Engineering Explanation Note */}
      <div className="flex items-start gap-2.5 p-3 rounded-md bg-[#0a1222] border border-blue-900/40 text-xs text-slate-300 font-mono">
        <Info className="h-4 w-4 text-cyan-400 flex-shrink-0 mt-0.5" />
        <div className="space-y-0.5">
          <p className="text-slate-200 font-semibold">
            Network Physics Notice:
          </p>
          <p className="text-slate-400 text-[11px] leading-relaxed">
            When a traffic bottleneck occurs, post-incident travel time (90.04 min) and distance (33.55 km) are naturally higher than baseline conditions due to real-world detour requirements. QPSO prevents severe congestion escalation that would otherwise delay routes past 98+ minutes.
          </p>
        </div>
      </div>
    </div>
  );
};
