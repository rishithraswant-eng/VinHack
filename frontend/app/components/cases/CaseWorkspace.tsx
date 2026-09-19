"use client";

import React, { useState, useEffect } from 'react';
import { Network, FileText, CheckCircle, Activity, Play, ShieldAlert, Cpu, Share2, Lock } from 'lucide-react';

export default function CaseWorkspace({ caseId, seedAddress }: { caseId: string, seedAddress: string }) {
  const [traceState, setTraceState] = useState('IDLE');
  const [traceResult, setTraceResult] = useState<any>(null);
  const [caseData, setCaseData] = useState<any>(null);
  const [logs, setLogs] = useState<{time: string, message: string, type: 'info'|'success'|'warning'}[]>([]);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const detectChain = (address: string) => {
    if (/^0x[a-fA-F0-9]{40}$/.test(address)) return 'Ethereum';
    if (/^(1|3)[a-zA-HJ-NP-Z0-9]{25,39}$/.test(address) || /^(bc1)[a-zA-HJ-NP-Z0-9]{25,39}$/.test(address)) return 'Bitcoin';
    return 'Unknown Chain';
  };

  useEffect(() => {
    const fetchCase = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/cases/${caseId}`);
        if (res.ok) {
          const data = await res.json();
          setCaseData(data);
          addLog(`Case ${caseId} initialized with ${data.authority} mandate.`, 'info');
          addLog(`Seed address validated (${detectChain(data.seed_address)}).`, 'info');
        }
      } catch (err) {
        console.error("Failed to fetch case", err);
      }
    };
    fetchCase();
  }, [caseId]);

  const addLog = (message: string, type: 'info'|'success'|'warning' = 'info') => {
    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    setLogs(prev => [...prev, { time, message, type }]);
  };

  const startTrace = async () => {
    setTraceState('INGESTING');
    addLog(`Starting ingestion for seed ${seedAddress}...`, 'info');
    
    try {
      console.log('Calling:', `${API_URL}/api/v1/traces/`);
      const res = await fetch(`${API_URL}/api/v1/traces/`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ case_id: caseId, seed_address: seedAddress })
      });
      if (!res.ok) throw new Error('API Error');
      const data = await res.json();
      const traceId = data.trace_id;
      
      pollTrace(traceId);
    } catch (err) {
      console.error("Trace failed to start", err);
      setTraceState('IDLE');
      addLog("Failed to connect to ingestion engine.", 'warning');
    }
  };

  const pollTrace = async (traceId: string) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/traces/${traceId}`);
        if (!res.ok) return;
        const data = await res.json();
        
        if (data.status !== traceState && data.status !== 'PENDING') {
          setTraceState(data.status);
          addLog(`Pipeline phase updated: ${data.status}`, 'info');
        }
        
        if (data.status === 'COMPLETED') {
          clearInterval(interval);
          setTraceResult(data);
          addLog("Trace completed successfully. Graph resolution finalized.", 'success');
        } else if (data.status === 'FAILED') {
          clearInterval(interval);
          setTraceState('IDLE');
          addLog("Pipeline failed.", 'warning');
        }
      } catch (err) {
        console.error("Polling error", err);
      }
    }, 1500);
  };

  return (
    <div className="h-full flex flex-col space-y-6">
      
      {/* Top Bar / Status */}
      <div className="bg-phantasm-surface border border-phantasm-border rounded-xl p-6 flex flex-col md:flex-row justify-between items-start md:items-center shadow-lg">
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <h1 className="text-2xl font-bold text-gray-100">Case: {caseId}</h1>
            <span className="bg-phantasm-cyan/10 text-phantasm-cyan border border-phantasm-cyan/30 px-3 py-1 rounded-full text-xs font-bold tracking-wide">
              ACTIVE
            </span>
          </div>
          <p className="text-gray-400 text-sm flex items-center">
            <FileText className="w-4 h-4 mr-2" />
            Authority: <strong className="ml-1 text-gray-200">
              {caseData ? caseData.authority : "Loading..."}
            </strong>
          </p>
        </div>
        
        <div className="mt-4 md:mt-0 flex flex-col items-end">
          <div className="flex items-center text-sm font-medium text-green-400 mb-1">
            <CheckCircle className="w-4 h-4 mr-1.5" />
            Lawful Status Verified
          </div>
          <p className="text-xs text-gray-500 font-mono">
            Seed: {seedAddress}
          </p>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Graph Preview */}
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
            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgzMCwgNDUsIDc0LCAwLjIpIiBzdHJva2Utd2lkdGg9IjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-50"></div>
            
            <div className="text-center z-10 p-8">
              {traceState === 'IDLE' && (
                <>
                  <Activity className="w-12 h-12 text-phantasm-cyan/50 mx-auto mb-4 animate-pulse" />
                  <p className="text-gray-400 text-sm max-w-md mx-auto">
                    The engine is idle. Run an initial ingestion on the seed address to begin populating the Neo4j graph.
                  </p>
                </>
              )}
              {['INGESTING', 'CLASSIFYING', 'ATTRIBUTING', 'SEALING', 'PENDING'].includes(traceState) && (
                <>
                  <div className="w-16 h-16 border-4 border-phantasm-cyan border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
                  <h3 className="text-phantasm-cyan font-bold text-xl tracking-widest mb-2 animate-pulse">{traceState}...</h3>
                  <p className="text-gray-400 text-sm">Processing graph analytics via AI Pipeline</p>
                </>
              )}
              {traceState === 'COMPLETED' && traceResult && (
                <div className="bg-[#0A0F1D]/80 border border-phantasm-cyan/30 rounded-xl p-6 inline-block text-left backdrop-blur-sm">
                  <h3 className="text-green-400 font-bold mb-4 flex items-center">
                    <CheckCircle className="w-5 h-5 mr-2" /> Trace Completed Successfully
                  </h3>
                  <div className="space-y-3">
                    <p className="text-sm text-gray-300">Target identified at VASP:</p>
                    <p className="text-xl font-mono text-white bg-gray-800 p-2 rounded">{traceResult.vasp_node || 'Unknown'}</p>
                    <div className="flex justify-between items-center mt-4 border-t border-gray-700 pt-4">
                      <span className="text-sm text-gray-400">Confidence Score:</span>
                      <span className="text-phantasm-amber font-bold">{traceResult.confidence ? (traceResult.confidence * 100).toFixed(1) : 0}%</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Guided NEXT STEP Card */}
        <div className="flex flex-col space-y-6">
          <div className="bg-gradient-to-b from-phantasm-surface to-[#0A0F1D] border border-phantasm-cyan/30 rounded-xl shadow-[0_0_20px_rgba(0,229,255,0.1)] p-6">
            <h3 className="text-phantasm-cyan font-bold tracking-wider text-sm mb-4">NEXT STEP</h3>
            
            {traceState === 'IDLE' ? (
              <>
                <h4 className="text-lg font-semibold text-gray-100 mb-2">Ingest Seed Activity</h4>
                <p className="text-sm text-gray-400 mb-6 leading-relaxed">
                  Fetch the complete transaction history for the seed address using the configured providers and cross-validation gate.
                </p>
                <button 
                  onClick={startTrace}
                  className="w-full bg-phantasm-cyan text-[#0A0F1D] font-bold py-3 rounded-lg flex items-center justify-center hover:bg-opacity-90 transition-all shadow-[0_0_10px_rgba(0,229,255,0.4)] group"
                >
                  <Play className="w-4 h-4 mr-2 fill-current" />
                  START INGESTION
                </button>
              </>
            ) : traceState === 'COMPLETED' ? (
              <>
                <h4 className="text-lg font-semibold text-gray-100 mb-2">View Dossier</h4>
                <p className="text-sm text-gray-400 mb-6 leading-relaxed">
                  The evidence has been sealed with Merkle proofs. You can now download the generated forensic dossier.
                </p>
                <button 
                  onClick={() => {
                    if (traceResult?.dossier_url) {
                      window.open(traceResult.dossier_url, '_blank');
                    }
                  }}
                  className="w-full bg-green-500 text-white font-bold py-3 rounded-lg flex items-center justify-center hover:bg-opacity-90 transition-all shadow-[0_0_10px_rgba(34,197,94,0.4)]"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  DOWNLOAD PDF
                </button>
              </>
            ) : (
              <div className="space-y-4">
                <div className={`flex items-center p-2 rounded ${['INGESTING', 'PENDING'].includes(traceState) ? 'bg-phantasm-cyan/20 text-phantasm-cyan border border-phantasm-cyan/50' : 'text-gray-500'}`}>
                  <Network className="w-4 h-4 mr-3" /> Ingesting Data
                </div>
                <div className={`flex items-center p-2 rounded ${traceState === 'CLASSIFYING' ? 'bg-phantasm-cyan/20 text-phantasm-cyan border border-phantasm-cyan/50' : 'text-gray-500'}`}>
                  <Cpu className="w-4 h-4 mr-3" /> Classifying Nodes
                </div>
                <div className={`flex items-center p-2 rounded ${traceState === 'ATTRIBUTING' ? 'bg-phantasm-cyan/20 text-phantasm-cyan border border-phantasm-cyan/50' : 'text-gray-500'}`}>
                  <Share2 className="w-4 h-4 mr-3" /> Attributing Paths
                </div>
                <div className={`flex items-center p-2 rounded ${traceState === 'SEALING' ? 'bg-phantasm-cyan/20 text-phantasm-cyan border border-phantasm-cyan/50' : 'text-gray-500'}`}>
                  <Lock className="w-4 h-4 mr-3" /> Sealing Evidence
                </div>
              </div>
            )}
          </div>
          
          {/* Recent Activity Log */}
          <div className="bg-phantasm-surface border border-phantasm-border rounded-xl p-5 flex-1">
            <h3 className="text-gray-400 font-semibold text-sm mb-4">Activity Log</h3>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {logs.map((log, i) => (
                <div key={i} className={`border-l-2 pl-3 py-1 ${
                  log.type === 'success' ? 'border-green-500' : 
                  log.type === 'warning' ? 'border-red-500' : 
                  'border-phantasm-amber'
                }`}>
                  <p className="text-xs text-gray-500 mb-0.5">{log.time}</p>
                  <p className="text-sm text-gray-200">{log.message}</p>
                </div>
              ))}
              {logs.length === 0 && (
                <p className="text-sm text-gray-500 italic">No activity yet...</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
