"use client";

import React from 'react';
import { 
  Hexagon, 
  Scale, 
  Building2, 
  Coins, 
  Network, 
  Settings, 
  LogOut, 
  CheckCircle2,
  Globe,
  ShieldCheck,
  ArrowLeftRight,
  User
} from 'lucide-react';

interface AppShellProps {
  children: React.ReactNode;
  currentStep?: number;
  onStepChange?: (step: number) => void;
  activeCase?: { caseId: string; seedAddress: string } | null;
  userRole?: 'citizen' | 'lea';
  officerDetails?: {
    officerName?: string;
    badgeNumber?: string;
    policeStation?: string;
  };
  onSwitchPortal?: () => void;
}

const LEA_STAGES = [
  { id: 1, label: "Statutory Reference", icon: Scale, subtitle: "Legal Mandate & FIR" },
  { id: 2, label: "Investigating Unit", icon: Building2, subtitle: "Police Station & Officer" },
  { id: 3, label: "Target Seed Address", icon: Coins, subtitle: "Suspect Wallet Address" },
  { id: 4, label: "Graph Resolution", icon: Network, subtitle: "On-Chain Attribution" },
];

const CITIZEN_STAGES = [
  { id: 1, label: "Target Seed Ingestion", icon: Coins, subtitle: "Suspect / Stolen Wallet" },
  { id: 4, label: "Graph Resolution", icon: Network, subtitle: "Attributed VASP Off-Ramp" },
];

export default function AppShell({ 
  children, 
  currentStep = 1, 
  onStepChange,
  activeCase,
  userRole = 'lea',
  officerDetails,
  onSwitchPortal
}: AppShellProps) {
  const isCitizen = userRole === 'citizen';
  const stages = isCitizen ? CITIZEN_STAGES : LEA_STAGES;
  const activeStage = activeCase ? 4 : currentStep;

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex overflow-hidden">
      
      {/* Sidebar - Clean Institutional Design */}
      <aside className="w-72 bg-white border-r border-slate-200 flex flex-col z-20 shrink-0 select-none shadow-xs">
        
        {/* Brand Header */}
        <div className="h-20 flex items-center px-6 border-b border-slate-200 space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center shadow-xs overflow-hidden p-1 shrink-0">
            <img 
              src="/wolf-icon-transparent.png" 
              alt="PHANTASM Logo" 
              className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(0,229,255,0.4)]"
            />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-1.5">
              <span className="text-base tracking-tight font-bold text-slate-900">PHANTASM</span>
            </div>
            <span className="text-[10px] font-mono tracking-wider text-slate-500 uppercase font-semibold">
              {isCitizen ? "CITIZEN TRACE PORTAL" : "LEGAL FORENSICS SUITE"}
            </span>
          </div>
        </div>
        
        {/* Navigation Stages */}
        <nav className="flex-1 py-6 px-3.5 space-y-1.5">
          <div className="px-3 pb-2 text-[11px] font-semibold uppercase tracking-wider text-slate-400">
            {isCitizen ? "Direct Ingestion Steps" : "Case Setup Steps"}
          </div>

          {stages.map((stage) => {
            const Icon = stage.icon;
            const isActive = activeStage === stage.id;
            const isCompleted = activeStage > stage.id;
            const isClickable = stage.id <= (activeCase ? 4 : (isCitizen ? 1 : 3)) && onStepChange;

            return (
              <button
                key={stage.id}
                type="button"
                disabled={!isClickable && stage.id !== activeStage}
                onClick={() => isClickable && onStepChange?.(stage.id)}
                className={`w-full flex items-center justify-between px-3.5 py-3 rounded-xl transition-all duration-150 text-left group ${
                  isActive
                    ? 'bg-sky-50 border border-sky-200 text-[#1B729E] font-semibold shadow-xs'
                    : isCompleted
                      ? 'bg-transparent text-slate-700 hover:bg-slate-100 hover:text-slate-900'
                      : 'bg-transparent text-slate-400 hover:text-slate-600 cursor-not-allowed'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className={`transition-colors ${
                    isActive ? 'text-[#1B729E]' : isCompleted ? 'text-slate-600' : 'text-slate-400'
                  }`}>
                    <Icon className="w-4 h-4" strokeWidth={isActive ? 2.2 : 1.8} />
                  </div>
                  <div>
                    <span className={`block text-xs font-semibold ${
                      isActive ? 'text-[#1B729E]' : 'text-slate-800'
                    }`}>
                      {stage.label}
                    </span>
                    <span className="block text-[11px] text-slate-500 font-normal">
                      {stage.subtitle}
                    </span>
                  </div>
                </div>

                {/* Status Indicator */}
                <div>
                  {isActive && (
                    <span className="inline-block w-2 h-2 rounded-full bg-[#1B729E]" />
                  )}
                  {isCompleted && !isActive && (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  )}
                </div>
              </button>
            );
          })}
        </nav>
        
        {/* Bottom Switch Portal Link */}
        <div className="p-3.5 border-t border-slate-200 space-y-1">
          {onSwitchPortal && (
            <button 
              type="button"
              onClick={onSwitchPortal}
              className="w-full flex items-center justify-between px-3 py-2 text-slate-700 hover:text-[#1B729E] hover:bg-sky-50 rounded-lg transition-colors group text-xs font-medium border border-slate-200"
            >
              <div className="flex items-center">
                <ArrowLeftRight className="w-4 h-4 mr-2.5 text-slate-500 group-hover:text-[#1B729E]" />
                <span>Switch Portal Tier</span>
              </div>
              <span className="text-[10px] font-mono uppercase text-slate-400">
                {isCitizen ? "→ LEA" : "→ Citizen"}
              </span>
            </button>
          )}

          <div className="px-3 pt-2 text-[10px] text-slate-400 font-mono text-center">
            {isCitizen ? "Public Mode · No FIR Required" : "Section 94 BNSS Compliant"}
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col relative overflow-hidden bg-slate-50">
        
        {/* Top Header */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 z-10 shadow-2xs">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="font-display text-lg font-bold tracking-wider uppercase text-slate-900">
                {isCitizen ? "Citizen Asset Investigation" : "Law Enforcement Suite"}
              </h2>
              <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded font-bold border ${
                isCitizen 
                  ? 'bg-sky-50 text-[#1B729E] border-sky-200' 
                  : 'bg-indigo-50 text-indigo-700 border-indigo-200'
              }`}>
                {isCitizen ? "Citizen Mode" : "Official LEA"}
              </span>
            </div>
            <p className="text-[11px] text-slate-500">
              {isCitizen ? "Direct Blockchain Ingestion & Algorithmic Attribution" : "Lawful Attribution & Crypto Asset Tracking"}
            </p>
          </div>

          {/* User / Officer Session Indicator */}
          <div className="flex items-center space-x-3.5">
            {isCitizen ? (
              <div className="flex items-center space-x-2.5 bg-slate-100/80 px-3 py-1.5 rounded-xl border border-slate-200">
                <div className="w-7 h-7 rounded-lg bg-sky-100 text-[#1B729E] flex items-center justify-center font-bold text-xs">
                  <User className="w-4 h-4" />
                </div>
                <div className="flex flex-col">
                  <span className="text-xs font-semibold text-slate-800">Public Investigator</span>
                  <span className="text-[10px] text-slate-500 font-mono">Citizen Ingestion</span>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-2.5">
                <div className="flex flex-col items-end">
                  <span className="text-xs font-semibold text-slate-800">
                    {officerDetails?.officerName ? officerDetails.officerName : "Authorized Officer (IO)"}
                  </span>
                  <span className="text-[11px] text-[#1B729E] font-mono font-medium">
                    {officerDetails?.badgeNumber ? `Badge #${officerDetails.badgeNumber}` : "LEA Unit"}
                  </span>
                </div>
                <div className="w-8 h-8 rounded-lg bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-700 font-mono text-xs font-semibold">
                  {officerDetails?.officerName 
                    ? officerDetails.officerName.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() 
                    : "IO"}
                </div>
              </div>
            )}

            {onSwitchPortal && (
              <button 
                onClick={onSwitchPortal}
                className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors" 
                title="Switch Portal or Logout"
              >
                <LogOut className="w-4 h-4" />
              </button>
            )}
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-8 relative">
          {children}
        </main>
      </div>
      
    </div>
  );
}

