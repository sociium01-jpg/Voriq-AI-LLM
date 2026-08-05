'use client';

import React, { useState } from 'react';
import { ShieldAlert, CheckCircle2, XCircle, Clock, AlertTriangle, UserCheck } from 'lucide-react';

export default function ApprovalQueueAdmin() {
  const [tickets, setTickets] = useState([
    { ticketId: 'ticket_78a1f49b', user: 'user_fintech_lead', tenant: 'org_bharat_ai', toolName: 'send_email', riskLevel: 'high', status: 'pending', inputs: { recipient: 'client@fintech.in', subject: 'Q3 Enterprise Proposal PDF' } },
    { ticketId: 'ticket_92b4c12d', user: 'user_media_director', tenant: 'org_bharat_ai', toolName: 'clone_voice_face', riskLevel: 'critical', status: 'pending', inputs: { character_id: 'Meera_Central_Kerala_v2' } },
    { ticketId: 'ticket_34e910aa', user: 'user_devops_admin', tenant: 'org_bharat_ai', toolName: 'create_cloud_resource', riskLevel: 'high', status: 'pending', inputs: { resource_type: 'GKE_GPU_NodePool_H100', count: 4 } }
  ]);

  const handleReview = (ticketId: string, action: 'approve' | 'reject') => {
    setTickets((prev) =>
      prev.map((t) => (t.ticketId === ticketId ? { ...t, status: action === 'approve' ? 'approved' : 'rejected' } : t))
    );
  };

  return (
    <div className="p-8 space-y-6 text-gray-100 min-h-screen bg-[#080A0F]">
      <div className="flex items-center justify-between border-b border-white/10 pb-5">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-6 h-6 text-amber-400" />
            Human-in-the-Loop Approval Queue
          </h1>
          <p className="text-xs text-gray-400 mt-1">Review pending high-risk tool execution tickets before dispatching to external infrastructure.</p>
        </div>
      </div>

      <div className="space-y-4">
        {tickets.map((t) => (
          <div key={t.ticketId} className="p-5 rounded-2xl bg-white/5 border border-white/10 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-white font-mono">{t.ticketId}</span>
                <span className={`px-2 py-0.5 rounded-full text-[10px] uppercase font-bold ${
                  t.riskLevel === 'critical' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                }`}>
                  {t.riskLevel} Risk
                </span>
                <span className="text-xs text-gray-400">Tool: <strong className="text-amber-300 font-mono">{t.toolName}</strong></span>
              </div>
              <div className="text-xs text-gray-300">
                User: <span className="font-mono text-gray-400">{t.user}</span> | Tenant: <span className="font-mono text-gray-400">{t.tenant}</span>
              </div>
              <div className="text-xs text-gray-400 bg-black/40 p-2 rounded-lg font-mono border border-white/5 mt-2">
                Inputs: {JSON.stringify(t.inputs)}
              </div>
            </div>

            <div className="flex items-center gap-3">
              {t.status === 'pending' ? (
                <>
                  <button
                    onClick={() => handleReview(t.ticketId, 'reject')}
                    className="flex items-center gap-1.5 bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/40 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all"
                  >
                    <XCircle className="w-4 h-4" />
                    <span>Reject</span>
                  </button>
                  <button
                    onClick={() => handleReview(t.ticketId, 'approve')}
                    className="flex items-center gap-1.5 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 border border-emerald-500/40 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Approve & Execute</span>
                  </button>
                </>
              ) : (
                <span className={`px-3 py-1.5 rounded-xl text-xs font-semibold uppercase ${
                  t.status === 'approved' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40' : 'bg-red-500/20 text-red-300 border border-red-500/40'
                }`}>
                  {t.status}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
