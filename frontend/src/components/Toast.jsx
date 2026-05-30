import React, { useEffect } from 'react';
import { X, CheckCircle, AlertTriangle, Info } from 'lucide-react';

export default function Toast({ message, type = 'success', onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose();
    }, 5000); // Auto close in 5 seconds
    
    return () => clearTimeout(timer);
  }, [onClose]);

  const styles = {
    success: {
      bg: 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300',
      icon: <CheckCircle className="h-5 w-5 text-emerald-400" />
    },
    error: {
      bg: 'bg-rose-950/80 border-rose-500/40 text-rose-300',
      icon: <AlertTriangle className="h-5 w-5 text-rose-400" />
    },
    info: {
      bg: 'bg-cyan-950/80 border-cyan-500/40 text-cyan-300',
      icon: <Info className="h-5 w-5 text-cyan-400" />
    }
  };

  const activeStyle = styles[type] || styles.info;

  return (
    <div className={`fixed bottom-5 right-5 flex items-center p-4 rounded-xl border backdrop-blur-md shadow-2xl transition-all duration-300 transform translate-y-0 z-50 max-w-sm ${activeStyle.bg}`}>
      <div className="mr-3 shrink-0">
        {activeStyle.icon}
      </div>
      <div className="text-sm font-medium pr-6 leading-tight">
        {message}
      </div>
      <button 
        onClick={onClose}
        className="absolute top-2.5 right-2.5 text-slate-400 hover:text-white transition-colors duration-150"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
}
