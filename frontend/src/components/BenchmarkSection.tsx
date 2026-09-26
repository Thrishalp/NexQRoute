import React from 'react';
import { BarChart3, TrendingDown, Zap, Clock, Route } from 'lucide-react';
import { BenchmarkData } from '../types';

interface BenchmarkSectionProps {
  benchmark: BenchmarkData;
}

export const BenchmarkSection: React.FC<BenchmarkSectionProps> = ({ benchmark }) => {
  // Calculations for bar widths relative to baseline (100%)
  const timeBaseline = benchmark.travel_time_baseline_min;
  const timeQpso = benchmark.travel_time_qpso_min;
  const timeQpsoPct = (timeQpso / timeBaseline) * 100;

  const distBaseline = benchmark.distance_baseline_km;
  const distQpso = benchmark.distance_qpso_km;
  const distQpsoPct = (distQpso / distBaseline) * 100;

  return (
    <div className="rounded-xl bg-[#0d1424]/90 border border-slate-800 p-5 shadow-[0_0_20px_rgba(0,0,0,0.25)] space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 pb-3 border-b border-slate-800/80">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-md bg-cyan-950/60 border border-cyan-800/60 text-cyan-400">
            <BarChart3 className="h-4 w-4" />
          </div>
          <div>
            <h3 className="font-mono text-sm font-bold text-slate-100 uppercase tracking-wider">
              Algorithm Benchmark
            </h3>
            <p className="text-xs text-slate-400">
              Greedy Baseline Routing vs. Discrete Quantum Particle Swarm Optimization
            </p>
          </div>
        </div>

        {/* Runtime Badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900 border border-slate-800 text-xs font-mono">
          <Zap className="h-3.5 w-3.5 text-cyan-400" />
          <span className="text-slate-400">QPSO Runtime:</span>
          <span className="font-bold text-emerald-400">{benchmark.runtime_sec.toFixed(3)} s</span>
        </div>
      </div>

      {/* Comparisons Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-1">
        
        {/* Metric 1: Travel Time */}
        <div className="rounded-lg bg-slate-900/60 border border-slate-800/80 p-4 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
              <Clock className="h-4 w-4 text-cyan-400" />
              <span className="font-semibold">Travel Time Comparison</span>
            </div>
            <span className="inline-flex items-center gap-1 text-xs font-mono font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800/50">
              <TrendingDown className="h-3.5 w-3.5" />
              -{benchmark.travel_time_improvement_pct.toFixed(2)}% Reduction
            </span>
          </div>

          {/* Bar 1: Baseline */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-slate-400">Baseline (Greedy)</span>
              <span className="text-slate-300 font-semibold">{timeBaseline.toFixed(2)} min</span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full rounded-full bg-slate-600 w-full" />
            </div>
          </div>

          {/* Bar 2: QPSO */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-cyan-400 font-semibold">QPSO (Optimized)</span>
              <span className="text-cyan-300 font-bold">{timeQpso.toFixed(2)} min</span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-500 shadow-[0_0_10px_rgba(6,182,212,0.5)] transition-all duration-700"
                style={{ width: `${timeQpsoPct}%` }}
              />
            </div>
          </div>
        </div>

        {/* Metric 2: Total Distance */}
        <div className="rounded-lg bg-slate-900/60 border border-slate-800/80 p-4 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-mono text-slate-300">
              <Route className="h-4 w-4 text-blue-400" />
              <span className="font-semibold">Distance Comparison</span>
            </div>
            <span className="inline-flex items-center gap-1 text-xs font-mono font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800/50">
              <TrendingDown className="h-3.5 w-3.5" />
              -{benchmark.distance_improvement_pct.toFixed(2)}% Reduction
            </span>
          </div>

          {/* Bar 1: Baseline */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-slate-400">Baseline (Greedy)</span>
              <span className="text-slate-300 font-semibold">{distBaseline.toFixed(2)} km</span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full rounded-full bg-slate-600 w-full" />
            </div>
          </div>

          {/* Bar 2: QPSO */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-blue-400 font-semibold">QPSO (Optimized)</span>
              <span className="text-blue-300 font-bold">{distQpso.toFixed(2)} km</span>
            </div>
            <div className="w-full h-3 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 shadow-[0_0_10px_rgba(59,130,246,0.5)] transition-all duration-700"
                style={{ width: `${distQpsoPct}%` }}
              />
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
