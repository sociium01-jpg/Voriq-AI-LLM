'use client';

import React, { useState } from 'react';
import {
  Shield, Database, Cpu, Layers, Activity, AlertTriangle, CheckCircle, Play, RotateCcw, BarChart3, Users, Lock
} from 'lucide-react';

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState<'overview' | 'datasets' | 'training' | 'registry' | 'gpus'>('overview');
  const [canaryTraffic, setCanaryTraffic] = useState(10.0);
  const [isRolledBack, setIsRolledBack] = useState(false);

  return (
    <div className="min-h-screen w-screen bg-background text-primaryText font-sans flex flex-col">
      {/* Header */}
      <header className="h-16 border-b border-surfaceBorder glass-card px-8 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-accent flex items-center justify-center font-bold text-white shadow-lg shadow-accent/20">
            V
          </div>
          <div>
            <h1 className="font-bold text-lg text-white">Voriq AI Admin Engine</h1>
            <p className="text-xs text-secondaryText">Phase 2 Proprietary Model Control Panel</p>
          </div>
        </div>

        <div className="flex items-center gap-4 text-xs">
          <span className="flex items-center gap-1.5 bg-green-500/15 text-green-400 border border-green-500/30 px-3 py-1.5 rounded-full">
            <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
            Model Gateway: Healthy
          </span>
          <div className="text-secondaryText">Role: <strong className="text-white">AI Administrator</strong></div>
        </div>
      </header>

      {/* Main Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Sidebar */}
        <aside className="w-64 glass-card border-r border-surfaceBorder p-4 space-y-2">
          <button
            onClick={() => setActiveTab('overview')}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeTab === 'overview' ? 'bg-accent/20 text-accent border border-accent/30' : 'text-secondaryText hover:text-white hover:bg-surface'
            }`}
          >
            <BarChart3 className="w-4 h-4" /> System Overview
          </button>

          <button
            onClick={() => setActiveTab('datasets')}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeTab === 'datasets' ? 'bg-accent/20 text-accent border border-accent/30' : 'text-secondaryText hover:text-white hover:bg-surface'
            }`}
          >
            <Database className="w-4 h-4" /> Datasets & Governance
          </button>

          <button
            onClick={() => setActiveTab('training')}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeTab === 'training' ? 'bg-accent/20 text-accent border border-accent/30' : 'text-secondaryText hover:text-white hover:bg-surface'
            }`}
          >
            <Cpu className="w-4 h-4" /> LoRA Fine-Tuning Service
          </button>

          <button
            onClick={() => setActiveTab('registry')}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeTab === 'registry' ? 'bg-accent/20 text-accent border border-accent/30' : 'text-secondaryText hover:text-white hover:bg-surface'
            }`}
          >
            <Layers className="w-4 h-4" /> Model Registry & Canary
          </button>

          <button
            onClick={() => setActiveTab('gpus')}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-colors ${
              activeTab === 'gpus' ? 'bg-accent/20 text-accent border border-accent/30' : 'text-secondaryText hover:text-white hover:bg-surface'
            }`}
          >
            <Activity className="w-4 h-4" /> GPU Worker Cluster
          </button>
        </aside>

        {/* Workspace Content View */}
        <main className="flex-1 overflow-y-auto p-8 space-y-8">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white">System Status & Overview</h2>
              <div className="grid grid-cols-4 gap-4">
                <div className="glass-card p-5 rounded-2xl">
                  <div className="text-xs text-secondaryText mb-1">Active Fine-Tuning Jobs</div>
                  <div className="text-2xl font-bold text-accent">2 Jobs</div>
                  <div className="text-[11px] text-green-400 mt-2">Hinglish-LoRA & Manglish-LoRA</div>
                </div>
                <div className="glass-card p-5 rounded-2xl">
                  <div className="text-xs text-secondaryText mb-1">GPU Memory Utilization</div>
                  <div className="text-2xl font-bold text-white">64% Avg</div>
                  <div className="text-[11px] text-secondaryText mt-2">NVIDIA H100 x 4 Cluster</div>
                </div>
                <div className="glass-card p-5 rounded-2xl">
                  <div className="text-xs text-secondaryText mb-1">Dataset Governance</div>
                  <div className="text-2xl font-bold text-green-400">Passed</div>
                  <div className="text-[11px] text-secondaryText mt-2">PII Scan & License Checked</div>
                </div>
                <div className="glass-card p-5 rounded-2xl">
                  <div className="text-xs text-secondaryText mb-1">Canary Release Stage</div>
                  <div className="text-2xl font-bold text-white">{isRolledBack ? 'Rolled Back' : '10.0% Traffic'}</div>
                  <div className="text-[11px] text-secondaryText mt-2">Voriq Indic Foundation V1</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'datasets' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white">Dataset Governance & Management</h2>
              <div className="glass-card p-6 rounded-2xl space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-white text-sm">hinglish-customer-support-v1</h3>
                  <span className="text-xs bg-green-500/20 text-green-400 px-3 py-1 rounded-full border border-green-500/30">Approved for Training</span>
                </div>
                <div className="grid grid-cols-4 gap-4 text-xs">
                  <div><strong>Rows:</strong> 15,000 Verified</div>
                  <div><strong>Language:</strong> Hindi / English</div>
                  <div><strong>PII Scan:</strong> Passed Zero Leakage</div>
                  <div><strong>License:</strong> Apache-2.0 Commercial</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'registry' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white">Model Registry & Canary Deployment Controls</h2>
              <div className="glass-card p-6 rounded-2xl space-y-6">
                <div className="flex items-center justify-between border-b border-surfaceBorder pb-4">
                  <div>
                    <h3 className="font-bold text-white text-base">vorik-indic-foundation-v1</h3>
                    <p className="text-xs text-secondaryText">Base: Meta Llama 3.3 70B | Adapter: vorik-hinglish-v1</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => setIsRolledBack(true)}
                      className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/30 rounded-xl text-xs font-semibold flex items-center gap-2"
                    >
                      <RotateCcw className="w-4 h-4" /> Trigger Immediate Rollback
                    </button>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex justify-between text-xs text-secondaryText">
                    <span>Canary Traffic Allocation</span>
                    <span className="font-semibold text-white">{isRolledBack ? '0.0%' : `${canaryTraffic}%`}</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={isRolledBack ? 0 : canaryTraffic}
                    onChange={(e) => {
                      setIsRolledBack(false);
                      setCanaryTraffic(parseFloat(e.target.value));
                    }}
                    className="w-full h-2 bg-surface rounded-lg appearance-none cursor-pointer accent-accent"
                  />
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
