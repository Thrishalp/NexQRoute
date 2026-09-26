import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  icon: LucideIcon;
  subtext?: string;
  variant?: 'cyan' | 'blue' | 'emerald' | 'amber';
  highlightChange?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  unit,
  icon: Icon,
  subtext,
  variant = 'cyan',
  highlightChange = false
}) => {
  const variantStyles = {
    cyan: {
      border: 'border-cyan-900/40 hover:border-cyan-700/60',
      iconBg: 'bg-cyan-950/60 border-cyan-800/60 text-cyan-400',
      glow: 'shadow-[0_0_20px_rgba(6,182,212,0.06)]'
    },
    blue: {
      border: 'border-blue-900/40 hover:border-blue-700/60',
      iconBg: 'bg-blue-950/60 border-blue-800/60 text-blue-400',
      glow: 'shadow-[0_0_20px_rgba(59,130,246,0.06)]'
    },
    emerald: {
      border: 'border-emerald-900/40 hover:border-emerald-700/60',
      iconBg: 'bg-emerald-950/60 border-emerald-800/60 text-emerald-400',
      glow: 'shadow-[0_0_20px_rgba(16,185,129,0.06)]'
    },
    amber: {
      border: 'border-amber-900/50 hover:border-amber-700/80',
      iconBg: 'bg-amber-950/60 border-amber-800/80 text-amber-400',
      glow: 'shadow-[0_0_25px_rgba(245,158,11,0.12)]'
    }
  }[variant];

  return (
    <div className={`relative overflow-hidden rounded-lg bg-[#0d1424]/90 backdrop-blur-sm border ${variantStyles.border} p-4 transition-all duration-300 ${variantStyles.glow} ${highlightChange ? 'ring-1 ring-amber-500/50' : ''}`}>
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-[11px] uppercase tracking-wider font-semibold text-slate-400 font-mono">
            {label}
          </p>
          <div className="flex items-baseline gap-1.5">
            <span className="text-2xl lg:text-3xl font-bold font-mono text-slate-100 tracking-tight">
              {value}
            </span>
            {unit && (
              <span className="text-xs font-mono text-slate-400 uppercase">
                {unit}
              </span>
            )}
          </div>
          {subtext && (
            <p className="text-xs text-slate-500 flex items-center gap-1 pt-0.5">
              {subtext}
            </p>
          )}
        </div>
        <div className={`p-2.5 rounded-md border ${variantStyles.iconBg}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      
      {/* Subtle bottom telemetry accent line */}
      <div className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-cyan-500/20 to-transparent" />
    </div>
  );
};
