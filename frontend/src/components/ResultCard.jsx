import React, { useState } from 'react';
import { Globe, MapPin, Phone, Mail, Award, Target, HelpCircle, MessageSquare, Copy, Check } from 'lucide-react';

export default function ResultCard({ result }) {
  const [copied, setCopied] = useState(false);

  if (!result) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(result.outreach_opener || '');
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getCleanLabel = (val) => val || 'N/A';

  return (
    <div className="w-full bg-glass rounded-2xl border border-slate-800/80 shadow-glow relative overflow-hidden transition-all duration-300 hover:border-cyan-500/30">
      {/* Glow highlight */}
      <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-600"></div>

      {/* Header Info */}
      <div className="p-6 border-b border-slate-800/85 flex flex-col sm:flex-row justify-between items-start gap-4">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <Globe className="h-4 w-4 text-cyan-400" />
            <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">Latest Enrichment</span>
          </div>
          <h3 className="text-2xl font-extrabold text-white tracking-tight">
            {getCleanLabel(result.website_name)}
          </h3>
          {result.company_name && (
            <p className="text-sm text-slate-400 font-medium">Registered as: {result.company_name}</p>
          )}
        </div>
        
        {/* URL link badge */}
        {result.website_url && (
          <a
            href={result.website_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs bg-slate-900 border border-slate-800 hover:border-cyan-500/40 text-slate-300 font-mono py-1.5 px-3 rounded-lg transition duration-150 shrink-0"
          >
            {result.website_url.replace(/^https?:\/\//, '')}
          </a>
        )}
      </div>

      {/* Content Grid */}
      <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Contact info column */}
        <div className="space-y-4">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-800/40 pb-2">
            Contact Information
          </h4>
          
          <div className="space-y-3">
            {/* Address */}
            <div className="flex items-start space-x-3">
              <MapPin className="h-4 w-4 text-slate-400 mt-1 shrink-0" />
              <div>
                <span className="text-xs text-slate-500 block">Address</span>
                <span className="text-sm text-slate-200">{getCleanLabel(result.address)}</span>
              </div>
            </div>
            
            {/* Mobile */}
            <div className="flex items-start space-x-3">
              <Phone className="h-4 w-4 text-slate-400 mt-1 shrink-0" />
              <div>
                <span className="text-xs text-slate-500 block">Mobile Number</span>
                <span className="text-sm text-slate-200 font-mono">{getCleanLabel(result.mobile_number)}</span>
              </div>
            </div>

            {/* Email list */}
            <div className="flex items-start space-x-3">
              <Mail className="h-4 w-4 text-slate-400 mt-1 shrink-0" />
              <div className="w-full">
                <span className="text-xs text-slate-500 block mb-1">Emails</span>
                {result.mail && result.mail.length > 0 ? (
                  <div className="flex flex-wrap gap-1.5 mt-0.5">
                    {result.mail.map((email, idx) => (
                      <span 
                        key={idx} 
                        className="text-xs font-mono bg-cyan-950/40 border border-cyan-800/30 text-cyan-300 py-1 px-2.5 rounded-lg"
                      >
                        {email}
                      </span>
                    ))}
                  </div>
                ) : (
                  <span className="text-sm text-slate-400 italic">No emails found</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Business Insights column */}
        <div className="space-y-4">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-slate-800/40 pb-2">
            Business Insights
          </h4>

          <div className="space-y-4">
            {/* Core Service */}
            <div className="flex items-start space-x-3">
              <Award className="h-4 w-4 text-purple-400 mt-1 shrink-0" />
              <div>
                <span className="text-xs text-slate-500 block">Core Service</span>
                <p className="text-sm text-slate-200 leading-relaxed">{getCleanLabel(result.core_service)}</p>
              </div>
            </div>

            {/* Target Customer */}
            <div className="flex items-start space-x-3">
              <Target className="h-4 w-4 text-emerald-400 mt-1 shrink-0" />
              <div>
                <span className="text-xs text-slate-500 block">Target Customer</span>
                <p className="text-sm text-slate-200 leading-relaxed">{getCleanLabel(result.target_customer)}</p>
              </div>
            </div>

            {/* Pain Point */}
            <div className="flex items-start space-x-3">
              <HelpCircle className="h-4 w-4 text-yellow-400 mt-1 shrink-0" />
              <div>
                <span className="text-xs text-slate-500 block">Probable Pain Point</span>
                <p className="text-sm text-slate-200 leading-relaxed">{getCleanLabel(result.probable_pain_point)}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Opener footer block */}
      <div className="bg-slate-950/80 border-t border-slate-800/85 p-6 relative">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <MessageSquare className="h-4 w-4 text-purple-400" />
            <span className="text-xs font-bold text-purple-400 uppercase tracking-widest">Outreach Opener Hook</span>
          </div>
          <button
            onClick={handleCopy}
            disabled={!result.outreach_opener}
            className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg transition duration-150 disabled:opacity-50"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-emerald-400 font-medium">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5" />
                <span>Copy Opener</span>
              </>
            )}
          </button>
        </div>
        <p className="text-slate-300 text-sm italic font-medium leading-relaxed bg-slate-900/40 p-4 rounded-xl border border-slate-800/40 select-all">
          "{getCleanLabel(result.outreach_opener)}"
        </p>
      </div>
    </div>
  );
}
