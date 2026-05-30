import React from 'react';
import { Cpu, Zap, Activity } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo Brand */}
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-tr from-cyan-500 to-purple-600 rounded-xl shadow-glow">
              <Zap className="h-6 w-6 text-white animate-pulse" />
            </div>
            <div>
              <span className="font-extrabold text-xl bg-gradient-to-r from-white via-slate-100 to-cyan-300 bg-clip-text text-transparent tracking-tight">
                LeadEnrich <span className="text-cyan-400 font-medium text-sm px-1.5 py-0.5 rounded-md bg-cyan-950/40 border border-cyan-800/30 ml-1">AI</span>
              </span>
              <p className="text-[10px] text-slate-400 font-mono tracking-widest uppercase">Prospect Intelligence</p>
            </div>
          </div>
          
          {/* System status pill */}
          <div className="flex items-center space-x-2 bg-slate-900/90 border border-slate-800 px-3.5 py-1.5 rounded-full text-xs font-medium text-slate-300">
            <Activity className="h-3.5 w-3.5 text-cyan-400 animate-pulse" />
            <span className="font-mono text-slate-400">Groq LLAMA-3.3</span>
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-ping"></span>
          </div>
        </div>
      </div>
    </nav>
  );
}
