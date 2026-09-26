import React from 'react';
import { RefreshCw, CheckCircle2, ShieldAlert, Atom } from 'lucide-react';
import { TrafficStatusType } from '../types';

interface TrafficIncidentPanelProps {
  trafficStatus: TrafficStatusType;
  isOptimizing: boolean;
  optimizationStep: number;
  onReoptimize: () => void;
}

const OPTIMIZATION_STEPS = [
  "Updating road network weights...",
  "Recalculating travel-time matrix with OSMnx...",
  "Running Quantum Particle Swarm Optimization (QPSO)...",
  "Generating capacity-feasible discrete routes...",
  "Routes successfully re-optimized."
];

export const TrafficIncidentPanel: React.FC<TrafficIncidentPanelProps> = ({
  trafficStatus,
  isOptimizing,
  optimizationStep,
  onReoptimize
}) => {
  if (trafficStatus !== 'INCIDENT' && !isOptimizing) {
    return null;
  }

  return (
    <>
      {/* Incident Notification Banner */}
      {trafficStatus === 'INCIDENT' && !isOptimizing && (
        <div className="rounded-lg bg-gradient-to-r from-amber-950/80 via-red-950/60 to-amber-950/80 border border-amber-500/80 p-4 shadow-[0_0_25px_rgba(245,158,11,0.25)] flex flex-col sm:flex-row sm:items-center justify-between gap-3 animate-pulse">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-md bg-amber-500/20 text-amber-400 flex-shrink-0 mt-0.5">
              <ShieldAlert className="h-5 w-5" />
            </div>
            <div>
              <h4 className="font-mono text-sm font-bold text-amber-300">
                CRITICAL TRAFFIC INCIDENT DETECTED
              </h4>
              <p className="text-xs font-mono text-slate-300 mt-0.5">
                Traffic conditions changed on Gachibowli arterial link. Re-optimization recommended.
              </p>
            </div>
          </div>

          <button
            onClick={onReoptimize}
            className="flex items-center justify-center gap-2 px-4 py-2 rounded-md bg-cyan-500 hover:bg-cyan-400 active:bg-cyan-600 text-slate-950 font-mono text-xs font-bold tracking-wider transition-all shadow-[0_0_15px_rgba(6,182,212,0.4)] cursor-pointer flex-shrink-0"
          >
            <RefreshCw className="h-4 w-4" />
            <span>RE-OPTIMIZE ROUTES</span>
          </button>
        </div>
      )}

      {/* Multi-stage Optimization Progress Modal / Overlay */}
      {isOptimizing && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/85 backdrop-blur-md p-4">
          <div className="w-full max-w-lg rounded-xl bg-[#0b1325] border border-cyan-500/60 p-6 shadow-[0_0_50px_rgba(6,182,212,0.25)] space-y-6">
            
            {/* Modal Header */}
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-lg bg-cyan-950 border border-cyan-700 text-cyan-400">
                <Atom className="h-6 w-6 animate-spin-slow" />
              </div>
              <div>
                <h3 className="font-mono text-base font-bold text-slate-100">
                  Quantum-Inspired Re-Optimization
                </h3>
                <p className="text-xs text-slate-400 font-mono">
                  Continuous QPSO with Random-Key Route Decoding
                </p>
              </div>
            </div>

            {/* Stepper Progress */}
            <div className="space-y-3">
              {OPTIMIZATION_STEPS.map((step, idx) => {
                const isCompleted = optimizationStep > idx;
                const isCurrent = optimizationStep === idx;

                return (
                  <div
                    key={idx}
                    className={`flex items-center gap-3 p-2.5 rounded-lg border text-xs font-mono transition-all duration-300 ${
                      isCompleted
                        ? 'bg-emerald-950/30 border-emerald-800/50 text-emerald-300'
                        : isCurrent
                        ? 'bg-cyan-950/60 border-cyan-500/80 text-cyan-200 shadow-[0_0_12px_rgba(6,182,212,0.15)]'
                        : 'bg-slate-900/40 border-slate-800/60 text-slate-500'
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircle2 className="h-4 w-4 text-emerald-400 flex-shrink-0" />
                    ) : isCurrent ? (
                      <RefreshCw className="h-4 w-4 text-cyan-400 animate-spin flex-shrink-0" />
                    ) : (
                      <div className="h-4 w-4 rounded-full border border-slate-700 flex items-center justify-center text-[9px] text-slate-600 flex-shrink-0">
                        {idx + 1}
                      </div>
                    )}
                    <span className={isCurrent ? 'font-bold tracking-wide' : ''}>
                      {step}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Overall Progress Bar */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-[11px] font-mono text-slate-400">
                <span>Optimization Pipeline</span>
                <span className="text-cyan-400 font-semibold">
                  {Math.round(((optimizationStep + 1) / OPTIMIZATION_STEPS.length) * 100)}%
                </span>
              </div>
              <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300"
                  style={{
                    width: `${((optimizationStep + 1) / OPTIMIZATION_STEPS.length) * 100}%`
                  }}
                />
              </div>
            </div>

          </div>
        </div>
      )}
    </>
  );
};
