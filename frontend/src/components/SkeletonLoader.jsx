import React from 'react';

export default function SkeletonLoader() {
  return (
    <div className="w-full bg-glass rounded-2xl p-6 border border-slate-800/80 animate-pulse space-y-6">
      {/* Title block */}
      <div className="flex justify-between items-start border-b border-slate-800/85 pb-4">
        <div className="space-y-2.5 w-1/3">
          <div className="h-4 bg-slate-800 rounded-md w-3/4"></div>
          <div className="h-6 bg-slate-700 rounded-md w-full"></div>
        </div>
        <div className="h-10 bg-slate-800 rounded-xl w-24"></div>
      </div>
      
      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="space-y-2">
            <div className="h-3 bg-slate-800 rounded w-1/4"></div>
            <div className="h-5 bg-slate-800/60 rounded w-full"></div>
          </div>
          <div className="space-y-2">
            <div className="h-3 bg-slate-800 rounded w-1/4"></div>
            <div className="h-5 bg-slate-800/60 rounded w-3/4"></div>
          </div>
          <div className="space-y-2">
            <div className="h-3 bg-slate-800 rounded w-1/4"></div>
            <div className="h-5 bg-slate-800/60 rounded w-5/6"></div>
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="space-y-2">
            <div className="h-3 bg-slate-800 rounded w-1/4"></div>
            <div className="h-16 bg-slate-800/60 rounded w-full"></div>
          </div>
          <div className="space-y-2">
            <div className="h-3 bg-slate-800 rounded w-1/4"></div>
            <div className="h-12 bg-slate-800/60 rounded w-full"></div>
          </div>
        </div>
      </div>

      {/* Opener Block */}
      <div className="border-t border-slate-800/85 pt-4 space-y-2">
        <div className="h-3 bg-slate-800 rounded w-1/6"></div>
        <div className="h-12 bg-slate-800/40 rounded w-full"></div>
      </div>
    </div>
  );
}
