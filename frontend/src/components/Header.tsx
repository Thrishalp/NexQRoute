import React from 'react';
import { RotateCcw, Activity, MapPin, Zap } from 'lucide-react';
import { TrafficStatusType } from '../types';

interface HeaderProps {
  trafficStatus: TrafficStatusType;
  onReset: () => void;
  isOptimizing: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  trafficStatus,
  onReset,
  isOptimizing
}) => {
  return (
    <header className="border-b border-slate-800 bg-[#0a0f1d]/90 backdrop-blur-md sticky top-0 z-30 px-4 lg:px-6 py-3">
      <div className="max-w-[1700px] mx-auto flex flex-col md:flex-row md:items-center md:justify-between gap-3">
        
        {/* Left: Branding */}
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-600/30 border border-cyan-500/40 flex items-center justify-center text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.15)]">
            <Zap className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-wider text-slate-100 font-mono">
                Q-ROUTE <span className="text-cyan-400">AI</span>
              </h1>
              <span className="px-2 py-0.5 text-[10px] uppercase font-semibold tracking-wider rounded bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">
                Command Center
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Quantum-Inspired Intelligent Traffic Route Optimization
            </p>
          </div>
        </div>

        {/* Center/Right: Telemetry Status Indicators */}
        <div className="flex items-center flex-wrap gap-2.5 sm:gap-4 text-xs font-mono">
          
          {/* System Status */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900/90 border border-slate-800">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-slate-400">System:</span>
            <span className="font-semibold text-emerald-400 tracking-wide">ONLINE</span>
          </div>

          {/* Road Network */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900/90 border border-slate-800">
            <MapPin className="h-3.5 w-3.5 text-cyan-400" />
            <span className="text-slate-400">Network:</span>
            <span className="font-medium text-slate-200">Gachibowli, HYD</span>
          </div>

          {/* Traffic Status */}
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-md border transition-colors ${
            trafficStatus === 'NORMAL'
              ? 'bg-emerald-950/30 border-emerald-800/60 text-emerald-400'
              : 'bg-amber-950/40 border-amber-600/80 text-amber-400 shadow-[0_0_12px_rgba(245,158,11,0.2)]'
          }`}>
            <Activity className="h-3.5 w-3.5" />
            <span className="text-slate-400">Traffic:</span>
            <span className="font-bold tracking-wider">{trafficStatus}</span>
          </div>

          {/* Reset Scenario Button */}
          <button
            onClick={onReset}
            disabled={isOptimizing}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-slate-800 hover:bg-slate-700 active:bg-slate-900 text-slate-300 hover:text-white border border-slate-700 text-xs font-sans transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            title="Reset to default optimized scenario"
          >
            <RotateCcw className="h-3.5 w-3.5 text-slate-400" />
            <span>Reset Scenario</span>
          </button>

        </div>

      </div>
    </header>
  );
};
