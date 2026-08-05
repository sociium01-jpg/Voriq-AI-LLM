'use client';

import React, { useState } from 'react';
import { Bot, Shield, Cpu, Activity, Play, Plus, RefreshCw, CheckCircle2, Sliders } from 'lucide-react';

export default function AgentRegistryAdmin() {
  const [agents, setAgents] = useState([
    { id: 'supervisor', name: 'Supervisor Router Agent', type: 'supervisor', baseModel: 'meta-llama-3.3-70b', status: 'production', maxSteps: 25, budget: '$2.00', toolsCount: 8 },
    { id: 'planner', name: 'Multi-Step Planner Agent', type: 'planner', baseModel: 'meta-llama-3.3-70b', status: 'production', maxSteps: 30, budget: '$3.00', toolsCount: 5 },
    { id: 'research', name: 'Multi-Source Research Agent', type: 'research', baseModel: 'meta-llama-3.3-70b', status: 'production', maxSteps: 20, budget: '$1.50', toolsCount: 4 },
    { id: 'coding', name: 'Polyglot Coding Agent', type: 'coding', baseModel: 'meta-llama-3.3-70b', status: 'production', maxSteps: 25, budget: '$2.00', toolsCount: 6 },
    { id: 'indian_language', name: 'Indic Code-Mixed Agent', type: 'indian_language', baseModel: 'vorik-indic-v1', status: 'production', maxSteps: 15, budget: '$1.00', toolsCount: 3 },
    { id: 'verification', name: 'Evidence Verification Agent', type: 'verification', baseModel: 'vorik-indic-v1', status: 'production', maxSteps: 10, budget: '$0.50', toolsCount: 2 }
  ]);

  return (
    <div className="p-8 space-y-6 text-gray-100 min-h-screen bg-[#080A0F]">
      <div className="flex items-center justify-between border-b border-white/10 pb-5">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Bot className="w-6 h-6 text-amber-400" />
            Agent Registry & Lifecycle Governance
          </h1>
          <p className="text-xs text-gray-400 mt-1">Manage stateful agent definitions, budget caps, and deployment status.</p>
        </div>
        <button className="flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-black px-4 py-2 rounded-xl text-xs font-semibold shadow-lg shadow-amber-500/20 transition-all">
          <Plus className="w-4 h-4" />
          <span>Register New Agent</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-white/5 border border-white/10 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">18</div>
            <div className="text-xs text-gray-400">Total Core Agents</div>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white/5 border border-white/10 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">6 Active</div>
            <div className="text-xs text-gray-400">In Production Status</div>
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-white/5 border border-white/10 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-bold text-white">100% Passed</div>
            <div className="text-xs text-gray-400">Tenant Isolation Policy</div>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-white/10 overflow-hidden bg-black/40">
        <table className="w-full text-left text-xs">
          <thead className="bg-white/5 text-gray-400 border-b border-white/10">
            <tr>
              <th className="p-3.5">Agent Name & ID</th>
              <th className="p-3.5">Agent Type</th>
              <th className="p-3.5">Base Model</th>
              <th className="p-3.5">Max Steps</th>
              <th className="p-3.5">Budget Cap</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {agents.map((agent) => (
              <tr key={agent.id} className="hover:bg-white/5 transition-colors">
                <td className="p-3.5 font-medium text-white flex items-center gap-2">
                  <Bot className="w-4 h-4 text-amber-400" />
                  <div>
                    <div>{agent.name}</div>
                    <div className="text-[10px] text-gray-500 font-mono">{agent.id}</div>
                  </div>
                </td>
                <td className="p-3.5 font-mono text-amber-300">{agent.type}</td>
                <td className="p-3.5 text-gray-300">{agent.baseModel}</td>
                <td className="p-3.5 text-gray-300 font-mono">{agent.maxSteps} steps</td>
                <td className="p-3.5 text-gray-300 font-mono">{agent.budget}</td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    {agent.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
