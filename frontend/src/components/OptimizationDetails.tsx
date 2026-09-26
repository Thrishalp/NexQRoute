import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Atom, HelpCircle } from 'lucide-react';

export const OptimizationDetails: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="rounded-xl bg-[#0d1424]/90 border border-slate-800 shadow-[0_0_20px_rgba(0,0,0,0.25)] overflow-hidden">
      {/* Toggle Header */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 bg-slate-900/60 hover:bg-slate-900/90 transition-colors text-left cursor-pointer border-b border-slate-800/80"
      >
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-md bg-cyan-950/60 border border-cyan-800/60 text-cyan-400">
            <Atom className="h-4 w-4" />
          </div>
          <div>
            <h3 className="font-mono text-xs font-bold text-slate-100 uppercase tracking-wider">
              Optimization Details & Formulation
            </h3>
            <p className="text-[11px] text-slate-400">
              Technical specifications of the underlying metaheuristic model
            </p>
          </div>
        </div>

        <div className="p-1 rounded-md bg-slate-800 text-slate-300">
          {isOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </div>
      </button>

      {/* Accordion Content */}
      {isOpen && (
        <div className="p-5 space-y-4 font-mono text-xs">
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            
            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Problem Formulation</span>
              <span className="font-semibold text-slate-200">Capacitated Vehicle Routing Problem (CVRP)</span>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Core Optimizer</span>
              <span className="font-semibold text-cyan-400">Quantum Particle Swarm Optimization (QPSO)</span>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Solution Encoding</span>
              <span className="font-semibold text-slate-200">Random-Key Continuous-to-Discrete Encoding</span>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Operational Constraints</span>
              <span className="font-semibold text-slate-200">Vehicle Capacity (40 units / vehicle)</span>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Cost Function Objective</span>
              <span className="font-semibold text-slate-200">Distance + Traffic-adjusted Travel Time</span>
            </div>

            <div className="bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <span className="text-slate-400 block text-[10px] uppercase">Road Network Engine</span>
              <span className="font-semibold text-slate-200">OpenStreetMap / OSMnx (Gachibowli Graph)</span>
            </div>

          </div>

          {/* Academic Context Alert */}
          <div className="flex items-start gap-2.5 p-3 rounded-lg bg-cyan-950/30 border border-cyan-800/40 text-cyan-200">
            <HelpCircle className="h-4 w-4 text-cyan-400 flex-shrink-0 mt-0.5" />
            <div className="text-[11px] leading-relaxed">
              <span className="font-bold text-cyan-300">Methodological Note: </span>
              QPSO is a quantum-inspired classical optimization algorithm utilizing quantum wave function mechanics to explore global solution spaces without getting trapped in local optima. <span className="underline decoration-cyan-500">No quantum computer is required</span>; it runs natively on standard classical CPU/GPU infrastructure.
            </div>
          </div>

        </div>
      )}
    </div>
  );
};
