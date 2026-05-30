import React, { useState, useEffect } from 'react';
import { Search, Loader2, Sparkles, AlertCircle } from 'lucide-react';

export default function EnrichForm({ onEnrich, isLoading }) {
  const [url, setUrl] = useState('');
  const [websiteName, setWebsiteName] = useState('');
  const [error, setError] = useState('');
  const [loadingTextIndex, setLoadingTextIndex] = useState(0);

  const loadingMessages = [
    "Enriching company profile...",
    "Scanning domain and checking sitemap.xml...",
    "Crawling pages and extracting links...",
    "Filtering with RapidFuzz semantic matcher...",
    "Extracting contact phone and email patterns...",
    "Stripping boilerplate HTML & layout tags...",
    "Running LLAMA-3.3 Groq inference (temperature 0.1)...",
    "Generating custom target customer profile...",
    "Synthesizing probable pain points...",
    "Polishing outreach opener..."
  ];

  // Rotate loading texts for feedback
  useEffect(() => {
    if (!isLoading) {
      setLoadingTextIndex(0);
      return;
    }
    const interval = setInterval(() => {
      setLoadingTextIndex((prev) => (prev + 1) % loadingMessages.length);
    }, 4000);
    return () => clearInterval(interval);
  }, [isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    const trimmedUrl = url.strip ? url.strip() : url.trim();
    if (!trimmedUrl) {
      setError('Company URL is required');
      return;
    }

    // Basic URL validation
    if (!trimmedUrl.includes('.') || trimmedUrl.length < 4) {
      setError('Please enter a valid website URL (e.g. company.com)');
      return;
    }

    onEnrich(trimmedUrl, websiteName.strip ? websiteName.strip() : websiteName.trim());
  };

  return (
    <div className="w-full bg-glass rounded-2xl p-6 border border-slate-800/80 shadow-glowPurple relative overflow-hidden">
      {/* Decorative Glow back-panel */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-purple-600/5 rounded-full blur-3xl pointer-events-none"></div>
      
      <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2 mb-4">
        <Sparkles className="h-5 w-5 text-cyan-400" />
        Analyze & Profiling Engine
      </h2>
      <p className="text-sm text-slate-400 mb-6">
        Enter a company website URL. The engine will scrape its contents and generate key B2B profile insights instantly.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Website Name (Optional) */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Website / Company Name <span className="text-slate-500">(Optional)</span>
            </label>
            <input
              type="text"
              placeholder="e.g. Relu Consultancy"
              value={websiteName}
              onChange={(e) => setWebsiteName(e.target.value)}
              disabled={isLoading}
              className="w-full bg-slate-950/70 border border-slate-800 focus:border-purple-500 focus:ring-1 focus:ring-purple-500 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-600 outline-none transition duration-200"
            />
          </div>

          {/* Company URL (Required) */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Company URL <span className="text-rose-500/70">*</span>
            </label>
            <input
              type="text"
              placeholder="e.g. reluconsultancy.in"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={isLoading}
              className="w-full bg-slate-950/70 border border-slate-800 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-600 outline-none transition duration-200"
            />
          </div>
        </div>

        {error && (
          <div className="flex items-center space-x-2 text-rose-400 bg-rose-950/30 border border-rose-900/40 rounded-xl px-4 py-3 text-xs">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-cyan-500 via-blue-600 to-purple-600 hover:from-cyan-400 hover:via-blue-500 hover:to-purple-500 text-white font-semibold py-3 px-4 rounded-xl shadow-glow transition duration-200 flex items-center justify-center space-x-2 disabled:opacity-60 disabled:cursor-not-allowed group"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <span className="text-sm font-mono tracking-wide text-cyan-200 animate-pulse">
                {loadingMessages[loadingTextIndex]}
              </span>
            </>
          ) : (
            <>
              <Search className="h-5 w-5 group-hover:scale-110 transition duration-150" />
              <span>Enrich Website</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
