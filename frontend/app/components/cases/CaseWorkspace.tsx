"use client";

import React from 'react';
import { Network, FileText, CheckCircle, Activity, Play } from 'lucide-react';

export default function CaseWorkspace() {
  return (
    <div className="h-full flex flex-col space-y-6">
      
      {/* Top Bar / Status */}
      <div className="bg-phantasm-surface border border-phantasm-border rounded-xl p-6 flex flex-col md:flex-row justify-between items-start md:items-center shadow-lg">
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <h1 className="text-2xl font-bold text-gray-100">Case: PHT-8991</h1>
            <span className="bg-phantasm-cyan/10 text-phantasm-cyan border border-phantasm-cyan/30 px-3 py-1 rounded-full text-xs font-bold tracking-wide">
              ACTIVE
            </span>
          </div>
          <p className="text-gray-400 text-sm flex items-center">
            <FileText className="w-4 h-4 mr-2" />
            Authority: <strong className="ml-1 text-gray-200">Sec 94 BNSS (FIR-2026/08/891)</strong>
          </p>
        </div>
        
        <div className="mt-4 md:mt-0 flex flex-col items-end">
          <div className="flex items-center text-sm font-medium text-green-400 mb-1">
            <CheckCircle className="w-4 h-4 mr-1.5" />
            Lawful Status Verified
          </div>
          <p className="text-xs text-gray-500 font-mono">
            Seed: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa
          </p>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Graph Preview (Placeholder) */}
        <div className="lg:col-span-2 bg-phantasm-surface border border-phantasm-border rounded-xl shadow-lg relative overflow-hidden flex flex-col">
          <div className="bg-phantasm-border/30 px-4 py-3 border-b border-phantasm-border flex items-center justify-between">
            <div className="flex items-center">
              <Network className="w-5 h-5 text-gray-400 mr-2" />
              <h2 className="text-sm font-semibold text-gray-200">Graph Resolution Engine</h2>
            </div>
            <div className="flex space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500"></span>
              <span className="w-2.5 h-2.5 rounded-full bg-yellow-500"></span>
              <span className="w-2.5 h-2.5 rounded-full bg-green-500"></span>
            </div>
          </div>
          
          <div className="flex-1 flex items-center justify-center bg-[#050810] relative">
            {/* Grid background effect */}
            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgzMCwgNDUsIDc0LCAwLjIpIiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-50"></div>
            
            <div className="text-center z-10 p-8">
              <Activity className="w-12 h-12 text-phantasm-cyan/50 mx-auto mb-4 animate-pulse" />
              <p className="text-gray-400 text-sm max-w-md mx-auto">
                The engine is idle. Run an initial ingestion on the seed address to begin populating the Neo4j graph.
              </p>
            </div>
          </div>
        </div>

        {/* Guided NEXT STEP Card */}
        <div className="flex flex-col space-y-6">
          <div className="bg-gradient-to-b from-phantasm-surface to-[#0A0F1D] border border-phantasm-cyan/30 rounded-xl shadow-[0_0_20px_rgba(0,229,255,0.1)] p-6">
            <h3 className="text-phantasm-cyan font-bold tracking-wider text-sm mb-4">NEXT STEP</h3>
            
            <h4 className="text-lg font-semibold text-gray-100 mb-2">Ingest Seed Activity</h4>
            <p className="text-sm text-gray-400 mb-6 leading-relaxed">
              Fetch the complete transaction history for the seed address using the configured providers and cross-validation gate.
            </p>
            
            <button className="w-full bg-phantasm-cyan text-[#0A0F1D] font-bold py-3 rounded-lg flex items-center justify-center hover:bg-opacity-90 transition-all shadow-[0_0_10px_rgba(0,229,255,0.4)] group">
              <Play className="w-4 h-4 mr-2 fill-current" />
              START INGESTION
            </button>
            
            <div className="mt-4 pt-4 border-t border-phantasm-cyan/10">
              <div className="flex justify-between text-xs text-gray-500">
                <span>Estimated nodes:</span>
                <span className="font-mono text-gray-300">~14</span>
              </div>
            </div>
          </div>
          
          {/* Recent Activity Log Placeholder */}
          <div className="bg-phantasm-surface border border-phantasm-border rounded-xl p-5 flex-1">
            <h3 className="text-gray-400 font-semibold text-sm mb-4">Activity Log</h3>
            <div className="space-y-3">
              <div className="border-l-2 border-phantasm-amber pl-3 py-1">
                <p className="text-xs text-gray-500 mb-0.5">10:42 AM</p>
                <p className="text-sm text-gray-200">Case initialized with BNSS mandate.</p>
              </div>
              <div className="border-l-2 border-phantasm-border pl-3 py-1">
                <p className="text-xs text-gray-500 mb-0.5">10:42 AM</p>
                <p className="text-sm text-gray-400">Seed address validated (Bitcoin).</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
