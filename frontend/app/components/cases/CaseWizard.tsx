"use client";

import React, { useState } from 'react';
import { ShieldCheck, Search, Link2, AlertCircle, ArrowRight } from 'lucide-react';

export default function CaseWizard() {
  const [authority, setAuthority] = useState({
    statuteRef: '',
    firNumber: '',
    policeStation: '',
    ioDesignation: ''
  });

  const [seedAddress, setSeedAddress] = useState('');
  
  const isAuthorityValid = authority.statuteRef.trim() !== '' && 
                           authority.firNumber.trim() !== '' && 
                           authority.policeStation.trim() !== '' && 
                           authority.ioDesignation.trim() !== '';

  const detectChain = (addr: string) => {
    if (!addr) return null;
    if (addr.startsWith('0x')) return 'Ethereum';
    if (addr.startsWith('1') || addr.startsWith('3') || addr.toLowerCase().startsWith('bc1')) return 'Bitcoin';
    return 'Unknown';
  };

  const detectedChain = detectChain(seedAddress);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Initialize New Investigation</h1>
        <p className="text-gray-400">Establish lawful authority and seed the graph resolution engine.</p>
      </div>

      <div className="space-y-8">
        {/* Authority Gate */}
        <div className="bg-phantasm-surface border border-phantasm-border rounded-xl overflow-hidden shadow-lg shadow-black/50">
          <div className="bg-phantasm-border/30 px-6 py-4 border-b border-phantasm-border flex items-center">
            <ShieldCheck className="w-5 h-5 text-phantasm-amber mr-3" />
            <h2 className="text-lg font-semibold tracking-wide text-gray-100">Statutory Authority Gate</h2>
          </div>
          
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">Statutory Reference <span className="text-phantasm-amber">*</span></label>
              <select 
                className="w-full bg-[#0A0F1D] border border-phantasm-border rounded-lg px-4 py-2.5 text-gray-100 focus:outline-none focus:border-phantasm-cyan transition-colors"
                value={authority.statuteRef}
                onChange={e => setAuthority({...authority, statuteRef: e.target.value})}
              >
                <option value="">Select Reference...</option>
                <option value="Sec 94 BNSS">Section 94 BNSS</option>
                <option value="Sec 79(3)(b) IT Act">Section 79(3)(b) IT Act</option>
              </select>
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">FIR / DD Number <span className="text-phantasm-amber">*</span></label>
              <input 
                type="text" 
                placeholder="e.g., FIR-2026/08/891"
                className="w-full bg-[#0A0F1D] border border-phantasm-border rounded-lg px-4 py-2.5 text-gray-100 focus:outline-none focus:border-phantasm-cyan transition-colors"
                value={authority.firNumber}
                onChange={e => setAuthority({...authority, firNumber: e.target.value})}
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">Police Station / Unit <span className="text-phantasm-amber">*</span></label>
              <input 
                type="text" 
                placeholder="e.g., Cyber Cell, Delhi"
                className="w-full bg-[#0A0F1D] border border-phantasm-border rounded-lg px-4 py-2.5 text-gray-100 focus:outline-none focus:border-phantasm-cyan transition-colors"
                value={authority.policeStation}
                onChange={e => setAuthority({...authority, policeStation: e.target.value})}
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-400">IO Designation & ID <span className="text-phantasm-amber">*</span></label>
              <input 
                type="text" 
                placeholder="e.g., Inspector, ID: 8891"
                className="w-full bg-[#0A0F1D] border border-phantasm-border rounded-lg px-4 py-2.5 text-gray-100 focus:outline-none focus:border-phantasm-cyan transition-colors"
                value={authority.ioDesignation}
                onChange={e => setAuthority({...authority, ioDesignation: e.target.value})}
              />
            </div>
          </div>
          
          {!isAuthorityValid && (
            <div className="px-6 pb-6">
              <div className="bg-phantasm-amber/10 border border-phantasm-amber/30 rounded-lg p-3 flex items-start">
                <AlertCircle className="w-5 h-5 text-phantasm-amber mt-0.5 mr-3 shrink-0" />
                <p className="text-sm text-phantasm-amber/90 leading-relaxed">
                  You must establish lawful authority before seeding addresses into the graph engine.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Seed Address Configuration */}
        <div className={`transition-all duration-300 ${!isAuthorityValid ? 'opacity-50 pointer-events-none' : 'opacity-100'}`}>
          <div className="bg-phantasm-surface border border-phantasm-border rounded-xl overflow-hidden shadow-lg shadow-black/50">
            <div className="bg-phantasm-border/30 px-6 py-4 border-b border-phantasm-border flex items-center">
              <Link2 className="w-5 h-5 text-phantasm-cyan mr-3" />
              <h2 className="text-lg font-semibold tracking-wide text-gray-100">Seed Address Configuration</h2>
            </div>
            
            <div className="p-6">
              <div className="space-y-2 relative">
                <label className="text-sm font-medium text-gray-400">Target Address</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Search className="w-5 h-5 text-gray-500" />
                  </div>
                  <input 
                    type="text" 
                    placeholder="Enter Bitcoin or Ethereum address..."
                    className="w-full bg-[#0A0F1D] border border-phantasm-border rounded-lg pl-12 pr-4 py-3 text-gray-100 font-mono text-sm focus:outline-none focus:border-phantasm-cyan transition-colors"
                    value={seedAddress}
                    onChange={e => setSeedAddress(e.target.value)}
                  />
                  {detectedChain && (
                    <div className="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                      <span className={`text-xs font-bold px-2 py-1 rounded border ${
                        detectedChain === 'Bitcoin' ? 'bg-[#F7931A]/10 text-[#F7931A] border-[#F7931A]/30' : 
                        detectedChain === 'Ethereum' ? 'bg-[#627EEA]/10 text-[#627EEA] border-[#627EEA]/30' : 
                        'bg-gray-800 text-gray-400 border-gray-600'
                      }`}>
                        {detectedChain}
                      </span>
                    </div>
                  )}
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  Auto-detects Bitcoin (Base58/Bech32/Bech32m) and Ethereum (0x).
                </p>
              </div>

              <div className="mt-8 flex justify-end">
                <button 
                  disabled={!isAuthorityValid || !seedAddress}
                  className="bg-phantasm-cyan text-[#0A0F1D] font-bold px-6 py-3 rounded-lg flex items-center transition-all hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(0,229,255,0.3)] disabled:shadow-none"
                >
                  INITIALIZE GRAPH ENGINE
                  <ArrowRight className="w-5 h-5 ml-2" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
