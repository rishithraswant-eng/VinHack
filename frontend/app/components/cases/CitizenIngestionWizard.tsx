"use client";

import React, { useState } from 'react';
import { 
  Search, 
  ArrowRight, 
  ArrowLeft, 
  Sparkles,
  CheckCircle2,
  Coins
} from 'lucide-react';

interface CitizenIngestionWizardProps {
  onBackToPortal?: () => void;
  onComplete: (caseId: string, seedAddress: string, disputedAmount: string, incidentType: string) => void;
}

const PRESET_ADDRESSES = [
  { label: "Ethereum Drainer", addr: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", chain: "ETH" },
  { label: "Bitcoin Mixer", addr: "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", chain: "BTC" },
  { label: "TRON Mule", addr: "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t", chain: "TRX" }
];

export default function CitizenIngestionWizard({ 
  onBackToPortal, 
  onComplete 
}: CitizenIngestionWizardProps) {
  const [seedAddress, setSeedAddress] = useState('');
  const [disputedAmount, setDisputedAmount] = useState('');

  const detectChain = (addr: string) => {
    if (!addr) return null;
    const clean = addr.trim();
    if (/^0x[a-fA-F0-9]{40}$/.test(clean)) return 'Ethereum (ERC-20)';
    if (/^(1|3)[a-zA-HJ-NP-Z0-9]{25,39}$/.test(clean) || /^(bc1)[a-zA-HJ-NP-Z0-9]{25,39}$/.test(clean)) return 'Bitcoin (UTXO)';
    if (/^T[A-Za-z1-9]{33}$/.test(clean)) return 'TRON (TRC-20)';
    if (/^[1-9A-HJ-NP-Za-km-z]{32,44}$/.test(clean)) return 'Solana (SPL)';
    return 'Custom / Multi-Chain';
  };

  const detectedChain = detectChain(seedAddress);
  const isValid = seedAddress.trim().length >= 26;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValid) return;
    const citizenCaseId = `CIT-${Math.floor(1000 + Math.random() * 9000)}`;
    onComplete(citizenCaseId, seedAddress.trim(), disputedAmount.trim(), "public_ingestion");
  };

  return (
    <div className="max-w-5xl mx-auto py-2 px-2">
      
      {/* Step Header Indicator */}
      <div className="flex items-center justify-between mb-8 pb-4 border-b border-slate-200">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-7 h-7 rounded-lg bg-[#1B729E] text-white font-mono text-xs font-bold shadow-xs">
            01
          </div>
          <div>
            <span className="text-[11px] uppercase tracking-wider text-slate-500 font-semibold block">Case Initialization</span>
            <div className="text-sm font-bold text-slate-900">
              Step 1 of 1: Target Address & Resolution Launch
            </div>
          </div>
        </div>

        {/* Actions & Progress Pills */}
        <div className="flex items-center space-x-4">
          {onBackToPortal && (
            <button
              type="button"
              onClick={onBackToPortal}
              className="px-3 py-1 rounded-lg border border-slate-300 hover:bg-slate-100 text-slate-700 text-xs font-semibold flex items-center transition shadow-2xs cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5 mr-1" />
              Switch Portal
            </button>
          )}

          <div className="flex items-center space-x-2">
            <div className="h-1.5 w-8 rounded-full bg-[#1B729E]" />
          </div>
        </div>
      </div>

      {/* Main Section */}
      <div className="animate-fadeIn">
        <h1 className="font-display text-3xl md:text-4xl font-extrabold uppercase tracking-wider text-slate-900 mb-2">
          TARGET BLOCKCHAIN SEED ADDRESS
        </h1>
        <p className="text-slate-600 text-sm mb-8">
          Seed the multigraph engine with suspect wallet address or illicit transfer destination.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* Suspect Wallet Card */}
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs">
            <div className="flex items-center justify-between mb-3">
              <label className="text-xs font-bold text-slate-700 uppercase tracking-wider font-mono">
                SUSPECT WALLET / SEED RECIPIENT ADDRESS <span className="text-rose-500">*</span>
              </label>
              {detectedChain && (
                <span className="text-[11px] font-mono text-[#1B729E] bg-sky-50 px-2 py-0.5 rounded border border-sky-200 font-bold">
                  {detectedChain}
                </span>
              )}
            </div>

            <div className="relative flex items-center">
              <div className="absolute left-3.5 text-slate-400">
                <Search className="w-4 h-4" />
              </div>
              <input
                type="text"
                required
                value={seedAddress}
                onChange={(e) => setSeedAddress(e.target.value)}
                placeholder="Enter Bitcoin, Ethereum, Tron, or Solana address..."
                className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 font-mono focus:border-[#1B729E] focus:ring-2 focus:ring-sky-100 outline-none transition"
              />
            </div>

            {/* Quick Preset Buttons */}
            <div className="mt-3 flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-semibold text-slate-400 font-mono">Presets:</span>
              {PRESET_ADDRESSES.map((preset, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setSeedAddress(preset.addr)}
                  className="px-2.5 py-1 rounded-md text-[11px] font-mono bg-slate-50 hover:bg-sky-50 hover:text-[#1B729E] border border-slate-200 hover:border-sky-300 transition text-slate-600 cursor-pointer"
                >
                  {preset.label} ({preset.chain})
                </button>
              ))}
            </div>
          </div>

          {/* Value & Finality Two-Column Card */}
          <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            
            {/* Disputed Value */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider font-mono mb-2">
                ESTIMATED DISPUTED VALUE (INR)
              </label>
              <div className="relative flex items-center">
                <span className="absolute left-3.5 text-slate-400 font-mono text-sm">₹</span>
                <input
                  type="text"
                  value={disputedAmount}
                  onChange={(e) => setDisputedAmount(e.target.value)}
                  placeholder="2,500,000"
                  className="w-full pl-8 pr-4 py-2.5 bg-slate-50/50 border border-slate-200 rounded-lg text-sm text-slate-900 font-mono focus:bg-white focus:border-[#1B729E] focus:ring-2 focus:ring-sky-100 outline-none transition"
                />
              </div>
            </div>

            {/* Finality Confirmations */}
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider font-mono mb-2">
                FINALITY CONFIRMATIONS
              </label>
              <div className="px-4 py-2.5 bg-slate-50/70 border border-slate-200 rounded-lg flex items-center justify-between text-xs font-mono text-slate-600">
                <span>Bitcoin: 6 Blocks</span>
                <span className="text-[#1B729E] font-semibold">Ethereum: 12 Epochs</span>
              </div>
            </div>
          </div>

          {/* Bottom Action Row */}
          <div className="flex items-center justify-between pt-4">
            {onBackToPortal ? (
              <button
                type="button"
                onClick={onBackToPortal}
                className="px-4 py-2.5 rounded-lg border border-slate-200 hover:bg-slate-100 text-slate-700 text-xs font-semibold flex items-center transition cursor-pointer"
              >
                <ArrowLeft className="w-3.5 h-3.5 mr-1.5" />
                Back
              </button>
            ) : <div />}

            <button
              type="submit"
              disabled={!isValid}
              className={`px-6 py-3 rounded-lg text-xs font-bold uppercase tracking-wider flex items-center space-x-2 transition-all shadow-xs ${
                isValid
                  ? 'bg-[#1B729E] hover:bg-[#155E82] text-white cursor-pointer shadow-sky-500/20'
                  : 'bg-slate-200 text-slate-400 cursor-not-allowed'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5 mr-1.5" />
              <span>Initialize Graph Engine</span>
              <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
