import React from 'react';
import { AlertOctagon, RefreshCw, RotateCcw } from 'lucide-react';
import { TrafficStatusType } from '../types';

interface ControlPanelProps {
  trafficStatus: TrafficStatusType;
  onSimulateIncident: () => void;
  onReoptimize: () => void;
  onReset: () => void;
  isOptimizing: boolean;
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  trafficStatus,
  onSimulateIncident,
  onReoptimize,
  onReset,
  isOptimizing
}) => {
  const hasIncident = trafficStatus === 'INCIDENT';

  return (
    <div className="rounded-lg bg-[#0d1424]/90 border border-slate-800 p-4 space-y-3 shadow-[0_0_15px_rgba(0,0,0,0.2)]">
      <div className="flex items-center justify-between">
        <h3 className="text-xs font-bold uppercase tracking-wider font-mono text-slate-300">
          Command Controls
        </h3>
        <span className="text-[10px] font-mono text-slate-500">
          DISPATCH CONSOLE
        </span>
      </div>

      <div className="space-y-2.5">
        
        {/* Primary Action: Simulate Traffic Incident */}
        <button
          onClick={onSimulateIncident}
          disabled={hasIncident || isOptimizing}
          className={`w-full flex items-center justify-center gap-2.5 py-2.5 px-4 rounded-md font-mono text-xs font-semibold tracking-wider transition-all duration-200 border cursor-pointer ${
            hasIncident
              ? 'bg-slate-800/60 border-slate-700/60 text-slate-500 cursor-not-allowed'
              : 'bg-amber-950/40 hover:bg-amber-900/50 active:bg-amber-950 text-amber-300 border-amber-600/70 hover:border-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.15)] hover:shadow-[0_0_20px_rgba(245,158,11,0.25)]'
          }`}
        >
          <AlertOctagon className="h-4 w-4 text-amber-400" />
          <span>SIMULATE TRAFFIC INCIDENT</span>
        </button>

        {/* Secondary Action: Re-optimize with QPSO */}
        <button
          onClick={onReoptimize}
          disabled={!hasIncident || isOptimizing}
          className={`w-full flex items-center justify-center gap-2.5 py-2.5 px-4 rounded-md font-mono text-xs font-semibold tracking-wider transition-all duration-200 border cursor-pointer ${
            isOptimizing
              ? 'bg-cyan-950/60 border-cyan-700 text-cyan-300 cursor-wait'
              : hasIncident
              ? 'bg-cyan-600 hover:bg-cyan-500 active:bg-cyan-700 text-slate-950 border-cyan-400 shadow-[0_0_20px_rgba(6,182,212,0.3)] animate-pulse'
              : 'bg-slate-800/40 border-slate-700/40 text-slate-500 cursor-not-allowed'
          }`}
        >
          <RefreshCw className={`h-4 w-4 ${isOptimizing ? 'animate-spin text-cyan-400' : 'text-slate-950'}`} />
          <span>{isOptimizing ? 'SOLVING WITH QPSO...' : 'RE-OPTIMIZE WITH QPSO'}</span>
        </button>

        {/* Tertiary Action: Reset Scenario */}
        <button
          onClick={onReset}
          disabled={isOptimizing}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-md bg-slate-900/90 hover:bg-slate-800 active:bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800 text-xs font-mono transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RotateCcw className="h-3.5 w-3.5" />
          <span>RESET SCENARIO</span>
        </button>

      </div>
    </div>
  );
};
