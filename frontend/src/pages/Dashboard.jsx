import React, { useState, useEffect, useRef } from 'react';
import Navbar from '../components/Navbar';
import EnrichForm from '../components/EnrichForm';
import ResultCard from '../components/ResultCard';
import ResultsTable from '../components/ResultsTable';
import SkeletonLoader from '../components/SkeletonLoader';
import Toast from '../components/Toast';
import { enrichCompany, getResults } from '../services/api';
import { RefreshCw, LayoutDashboard, Compass } from 'lucide-react';

export default function Dashboard() {
  const [results, setResults] = useState([]);
  const [selectedResult, setSelectedResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const resultCardRef = useRef(null);

  // Fetch results on initial load
  useEffect(() => {
    fetchDirectory();
  }, []);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  const fetchDirectory = async () => {
    try {
      const data = await getResults();
      setResults(data);
    } catch (err) {
      console.error(err);
      showToast('Failed to load database. Check if backend server is running.', 'error');
    }
  };

  const handleEnrich = async (url, websiteName) => {
    setIsLoading(true);
    setSelectedResult(null); // Clear previous selection during load
    showToast('Starting Smart Crawl & B2B Enrichment...', 'info');

    try {
      const data = await enrichCompany(url, websiteName);
      setSelectedResult(data);
      
      // Update local storage representation
      setResults((prev) => {
        // Filter out existing duplicates
        const filtered = prev.filter(
          (c) => c.website_name.toLowerCase() !== data.website_name.toLowerCase() && 
                 c.website_url?.toLowerCase() !== data.website_url?.toLowerCase()
        );
        return [data, ...filtered];
      });

      showToast(`Successfully enriched profile for ${data.website_name}!`, 'success');
      
      // Smooth scroll to the result card
      setTimeout(() => {
        resultCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 300);

    } catch (err) {
      console.error(err);
      showToast(err.message || 'Scraping timed out or URL was blocked. Returning scraped items.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const selectCompanyFromTable = (company) => {
    setSelectedResult(company);
    setTimeout(() => {
      resultCardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
  };

  return (
    <div className="min-h-screen bg-[#020205] bg-grid-pattern pb-20 relative overflow-hidden">
      {/* Background Neon Glowing Spotlights */}
      <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-purple-900/10 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>
      <div className="absolute top-[20%] right-[-10%] w-[45vw] h-[45vw] bg-cyan-900/10 rounded-full blur-[120px] pointer-events-none animate-pulse-slow"></div>
      <div className="absolute bottom-[10%] left-[20%] w-[40vw] h-[40vw] bg-blue-900/5 rounded-full blur-[120px] pointer-events-none"></div>

      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 sm:mt-16 space-y-12 relative z-10">
        {/* Hero Banner Section */}
        <section className="text-center max-w-3xl mx-auto space-y-5">
          <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-500/10 via-cyan-500/10 to-blue-500/10 border border-slate-800/80 px-4 py-2 rounded-full text-xs font-semibold text-slate-300 shadow-glow">
            <span className="flex h-2 w-2 rounded-full bg-cyan-400 animate-pulse"></span>
            <span className="font-mono text-cyan-400 tracking-wide uppercase text-[10px]">Developer Hiring Hackathon Deployed Sandbox</span>
          </div>
          
          <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight leading-[1.05] font-sans">
            Turn Any Website into <br className="hidden sm:inline" />
            <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent">
              Actionable B2B Insights
            </span>
          </h1>
          
          <p className="text-sm sm:text-base text-slate-400 leading-relaxed font-sans max-w-2xl mx-auto">
            A high-performance AI crawler and corporate profiler. Extract verified emails, phone numbers, and addresses. Map target customers and pain points using Groq AI instantly.
          </p>
        </section>

        {/* Action Panel Grid: Form on Left, Output Card on Right */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Form container */}
          <div className="lg:col-span-5">
            <EnrichForm onEnrich={handleEnrich} isLoading={isLoading} />
          </div>

          {/* Result Card preview container */}
          <div className="lg:col-span-7 w-full" ref={resultCardRef}>
            {isLoading && <SkeletonLoader />}
            
            {!isLoading && selectedResult && (
              <ResultCard result={selectedResult} />
            )}
            
            {!isLoading && !selectedResult && (
              <div className="h-72 border border-dashed border-slate-800/80 rounded-2xl flex flex-col items-center justify-center text-slate-500 bg-glass">
                <LayoutDashboard className="h-10 w-10 text-slate-700 mb-3" />
                <p className="text-sm font-medium">Result Board Ready</p>
                <p className="text-xs text-slate-650 max-w-xs text-center mt-1">
                  Once enriched, the company profile card with emails, pain points, and sales hooks will render here.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Database Directory Section */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-extrabold text-white tracking-tight">Database & History Logs</h2>
              <p className="text-xs text-slate-500">Query history and enriched datasets loaded in system memory.</p>
            </div>
            
            <button
              onClick={fetchDirectory}
              className="flex items-center space-x-2 bg-slate-900 border border-slate-800 hover:border-cyan-500/40 text-slate-300 hover:text-white px-4 py-2 text-xs font-semibold rounded-xl transition duration-150"
            >
              <RefreshCw className="h-3.5 w-3.5 text-slate-400" />
              <span>Show All Results</span>
            </button>
          </div>

          <ResultsTable results={results} onSelectCompany={selectCompanyFromTable} />
        </section>
      </main>

      {/* Toast Alert Notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}
