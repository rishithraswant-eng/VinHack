import React from 'react';
import { Shield, LayoutDashboard, Search, FileText, Settings, LogOut, AlertTriangle } from 'lucide-react';
import Link from 'next/link';

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-phantasm-bg text-gray-100 font-sans flex overflow-hidden">
      
      {/* Sidebar */}
      <aside className="w-64 bg-phantasm-surface border-r border-phantasm-border flex flex-col z-10 shrink-0">
        <div className="h-16 flex items-center px-6 border-b border-phantasm-border">
          <Shield className="w-8 h-8 text-phantasm-cyan mr-3" />
          <span className="font-bold text-xl tracking-wider text-phantasm-cyan">PHANTASM</span>
        </div>
        
        <nav className="flex-1 py-6 px-4 space-y-2">
          <Link href="#" className="flex items-center px-4 py-3 bg-phantasm-border/50 text-phantasm-cyan rounded-lg group">
            <LayoutDashboard className="w-5 h-5 mr-3" />
            <span className="font-medium">Dashboard</span>
          </Link>
          <Link href="#" className="flex items-center px-4 py-3 text-gray-400 hover:text-gray-100 hover:bg-white/5 rounded-lg transition-colors group">
            <Search className="w-5 h-5 mr-3" />
            <span className="font-medium">Global Search</span>
          </Link>
          <Link href="#" className="flex items-center px-4 py-3 text-gray-400 hover:text-gray-100 hover:bg-white/5 rounded-lg transition-colors group">
            <FileText className="w-5 h-5 mr-3" />
            <span className="font-medium">Cases</span>
          </Link>
        </nav>
        
        <div className="p-4 border-t border-phantasm-border">
          <Link href="#" className="flex items-center px-4 py-3 text-gray-400 hover:text-gray-100 hover:bg-white/5 rounded-lg transition-colors group">
            <Settings className="w-5 h-5 mr-3" />
            <span className="font-medium">Settings</span>
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col relative overflow-hidden">
        
        {/* NON-DISMISSIBLE MOCK CHIP - Rendered unconditionally and fixed */}
        <div className="w-full bg-phantasm-amber/20 border-b border-phantasm-amber text-phantasm-amber px-4 py-2 flex items-center justify-center font-mono text-sm shadow-md z-50">
          <AlertTriangle className="w-4 h-4 mr-2 shrink-0" />
          <span className="font-bold tracking-wide">MOCK SIMULATION MODE — NOT CONNECTED TO PRODUCTION SAHYOG</span>
        </div>

        {/* Header */}
        <header className="h-16 bg-phantasm-surface/80 backdrop-blur-sm border-b border-phantasm-border flex items-center justify-end px-8 z-10">
          {/* Officer Session Indicator */}
          <div className="flex items-center space-x-4">
            <div className="flex flex-col items-end">
              <span className="text-sm font-semibold text-gray-200">Offc. A. Sharma (IO)</span>
              <span className="text-xs text-phantasm-cyan font-mono">ID: SHM-8891-ND</span>
            </div>
            <div className="w-10 h-10 rounded-full bg-phantasm-border flex items-center justify-center border border-phantasm-cyan/30 text-phantasm-cyan">
              AS
            </div>
            <button className="p-2 text-gray-400 hover:text-phantasm-amber transition-colors ml-2" title="End Session">
              <LogOut className="w-5 h-5" />
            </button>
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
