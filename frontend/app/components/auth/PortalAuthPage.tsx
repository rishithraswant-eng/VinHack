"use client";

import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Scale, 
  User, 
  Globe, 
  Zap, 
  FileText, 
  ArrowRight, 
  CheckCircle2, 
  Hexagon, 
  Building2, 
  Sparkles,
  ArrowLeft,
  BadgeCheck,
  Lock
} from 'lucide-react';

export interface LeaOfficerDetails {
  officerName: string;
  badgeNumber: string;
  policeStation: string;
  rank: string;
}

interface PortalAuthPageProps {
  onSelectCitizen: () => void;
  onSelectLea: (officer: LeaOfficerDetails) => void;
  onBackToLanding: () => void;
}

export default function PortalAuthPage({ 
  onSelectCitizen, 
  onSelectLea,
  onBackToLanding
}: PortalAuthPageProps) {
  // LEA Form state - clean user input
  const [officerName, setOfficerName] = useState("");
  const [badgeNumber, setBadgeNumber] = useState("");
  const [policeStation, setPoliceStation] = useState("");
  const [rank, setRank] = useState("");

  const handleLeaSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSelectLea({
      officerName: officerName.trim(),
      badgeNumber: badgeNumber.trim(),
      policeStation: policeStation.trim(),
      rank: rank.trim()
    });
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex flex-col justify-between relative overflow-hidden font-sans select-none">
      
      {/* Subtle Dot Mesh Background */}
      <div className="absolute inset-0 [background-image:radial-gradient(#CBD5E1_1px,transparent_1px)] [background-size:24px_24px] pointer-events-none opacity-60" />
      
      {/* Top Institutional Header */}
      <header className="relative z-10 w-full bg-white border-b border-slate-200 px-6 sm:px-8 py-4 flex items-center justify-between shadow-2xs">
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center shadow-xs overflow-hidden p-1 shrink-0">
            <img 
              src="/wolf-icon-transparent.png" 
              alt="PHANTASM Logo" 
              className="w-full h-full object-contain filter drop-shadow-[0_0_8px_rgba(0,229,255,0.4)]"
            />
          </div>
          <div>
            <div className="text-base font-bold tracking-tight text-slate-900">
              PHANTASM
            </div>
            <p className="text-[10px] font-mono tracking-wider text-slate-500 uppercase font-semibold">
              NATIONAL FORENSIC ATTRIBUTION GATEWAY
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={onBackToLanding}
          className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 hover:text-slate-900 bg-white hover:bg-slate-50 border border-slate-300 transition flex items-center shadow-2xs cursor-pointer"
        >
          <ArrowLeft className="w-3.5 h-3.5 mr-1.5 text-slate-500" />
          Back to Overview
        </button>
      </header>

      {/* Main Content Area */}
      <main className="relative z-10 max-w-6xl mx-auto w-full px-6 py-8 sm:py-10 flex-1 flex flex-col justify-center">
        
        {/* Title & Institutional Header */}
        <div className="text-center max-w-3xl mx-auto mb-8 sm:mb-10">
          <h1 className="font-display text-3xl sm:text-4xl lg:text-5xl font-extrabold uppercase tracking-wider text-slate-900 mb-3">
            Choose Your Investigation Gateway
          </h1>
          <p className="text-xs sm:text-sm text-slate-600 max-w-2xl mx-auto leading-relaxed">
            PHANTASM provides tailored workflows: A direct, instant-ingestion portal for individual citizens and victims, alongside a full statutory compliance suite for Law Enforcement Agencies.
          </p>
        </div>

        {/* Dual Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
          
          {/* Card 1: Citizen / Public Gateway */}
          <div className="bg-white border border-slate-200 hover:border-[#1B729E]/60 rounded-2xl p-7 sm:p-8 flex flex-col justify-between shadow-xs hover:shadow-md transition-all duration-200 group relative">
            <div>
              {/* Title & Icon */}
              <div className="flex items-start space-x-4 mb-4">
                <div className="w-12 h-12 rounded-xl bg-sky-50 border border-sky-200 flex items-center justify-center text-[#1B729E] shrink-0 shadow-xs">
                  <User className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 tracking-tight">
                    Normal Citizen / Victim Tracer
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    For individuals, fraud victims, and public compliance researchers
                  </p>
                </div>
              </div>

              {/* Features List */}
              <div className="space-y-3 py-4 border-t border-slate-100 my-4 text-xs text-slate-700">
                <div className="flex items-start space-x-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>
                    <strong className="text-slate-900 font-semibold">Direct Wallet Bypass:</strong> Skip FIR numbers, police station, and officer designation fields.
                  </span>
                </div>
                <div className="flex items-start space-x-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>
                    <strong className="text-slate-900 font-semibold">Instant Graph Resolution:</strong> Run Hawkes TPP & GNN algorithms to pinpoint receiving exchange VASPs.
                  </span>
                </div>
                <div className="flex items-start space-x-2.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>
                    <strong className="text-slate-900 font-semibold">Public Verification Dossier:</strong> Download self-verifying algorithmic report with Merkle proof stamps.
                  </span>
                </div>
              </div>
            </div>

            {/* CTA Button */}
            <div className="pt-4 border-t border-slate-100">
              <button
                type="button"
                onClick={onSelectCitizen}
                className="w-full py-3.5 px-6 rounded-xl bg-[#1B729E] hover:bg-[#155E82] text-white font-bold text-xs uppercase tracking-wider flex items-center justify-center space-x-2 shadow-xs transition hover:scale-[1.01] cursor-pointer"
              >
                <span>Continue as Normal Citizen</span>
                <ArrowRight className="w-4 h-4" />
              </button>
              <p className="text-[11px] text-center text-slate-400 mt-2.5">
                No police credentials or legal authorization required
              </p>
            </div>
          </div>

          {/* Card 2: Law Enforcement Agency (LEA) Portal */}
          <div className="bg-white border border-slate-200 hover:border-indigo-400/80 rounded-2xl p-7 sm:p-8 flex flex-col justify-between shadow-xs hover:shadow-md transition-all duration-200 group relative">
            <div>
              {/* Title & Icon */}
              <div className="flex items-start space-x-4 mb-4">
                <div className="w-12 h-12 rounded-xl bg-indigo-50 border border-indigo-200 flex items-center justify-center text-indigo-700 shrink-0 shadow-xs">
                  <Scale className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-slate-900 tracking-tight">
                    LEA & Judicial Portal
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    For Police Cyber Cells, ED, FIU-IND, and Court-Appointed Forensics
                  </p>
                </div>
              </div>

              {/* Officer Form */}
              <form onSubmit={handleLeaSubmit} className="space-y-3 pt-3 text-xs">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-700 mb-1">
                      Officer Name & Rank
                    </label>
                    <input 
                      type="text" 
                      value={officerName}
                      onChange={(e) => setOfficerName(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-300 text-slate-900 outline-none focus:bg-white focus:border-[#1B729E] focus:ring-2 focus:ring-sky-100 text-xs transition"
                      placeholder="e.g. Inspector A. Sharma"
                    />
                  </div>
                  <div>
                    <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-700 mb-1">
                      Badge / Officer ID
                    </label>
                    <input 
                      type="text" 
                      value={badgeNumber}
                      onChange={(e) => setBadgeNumber(e.target.value)}
                      className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-300 text-slate-900 font-mono outline-none focus:bg-white focus:border-[#1B729E] focus:ring-2 focus:ring-sky-100 text-xs transition"
                      placeholder="e.g. SHM-8891"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-700 mb-1">
                    Police Station / Unit
                  </label>
                  <input 
                    type="text" 
                    value={policeStation}
                    onChange={(e) => setPoliceStation(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-300 text-slate-900 outline-none focus:bg-white focus:border-[#1B729E] focus:ring-2 focus:ring-sky-100 text-xs transition"
                    placeholder="e.g. Cyber Crime Cell, New Delhi"
                  />
                </div>

                {/* Submit Action */}
                <div className="pt-2">
                  <button
                    type="submit"
                    className="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-indigo-700 to-[#1B729E] hover:from-indigo-800 hover:to-[#155E82] text-white font-bold text-xs uppercase tracking-wider flex items-center justify-center space-x-2 shadow-xs transition hover:scale-[1.01] cursor-pointer"
                  >
                    <span>Authenticate & Open LEA Suite</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                  <p className="text-[11px] text-center text-slate-400 mt-2.5">
                    Unlocks 3-Stage Case Setup (Statutory Mandate, FIR, IO Seal)
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </main>

      {/* Institutional Footer */}
      <footer className="relative z-10 w-full bg-white border-t border-slate-200 px-6 sm:px-8 py-3.5 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500 gap-2">
        <div className="flex items-center space-x-2">
          <BadgeCheck className="w-4 h-4 text-[#1B729E]" />
          <span>PHANTASM — Ministry of Home Affairs / I4C Portal</span>
        </div>
        <div className="font-mono text-slate-500">
          Compliant with Sec 94 BNSS & Sec 63 BSA / 65B IEA
        </div>
      </footer>
    </div>
  );
}
