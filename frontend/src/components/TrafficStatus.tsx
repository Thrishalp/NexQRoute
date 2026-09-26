import React from 'react';
import { ShieldCheck, AlertTriangle } from 'lucide-react';
import { TrafficStatusType } from '../types';

interface TrafficStatusProps {
  status: TrafficStatusType;
  level: string;
  activeIncidents: number;
}

export const TrafficStatus: React.FC<TrafficStatusProps> = ({
  status,
  level,
  activeIncidents
}) => {
  const isNormal = status === 'NORMAL';

  return (
    <div className={`rounded-lg p-4 border transition-all duration-300 ${
      isNormal
        ? 'bg-emerald-950/20 border-emerald-800/40 shadow-[0_0_20px_rgba(16,185,129,0.05)]'
        : 'bg-amber-950/30 border-amber-600/60 shadow-[0_0_25px_rgba(245,158,11,0.1)]'
    }`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {isNormal ? (
            <ShieldCheck className="h-5 w-5 text-emerald-400" />
          ) : (
            <AlertTriangle className="h-5 w-5 text-amber-400 animate-bounce" />
          )}
          <h3 className="text-xs font-bold uppercase tracking-wider font-mono text-slate-300">
            Traffic Status
          </h3>
        </div>
        
        {/* Pulsing state badge */}
        <div className="flex items-center gap-1.5">
          <span className={`inline-block h-2 w-2 rounded-full ${isNormal ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400 animate-ping'}`} />
          <span className={`text-xs font-mono font-bold tracking-wider ${isNormal ? 'text-emerald-400' : 'text-amber-400'}`}>
            {status}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs pt-1 border-t border-slate-800/60">
        <div>
          <span className="text-slate-400 block font-mono">Traffic Level</span>
          <span className={`font-semibold font-mono ${isNormal ? 'text-slate-200' : 'text-amber-300 font-bold'}`}>
            {level}
          </span>
        </div>
        <div>
          <span className="text-slate-400 block font-mono">Active Incidents</span>
          <span className={`font-semibold font-mono ${activeIncidents > 0 ? 'text-amber-400 font-bold' : 'text-emerald-400'}`}>
            {activeIncidents} {activeIncidents === 1 ? 'Incident' : 'Incidents'}
          </span>
        </div>
      </div>
    </div>
  );
};
