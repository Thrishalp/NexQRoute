import React from 'react';
import { TrafficStatusType } from '../types';

interface LegendProps {
  trafficStatus: TrafficStatusType;
}

export const Legend: React.FC<LegendProps> = ({ trafficStatus }) => {
  return (
    <div className="bg-[#0b1220]/90 backdrop-blur-md border border-slate-800 rounded-lg p-3 text-xs font-mono shadow-xl space-y-2">
      <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-1">
        Map Legend
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 items-center">
        
        {/* Depot */}
        <div className="flex items-center gap-2">
          <div className="w-3.5 h-3.5 rounded-full bg-blue-500 border border-blue-300 shadow-[0_0_8px_rgba(59,130,246,0.6)] flex items-center justify-center text-[8px] font-bold text-white">
            D
          </div>
          <span className="text-slate-300">Depot Hub</span>
        </div>

        {/* Customer */}
        <div className="flex items-center gap-2">
          <div className="w-3.5 h-3.5 rounded bg-slate-900 border border-cyan-400 shadow-[0_0_6px_rgba(6,182,212,0.4)] flex items-center justify-center text-[8px] text-cyan-300 font-bold">
            C
          </div>
          <span className="text-slate-300">Customer</span>
        </div>

        {/* Vehicle V1 Route */}
        <div className="flex items-center gap-2">
          <div className="w-4 h-1 rounded bg-[#06b6d4] shadow-[0_0_6px_#06b6d4]" />
          <span className="text-slate-300">Route V1</span>
        </div>

        {/* Vehicle V2 Route */}
        <div className="flex items-center gap-2">
          <div className="w-4 h-1 rounded bg-[#3b82f6] shadow-[0_0_6px_#3b82f6]" />
          <span className="text-slate-300">Route V2</span>
        </div>

        {/* Traffic Incident */}
        <div className="flex items-center gap-2">
          <div className={`w-4 h-1 border-b-2 border-dashed border-red-500 shadow-[0_0_8px_#ef4444] ${trafficStatus === 'INCIDENT' ? 'animate-pulse' : 'opacity-40'}`} />
          <span className={trafficStatus === 'INCIDENT' ? 'text-red-400 font-semibold' : 'text-slate-500'}>
            Incident Zone
          </span>
        </div>

      </div>
    </div>
  );
};
