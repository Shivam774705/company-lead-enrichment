import React, { useState } from 'react';
import { Eye, ChevronDown, ChevronUp, Search, Database, Globe } from 'lucide-react';

export default function ResultsTable({ results, onSelectCompany }) {
  const [filterText, setFilterText] = useState('');
  const [expandedRow, setExpandedRow] = useState(null);

  const toggleRow = (idx) => {
    setExpandedRow(expandedRow === idx ? null : idx);
  };

  const filteredResults = results.filter((company) => {
    const text = (
      (company.website_name || '') + 
      (company.company_name || '') + 
      (company.core_service || '') +
      (company.website_url || '')
    ).toLowerCase();
    return text.includes(filterText.toLowerCase());
  });

  return (
    <div className="w-full bg-glass rounded-2xl border border-slate-800/80 shadow-2xl overflow-hidden">
      {/* Table header controls */}
      <div className="p-6 border-b border-slate-800/85 flex flex-col sm:flex-row items-center justify-between gap-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Database className="h-5 w-5 text-cyan-400" />
          Enriched Company Directory
          <span className="text-xs text-slate-500 font-mono">({filteredResults.length} records)</span>
        </h3>
        
        {/* Search Input */}
        <div className="relative w-full sm:w-72">
          <Search className="absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search database..."
            value={filterText}
            onChange={(e) => setFilterText(e.target.value)}
            className="w-full bg-slate-950/70 border border-slate-800 focus:border-cyan-500 rounded-xl pl-10 pr-4 py-2 text-xs text-slate-200 outline-none placeholder-slate-600 transition"
          />
        </div>
      </div>

      {/* Main Container */}
      {filteredResults.length === 0 ? (
        <div className="p-12 text-center text-slate-500">
          <Globe className="h-12 w-12 mx-auto text-slate-700 mb-3 animate-pulse" />
          <p className="text-sm">No companies enriched yet or match search criteria.</p>
          <p className="text-xs text-slate-600 mt-1">Run an enrichment query above to populate the directory.</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          {/* Desktop Table View */}
          <table className="w-full border-collapse text-left text-sm text-slate-300">
            <thead className="bg-slate-950/60 border-b border-slate-800/85 text-xs text-slate-400 font-bold uppercase tracking-wider">
              <tr>
                <th className="px-6 py-4">Company / Website</th>
                <th className="px-6 py-4 hidden md:table-cell">Core Services</th>
                <th className="px-6 py-4 hidden lg:table-cell">Target Customer</th>
                <th className="px-6 py-4">Emails</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {filteredResults.map((company, idx) => {
                const isExpanded = expandedRow === idx;
                const emailStr = company.mail && company.mail.length > 0 
                  ? company.mail.join(', ') 
                  : 'N/A';
                  
                return (
                  <React.Fragment key={idx}>
                    {/* Primary Row */}
                    <tr className="hover:bg-slate-900/30 transition-colors duration-150">
                      <td className="px-6 py-4">
                        <div className="font-semibold text-white">{company.website_name || 'N/A'}</div>
                        {company.website_url && (
                          <div className="text-[10px] text-slate-500 font-mono truncate max-w-xs">{company.website_url}</div>
                        )}
                      </td>
                      <td className="px-6 py-4 hidden md:table-cell max-w-xs truncate">
                        {company.core_service || <span className="text-slate-600 italic">N/A</span>}
                      </td>
                      <td className="px-6 py-4 hidden lg:table-cell max-w-xs truncate">
                        {company.target_customer || <span className="text-slate-600 italic">N/A</span>}
                      </td>
                      <td className="px-6 py-4">
                        {company.mail && company.mail.length > 0 ? (
                          <span className="text-xs font-mono bg-cyan-950/20 text-cyan-400 py-1 px-2.5 rounded-md border border-cyan-850/30">
                            {company.mail[0]}
                            {company.mail.length > 1 && ` (+${company.mail.length - 1})`}
                          </span>
                        ) : (
                          <span className="text-slate-600 italic text-xs">N/A</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-right space-x-2">
                        <button
                          onClick={() => onSelectCompany(company)}
                          title="View Details Card"
                          className="inline-flex items-center p-1.5 bg-slate-900 border border-slate-800 hover:border-cyan-500/40 text-slate-400 hover:text-white rounded-lg transition"
                        >
                          <Eye className="h-4 w-4" />
                        </button>
                        <button
                          onClick={() => toggleRow(idx)}
                          className="inline-flex items-center p-1.5 bg-slate-900 border border-slate-800 hover:border-purple-500/40 text-slate-400 hover:text-white rounded-lg transition"
                        >
                          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                        </button>
                      </td>
                    </tr>

                    {/* Expandable Details Row */}
                    {isExpanded && (
                      <tr className="bg-slate-950/40">
                        <td colSpan="5" className="px-8 py-5 text-xs border-t border-b border-slate-850/50">
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {/* Panel 1: Contacts */}
                            <div className="space-y-2">
                              <h5 className="font-bold text-purple-400 uppercase tracking-widest text-[10px]">Contact Info</h5>
                              <div className="space-y-1 text-slate-300">
                                <div><span className="text-slate-500 font-medium">Full Name:</span> {company.company_name || 'N/A'}</div>
                                <div><span className="text-slate-500 font-medium">Address:</span> {company.address || 'N/A'}</div>
                                <div><span className="text-slate-500 font-medium">Phone:</span> {company.mobile_number || 'N/A'}</div>
                                <div><span className="text-slate-500 font-medium">Emails:</span> {emailStr}</div>
                              </div>
                            </div>
                            
                            {/* Panel 2: Insights */}
                            <div className="space-y-2 md:col-span-2">
                              <h5 className="font-bold text-cyan-400 uppercase tracking-widest text-[10px]">Strategic Summary</h5>
                              <div className="space-y-2.5">
                                <div>
                                  <span className="text-slate-500 font-medium block">Core Services & Expertise</span>
                                  <p className="text-slate-300 leading-relaxed">{company.core_service || 'N/A'}</p>
                                </div>
                                <div>
                                  <span className="text-slate-500 font-medium block">Key Pain Points Addressed</span>
                                  <p className="text-slate-300 leading-relaxed">{company.probable_pain_point || 'N/A'}</p>
                                </div>
                                <div>
                                  <span className="text-slate-500 font-medium block">Cold Outreach Hook</span>
                                  <p className="text-slate-300 italic leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-slate-850/50">
                                    "{company.outreach_opener || 'N/A'}"
                                  </p>
                                </div>
                              </div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
