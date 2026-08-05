'use client';

import React, { useState, useEffect } from 'react';
import {
  MessageSquare, Plus, Search, Sparkles, Image as ImageIcon, Video, FileText,
  Settings, UserCheck, Send, ShieldAlert, Cpu, Terminal, ArrowRight, CornerDownLeft,
  Volume2, Globe, Database, Layers, ChevronLeft, ChevronRight, Paperclip, Check,
  Copy, ChevronDown, ChevronUp, X, Play, Pause, Sliders, Zap, BarChart3, Lock,
  RefreshCw, Download, Share2, Maximize2, PanelLeftClose, PanelLeft, PanelRightClose,
  PanelRight, Mic, Sparkle, Bot, User, CheckCircle2, AlertCircle, FileCode, SlidersHorizontal,
  Flame, HardDrive, ArrowUpRight
} from 'lucide-react';

interface Citation {
  document_name: string;
  page?: number;
  snippet: string;
  relevance_score: number;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  language?: string;
  citations?: Citation[];
  codeBlock?: { language: string; code: string };
  timestamp: string;
  latencyMs?: number;
}

interface Character {
  id: string;
  name: string;
  region: string;
  attire: string;
  voice: string;
  status: 'Active Lock' | 'Ready' | 'Training';
  consentVerified: boolean;
  avatarGradient: string;
  description: string;
  keyframeLockCount: number;
}

interface LoRAAdapter {
  id: string;
  name: string;
  baseModel: string;
  bleuScore: number;
  accuracy: number;
  canaryTraffic: number;
  status: 'Production' | 'Canary Testing' | 'Training' | 'Archived';
  loss: number;
  epochsCompleted: number;
  totalEpochs: number;
}

interface MediaAsset {
  id: string;
  prompt: string;
  preset: string;
  aspectRatio: string;
  type: 'image' | 'video';
  status: 'rendered' | 'rendering';
  timestamp: string;
  gradientBg: string;
  likes: number;
}

export default function VoriqStudio() {
  // Navigation & View Layout State
  const [activeTab, setActiveTab] = useState<'chat' | 'characters' | 'media' | 'models'>('chat');
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true);
  const [searchThreadQuery, setSearchThreadQuery] = useState('');

  // Workspace Conversations State
  const [conversations, setConversations] = useState<Array<{ id: string; title: string; dialect: string; timestamp: string; count: number }>>([
    { id: 'conv_1', title: 'DPDP Act Compliance RAG', dialect: 'English', timestamp: '2m ago', count: 4 },
    { id: 'conv_2', title: 'Manglish Client Proposal', dialect: 'Manglish', timestamp: '1h ago', count: 8 },
    { id: 'conv_3', title: 'Fintech Hinglish Assistant', dialect: 'Hinglish', timestamp: '1d ago', count: 12 },
  ]);
  const [currentConvId, setCurrentConvId] = useState<string | null>('conv_1');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'msg_init_1',
      role: 'user',
      content: 'Can you summarize the key data protection provisions for Indian startups under DPDP Act 2023?',
      timestamp: '17:20',
    },
    {
      id: 'msg_init_2',
      role: 'assistant',
      content: 'Under the Digital Personal Data Protection (DPDP) Act 2023, Indian startups must adhere to strict data compliance frameworks. Key provisions include explicit consent architecture, data minimization, and mandatory breach notification within prescribed timelines.',
      language: 'English (Verified RAG)',
      timestamp: '17:21',
      latencyMs: 340,
      codeBlock: {
        language: 'typescript',
        code: `// Sample Voriq DPDP Consent Verification Middleware
import { VoriqGuardrail } from '@vorik/sdk';

export async function verifyUserConsent(userId: string, dataScope: string[]) {
  const audit = await VoriqGuardrail.auditConsent({
    tenantId: process.env.VORIK_TENANT_ID,
    userId,
    requestedScope: dataScope,
  });
  return audit.isCompliant;
}`
      },
      citations: [
        {
          document_name: 'Voriq_DPDP_Act_Summary.pdf',
          page: 4,
          snippet: 'Section 6(1): Data Fiduciaries must give clear notice to data principals before requesting consent for personal data processing.',
          relevance_score: 0.96,
        },
        {
          document_name: 'India_AI_OS_Compliance_Spec.pdf',
          page: 12,
          snippet: 'Zero-retention ephemeral inference pipelines ensure end-to-end data privacy across edge endpoints.',
          relevance_score: 0.91,
        }
      ]
    }
  ]);

  // Input & Execution State
  const [inputQuery, setInputQuery] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedModel, setSelectedModel] = useState('vorik-indic-v1');
  const [languageOverride, setLanguageOverride] = useState('auto');
  const [ragEnabled, setRagEnabled] = useState(true);
  const [expandedCitationId, setExpandedCitationId] = useState<string | null>(null);
  const [copiedCodeId, setCopiedCodeId] = useState<string | null>(null);

  // Agent Steps & Trace State
  const [agentSteps, setAgentSteps] = useState<Array<{ step: string; detail: string; status: 'done' | 'running' | 'waiting'; time: string }>>([
    { step: '1. Supervisor Intent Classifier', detail: 'Modality: Text | Dialect: English | RAG: Active', status: 'done', time: '12ms' },
    { step: '2. Vector DB Retrieval', detail: 'Scanned 14 collection chunks (Score > 0.88)', status: 'done', time: '85ms' },
    { step: '3. Model Router & Adapter', detail: 'Routed to meta-llama/Llama-3.3-70B + DPDP-LoRA', status: 'done', time: '140ms' },
    { step: '4. Stream Generation', detail: 'Token rate: 142 tokens/sec | Compliance Verified', status: 'done', time: '103ms' },
  ]);
  const [showRawLogs, setShowRawLogs] = useState(false);

  // Character Consistency State
  const [characters, setCharacters] = useState<Character[]>([
    {
      id: 'char_1',
      name: 'Meera',
      region: 'Central Kerala',
      attire: 'Contemporary Handloom Saree',
      voice: 'Malayalam TTS Engine v2 (24kHz)',
      status: 'Active Lock',
      consentVerified: true,
      avatarGradient: 'from-amber-500/30 via-yellow-600/20 to-neutral-900',
      description: 'Tech-savvy startup lead representation for South Indian regional campaigns.',
      keyframeLockCount: 48,
    },
    {
      id: 'char_2',
      name: 'Arjun',
      region: 'Telangana (Hyderabad Urban)',
      attire: 'Smart Casual Linen Blazer',
      voice: 'Telugu Neural TTS Engine',
      status: 'Ready',
      consentVerified: true,
      avatarGradient: 'from-orange-500/30 via-amber-600/20 to-neutral-900',
      description: 'Fintech narrator character tuned for clear code-mixed Telugu tutorials.',
      keyframeLockCount: 36,
    },
    {
      id: 'char_3',
      name: 'Ananya',
      region: 'Rajasthan (Jaipur Cultural)',
      attire: 'Heritage Zari Bandhani',
      voice: 'Hindi Neural Warm Tone',
      status: 'Active Lock',
      consentVerified: true,
      avatarGradient: 'from-yellow-500/30 via-orange-600/20 to-neutral-900',
      description: 'E-commerce ambassador character tailored for festive season video ads.',
      keyframeLockCount: 64,
    }
  ]);
  const [playingVoiceId, setPlayingVoiceId] = useState<string | null>(null);

  // Media Studio State
  const [mediaPrompt, setMediaPrompt] = useState('Modern Kerala tech hub office during golden hour with Meera in handloom attire...');
  const [mediaPreset, setMediaPreset] = useState('Kerala Backwaters Twilight');
  const [mediaAspectRatio, setMediaAspectRatio] = useState<'16:9' | '9:16' | '1:1' | '21:9'>('16:9');
  const [cameraAngle, setCameraAngle] = useState('Eye-Level Cinematic');
  const [generatedAssets, setGeneratedAssets] = useState<MediaAsset[]>([
    {
      id: 'asset_1',
      prompt: 'Meera leading an AI product demo in a modern Kochi tech studio at twilight.',
      preset: 'Kerala Backwaters Twilight',
      aspectRatio: '16:9',
      type: 'image',
      status: 'rendered',
      timestamp: '10m ago',
      gradientBg: 'from-amber-600/40 via-yellow-900/30 to-black',
      likes: 24,
    },
    {
      id: 'asset_2',
      prompt: 'Arjun speaking at a Hyderabad fintech launch keynote video storyboard.',
      preset: 'Mumbai Tech Hub Dusk',
      aspectRatio: '9:16',
      type: 'video',
      status: 'rendered',
      timestamp: '25m ago',
      gradientBg: 'from-orange-600/40 via-amber-950/30 to-black',
      likes: 19,
    }
  ]);

  // Fine-Tuning State
  const [adapters, setAdapters] = useState<LoRAAdapter[]>([
    {
      id: 'lora_1',
      name: 'Voriq-Indic-Foundation-70B-v1.4',
      baseModel: 'Meta Llama 3.3 70B Instruct',
      bleuScore: 44.8,
      accuracy: 99.4,
      canaryTraffic: 85.0,
      status: 'Production',
      loss: 0.124,
      epochsCompleted: 10,
      totalEpochs: 10,
    },
    {
      id: 'lora_2',
      name: 'Voriq-Manglish-CodeMixed-v2',
      baseModel: 'Mistral 7B Instruct v0.3',
      bleuScore: 41.2,
      accuracy: 97.8,
      canaryTraffic: 15.0,
      status: 'Canary Testing',
      loss: 0.188,
      epochsCompleted: 8,
      totalEpochs: 10,
    },
    {
      id: 'lora_3',
      name: 'Voriq-Legal-Indic-DPDP-v1',
      baseModel: 'Meta Llama 3.3 70B Instruct',
      bleuScore: 39.5,
      accuracy: 98.1,
      canaryTraffic: 0.0,
      status: 'Training',
      loss: 0.245,
      epochsCompleted: 4,
      totalEpochs: 10,
    }
  ]);

  // Create New Workspace Thread
  const createNewConversation = () => {
    const newId = `conv_${Date.now()}`;
    const newConv = {
      id: newId,
      title: 'New Workspace Thread',
      dialect: 'Auto',
      timestamp: 'Just now',
      count: 0
    };
    setConversations([newConv, ...conversations]);
    setCurrentConvId(newId);
    setMessages([]);
    setAgentSteps([
      { step: '1. Supervisor Initialized', detail: 'Thread state reset. Awaiting input.', status: 'done', time: '2ms' }
    ]);
  };

  // Handle Send Message
  const handleSendMessage = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputQuery.trim() || isGenerating) return;

    const queryText = inputQuery;
    setInputQuery('');
    setIsGenerating(true);

    if (!currentConvId) {
      const newId = `conv_${Date.now()}`;
      setConversations([{ id: newId, title: queryText.slice(0, 28) + '...', dialect: languageOverride, timestamp: 'Just now', count: 1 }, ...conversations]);
      setCurrentConvId(newId);
    }

    const userMsg: Message = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: queryText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);

    // Live Step Simulation
    setAgentSteps([
      { step: '1. Supervisor Router', detail: 'Classifying dialect & safety guardrails...', status: 'running', time: '...' },
      { step: '2. Vector RAG Retrieval', detail: 'Querying Qdrant index...', status: 'waiting', time: '...' },
      { step: '3. Dynamic LoRA Routing', detail: 'Selecting weights...', status: 'waiting', time: '...' },
      { step: '4. Stream Generation', detail: 'Preparing output stream...', status: 'waiting', time: '...' },
    ]);

    setTimeout(() => {
      setAgentSteps((prev) => [
        { ...prev[0], status: 'done', time: '14ms' },
        { ...prev[1], status: 'running', detail: 'Extracted 3 relevant doc passages' },
        prev[2],
        prev[3],
      ]);
    }, 400);

    setTimeout(() => {
      setAgentSteps((prev) => [
        prev[0],
        { ...prev[1], status: 'done', time: '78ms' },
        { ...prev[2], status: 'running', detail: 'Loaded Voriq-Indic-LoRA-v1.4' },
        prev[3],
      ]);
    }, 800);

    setTimeout(() => {
      const isManglish = /enikku|naale|cheyyamo|nalla|allenkil/i.test(queryText);
      const isHinglish = /kya|kar|karo|bhai|nahi|samajh/i.test(queryText);

      let detectedLang = 'English (Standard)';
      if (isManglish) detectedLang = '🇲🇱 Manglish / Malayalam Code-Mixed';
      else if (isHinglish) detectedLang = '🇮🇳 Hinglish / Hindi Code-Mixed';

      let replyContent = `Voriq AI Engine: Processed query "${queryText}".\n\n`;

      if (isManglish) {
        replyContent += `Enikku ningalude request manassilayi. Voriq Indic Engine uses localized South-Asian LLM adapters to respond with 99.2% cultural and linguistic precision.`;
      } else if (isHinglish) {
        replyContent += `Aapke request ko Voriq AI engine ne process kar liya hai. Self-hosted GPU infrastructure ensures low latency and complete tenant privacy.`;
      } else {
        replyContent += `The response has been computed via Voriq's self-hosted open-weight foundation model stack. RAG vector context and citation sources are attached below.`;
      }

      const assistantMsg: Message = {
        id: `asst_${Date.now()}`,
        role: 'assistant',
        content: replyContent,
        language: detectedLang,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        latencyMs: 312,
        citations: ragEnabled ? [
          {
            document_name: 'Voriq_Indic_Architecture_2026.pdf',
            page: 2,
            snippet: 'Dual-path script tokenizers preserve Romanised Indic nuances without vocabulary explosion.',
            relevance_score: 0.95
          }
        ] : undefined
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setAgentSteps((prev) => [
        prev[0],
        prev[1],
        { ...prev[2], status: 'done', time: '120ms' },
        { step: '4. Stream Generation', detail: 'Completed 164 tokens (312ms latency)', status: 'done', time: '312ms' },
      ]);
      setIsGenerating(false);
    }, 1300);
  };

  // Copy code helper
  const handleCopyCode = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCodeId(id);
    setTimeout(() => setCopiedCodeId(null), 2000);
  };

  // Quick Prompt Click
  const handleQuickPrompt = (prompt: string) => {
    setInputQuery(prompt);
  };

  const filteredConversations = conversations.filter((c) =>
    c.title.toLowerCase().includes(searchThreadQuery.toLowerCase())
  );

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#080A0F] text-gray-100 font-sans select-none">

      {/* ========================================================================= */}
      {/* 1. LEFT SIDEBAR: Linear-Inspired Glass Navigation & Thread Drawer        */}
      {/* ========================================================================= */}
      <aside
        className={`flex-shrink-0 border-r border-white/10 glass-panel flex flex-col justify-between transition-all duration-300 z-20 ${
          leftSidebarOpen ? 'w-72' : 'w-16'
        }`}
      >
        <div className="flex flex-col h-full overflow-hidden">
          {/* Header & Logo */}
          <div className="p-4 flex items-center justify-between border-b border-white/10">
            {leftSidebarOpen ? (
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-amber-500 to-yellow-400 flex items-center justify-center font-bold text-black shadow-lg shadow-amber-500/20">
                  <Sparkle className="w-5 h-5 fill-black" />
                </div>
                <div>
                  <h1 className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">
                    Voriq AI Studio
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 font-mono border border-amber-500/30">v2.4</span>
                  </h1>
                  <p className="text-[11px] text-gray-400">India-First Multimodal OS</p>
                </div>
              </div>
            ) : (
              <div className="mx-auto h-9 w-9 rounded-xl bg-gradient-to-tr from-amber-500 to-yellow-400 flex items-center justify-center font-bold text-black">
                <Sparkle className="w-5 h-5 fill-black" />
              </div>
            )}

            <button
              onClick={() => setLeftSidebarOpen(!leftSidebarOpen)}
              className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
              title={leftSidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
            >
              {leftSidebarOpen ? <PanelLeftClose className="w-4 h-4" /> : <PanelLeft className="w-4 h-4" />}
            </button>
          </div>

          {/* New Workspace Thread Button */}
          <div className="p-3">
            <button
              onClick={createNewConversation}
              className={`w-full flex items-center justify-center gap-2.5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500/20 via-yellow-500/15 to-amber-500/20 hover:from-amber-500/30 hover:to-yellow-500/30 border border-amber-500/40 text-amber-300 font-medium text-xs transition-all shadow-lg shadow-amber-500/10 ${
                !leftSidebarOpen && 'px-0'
              }`}
            >
              <Plus className="w-4 h-4 text-amber-400" />
              {leftSidebarOpen && <span>New Workspace Thread</span>}
            </button>
          </div>

          {/* Navigation Pill Tabs */}
          <div className="px-3 space-y-1 my-2">
            <button
              onClick={() => setActiveTab('chat')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'chat'
                  ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30 shadow-sm saffron-glow-sm'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              } ${!leftSidebarOpen && 'justify-center px-0'}`}
              title="AI Chat & RAG Studio"
            >
              <MessageSquare className="w-4 h-4 flex-shrink-0 text-amber-400" />
              {leftSidebarOpen && <span>AI Chat & RAG Studio</span>}
            </button>

            <button
              onClick={() => setActiveTab('characters')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'characters'
                  ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30 shadow-sm saffron-glow-sm'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              } ${!leftSidebarOpen && 'justify-center px-0'}`}
              title="Character Consistency Engine"
            >
              <UserCheck className="w-4 h-4 flex-shrink-0 text-amber-400" />
              {leftSidebarOpen && <span>Character Consistency</span>}
            </button>

            <button
              onClick={() => setActiveTab('media')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'media'
                  ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30 shadow-sm saffron-glow-sm'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              } ${!leftSidebarOpen && 'justify-center px-0'}`}
              title="Culturally Grounded Media Studio"
            >
              <Video className="w-4 h-4 flex-shrink-0 text-amber-400" />
              {leftSidebarOpen && <span>Media Studio</span>}
            </button>

            <button
              onClick={() => setActiveTab('models')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'models'
                  ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30 shadow-sm saffron-glow-sm'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              } ${!leftSidebarOpen && 'justify-center px-0'}`}
              title="Phase 2 Fine-Tuning Registry"
            >
              <Layers className="w-4 h-4 flex-shrink-0 text-amber-400" />
              {leftSidebarOpen && <span>Fine-Tuning Registry</span>}
            </button>
          </div>

          {/* Recent Workspace Threads Section (when Chat tab active & expanded) */}
          {leftSidebarOpen && activeTab === 'chat' && (
            <div className="flex-1 overflow-hidden flex flex-col px-3 pt-3 border-t border-white/10">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
                  Recent Threads
                </span>
                <span className="text-[10px] bg-white/10 px-1.5 py-0.5 rounded text-gray-300 font-mono">
                  {conversations.length}
                </span>
              </div>

              {/* Thread Search Filter */}
              <div className="relative mb-2">
                <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-gray-500" />
                <input
                  type="text"
                  placeholder="Filter threads..."
                  value={searchThreadQuery}
                  onChange={(e) => setSearchThreadQuery(e.target.value)}
                  className="w-full bg-black/40 border border-white/10 rounded-lg pl-8 pr-3 py-1.5 text-[11px] text-gray-200 focus:outline-none focus:border-amber-500/40"
                />
              </div>

              {/* Thread List */}
              <div className="flex-1 overflow-y-auto space-y-1 pr-1">
                {filteredConversations.length === 0 ? (
                  <div className="text-[11px] text-gray-500 text-center py-6 italic">
                    No matching threads found.
                  </div>
                ) : (
                  filteredConversations.map((conv) => (
                    <button
                      key={conv.id}
                      onClick={() => setCurrentConvId(conv.id)}
                      className={`w-full text-left p-2.5 rounded-xl text-xs transition-all flex flex-col gap-1 border ${
                        currentConvId === conv.id
                          ? 'bg-amber-500/10 border-amber-500/30 text-white font-medium shadow-sm'
                          : 'border-transparent text-gray-400 hover:text-gray-200 hover:bg-white/5'
                      }`}
                    >
                      <div className="flex items-center justify-between w-full">
                        <span className="truncate pr-2">{conv.title}</span>
                        <span className="text-[10px] text-gray-500 flex-shrink-0">{conv.timestamp}</span>
                      </div>
                      <div className="flex items-center gap-2 text-[10px] text-gray-500">
                        <span className="px-1.5 py-0.2 rounded bg-white/5 border border-white/10 text-amber-400 font-mono">
                          {conv.dialect}
                        </span>
                        <span>• {conv.count} messages</span>
                      </div>
                    </button>
                  ))
                )}
              </div>
            </div>
          )}

          {/* User Tenant / Org Card at Bottom */}
          <div className="p-3 border-t border-white/10 mt-auto bg-black/30">
            {leftSidebarOpen ? (
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-amber-500/20 to-yellow-600/20 border border-amber-500/40 flex items-center justify-center font-bold text-xs text-amber-400">
                    BH
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-white tracking-tight">Bharat AI Enterprise</div>
                    <div className="text-[10px] text-amber-400/80 flex items-center gap-1">
                      <span className="h-1.5 w-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                      Super Admin Tenant
                    </div>
                  </div>
                </div>
                <Settings className="w-4 h-4 text-gray-400 hover:text-white cursor-pointer transition-colors" />
              </div>
            ) : (
              <div className="mx-auto h-8 w-8 rounded-lg bg-amber-500/20 border border-amber-500/40 flex items-center justify-center font-bold text-xs text-amber-400">
                BH
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* ========================================================================= */}
      {/* 2. MAIN WORKSPACE: Header Bar & Interactive Dynamic Canvas               */}
      {/* ========================================================================= */}
      <main className="flex-1 flex flex-col overflow-hidden relative bg-[#080A0F]">

        {/* Top Control Bar Header */}
        <header className="h-14 border-b border-white/10 glass-panel px-6 flex items-center justify-between z-10">
          {/* Left: Model & Language Selectors */}
          <div className="flex items-center gap-3">
            {/* Model Pill Switcher */}
            <div className="flex items-center gap-2 bg-black/40 border border-white/10 rounded-xl px-3 py-1.5">
              <Cpu className="w-4 h-4 text-amber-400" />
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="bg-transparent text-xs text-white font-medium focus:outline-none cursor-pointer pr-1"
              >
                <option value="vorik-indic-v1" className="bg-neutral-900 text-white">Voriq Indic Foundation V1 (70B)</option>
                <option value="meta-llama-3.3-70b" className="bg-neutral-900 text-white">Meta Llama 3.3 70B Instruct</option>
                <option value="mistral-7b-indic" className="bg-neutral-900 text-white">Mistral 7B + Hinglish LoRA</option>
                <option value="vorik-vision-v2" className="bg-neutral-900 text-white">Voriq Vision-Pro V2 Multimodal</option>
              </select>
            </div>

            {/* Language Dialect Switcher */}
            <div className="flex items-center gap-2 bg-black/40 border border-white/10 rounded-xl px-3 py-1.5">
              <Globe className="w-4 h-4 text-amber-400" />
              <select
                value={languageOverride}
                onChange={(e) => setLanguageOverride(e.target.value)}
                className="bg-transparent text-xs text-white font-medium focus:outline-none cursor-pointer pr-1"
              >
                <option value="auto" className="bg-neutral-900 text-white">🌐 Auto Language Detection</option>
                <option value="hindi" className="bg-neutral-900 text-white">🇮🇳 Hindi (Devanagari / Hinglish)</option>
                <option value="malayalam" className="bg-neutral-900 text-white">🇲🇱 Malayalam (Malayalam / Manglish)</option>
                <option value="tamil" className="bg-neutral-900 text-white">🇹🇲 Tamil (Tamil / Tanglish)</option>
                <option value="telugu" className="bg-neutral-900 text-white">🇨🇳 Telugu (Telugu / Tenglish)</option>
              </select>
            </div>

            {/* RAG Vector Index Toggle */}
            <button
              onClick={() => setRagEnabled(!ragEnabled)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                ragEnabled
                  ? 'bg-amber-500/15 border-amber-500/40 text-amber-300 shadow-sm'
                  : 'bg-black/40 border-white/10 text-gray-400 hover:text-white'
              }`}
            >
              <Database className="w-3.5 h-3.5 text-amber-400" />
              <span>RAG Knowledge Index</span>
              <span className={`h-2 w-2 rounded-full ${ragEnabled ? 'bg-green-400 animate-pulse' : 'bg-gray-600'}`}></span>
            </button>
          </div>

          {/* Right: Cluster Status & Drawer Toggle */}
          <div className="flex items-center gap-3 text-xs">
            <div className="hidden md:flex items-center gap-2 bg-white/5 border border-white/10 px-3 py-1 rounded-full text-gray-300">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping"></span>
              <span className="font-mono text-[11px]">8x H100 SXM5 — Active</span>
              <span className="text-gray-500">•</span>
              <span className="text-amber-400 font-mono">$0.0004 / msg</span>
            </div>

            <button
              onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
              className={`p-2 rounded-xl border transition-all ${
                rightSidebarOpen
                  ? 'bg-amber-500/20 border-amber-500/40 text-amber-300'
                  : 'bg-black/40 border-white/10 text-gray-400 hover:text-white'
              }`}
              title="Toggle Agent Activity Reasoning Drawer"
            >
              <Terminal className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Dynamic Main Workspace Content Canvas */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">

          {/* --------------------------------------------------------------------- */}
          {/* TAB 1: AI STUDIO CHAT & RAG WORKSPACE                                 */}
          {/* --------------------------------------------------------------------- */}
          {activeTab === 'chat' && (
            messages.length === 0 ? (
              /* Minimalist Empty Workspace State */
              <div className="h-full flex flex-col items-center justify-center max-w-2xl mx-auto py-12 text-center space-y-8">
                {/* Hero Glow Icon */}
                <div className="relative">
                  <div className="absolute -inset-4 bg-gradient-to-tr from-amber-500 to-yellow-600 rounded-3xl opacity-20 blur-xl animate-pulse-glow"></div>
                  <div className="relative h-20 w-20 rounded-2xl bg-gradient-to-b from-neutral-900 to-black border border-amber-500/40 flex items-center justify-center text-amber-400 shadow-2xl saffron-glow">
                    <Sparkles className="w-10 h-10" />
                  </div>
                </div>

                <div>
                  <h2 className="text-2xl font-bold text-white tracking-tight mb-2">
                    Voriq AI Multimodal Studio
                  </h2>
                  <p className="text-xs text-gray-400 max-w-md mx-auto leading-relaxed">
                    India-first foundation intelligence with code-mixed Indic tokenizers, RAG citations, and character profile consistency locks.
                  </p>
                </div>

                {/* Floating Quick-Prompt Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full">
                  <button
                    onClick={() => handleQuickPrompt("Enikku tomorrow client meeting undu. Prepare cheyyan key points suggest cheyyamo?")}
                    className="p-4 glass-panel glass-panel-hover rounded-2xl text-left border border-white/10 flex flex-col justify-between gap-3 group transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30">
                        🇲🇱 Manglish / Code-Mixed
                      </span>
                      <ArrowUpRight className="w-4 h-4 text-gray-500 group-hover:text-amber-400 transition-colors" />
                    </div>
                    <p className="text-xs text-gray-300 font-medium">
                      "Enikku tomorrow client meeting undu. Prepare cheyyan key points..."
                    </p>
                    <span className="text-[10px] text-gray-500">Regional Indic Dialect Router</span>
                  </button>

                  <button
                    onClick={() => handleQuickPrompt("Draft a DPDP Act 2023 compliance checklist for SaaS startup user consent.")}
                    className="p-4 glass-panel glass-panel-hover rounded-2xl text-left border border-white/10 flex flex-col justify-between gap-3 group transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30">
                        📄 DPDP Act 2023 RAG
                      </span>
                      <ArrowUpRight className="w-4 h-4 text-gray-500 group-hover:text-amber-400 transition-colors" />
                    </div>
                    <p className="text-xs text-gray-300 font-medium">
                      "Draft a DPDP Act 2023 compliance checklist for SaaS startup..."
                    </p>
                    <span className="text-[10px] text-gray-500">Indexed Document Citation Engine</span>
                  </button>

                  <button
                    onClick={() => handleQuickPrompt("Mere nayi AI startup ke liye investor pitch deck outline ready karo with Hinglish tone.")}
                    className="p-4 glass-panel glass-panel-hover rounded-2xl text-left border border-white/10 flex flex-col justify-between gap-3 group transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30">
                        🇮🇳 Hinglish Business
                      </span>
                      <ArrowUpRight className="w-4 h-4 text-gray-500 group-hover:text-amber-400 transition-colors" />
                    </div>
                    <p className="text-xs text-gray-300 font-medium">
                      "Mere nayi AI startup ke liye investor pitch deck outline..."
                    </p>
                    <span className="text-[10px] text-gray-500">Fine-Tuned Llama 3.3 Adapter</span>
                  </button>

                  <button
                    onClick={() => handleQuickPrompt("Write a high-performance Rust service for Indic text tokenization with zero memory allocation.")}
                    className="p-4 glass-panel glass-panel-hover rounded-2xl text-left border border-white/10 flex flex-col justify-between gap-3 group transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30">
                        💻 Polyglot Code
                      </span>
                      <ArrowUpRight className="w-4 h-4 text-gray-500 group-hover:text-amber-400 transition-colors" />
                    </div>
                    <p className="text-xs text-gray-300 font-medium">
                      "Write a high-performance Rust service for Indic text tokenization..."
                    </p>
                    <span className="text-[10px] text-gray-500">Syntax Highlighted Code Generation</span>
                  </button>
                </div>
              </div>
            ) : (
              /* Active Chat Stream View */
              <div className="space-y-6 max-w-3xl mx-auto pb-24">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex flex-col gap-2 ${
                      msg.role === 'user' ? 'items-end' : 'items-start'
                    }`}
                  >
                    {/* Role Header */}
                    <div className="flex items-center gap-2 text-xs text-gray-400 px-1">
                      {msg.role === 'user' ? (
                        <>
                          <span>You</span>
                          <User className="w-3.5 h-3.5 text-amber-400" />
                        </>
                      ) : (
                        <>
                          <div className="h-4 w-4 rounded bg-amber-500 flex items-center justify-center text-black font-bold text-[9px]">V</div>
                          <span className="font-semibold text-white">Voriq AI Engine</span>
                          {msg.language && (
                            <span className="bg-amber-500/15 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded text-[10px] font-mono">
                              {msg.language}
                            </span>
                          )}
                          {msg.latencyMs && (
                            <span className="text-[10px] text-gray-500 font-mono">
                              • {msg.latencyMs}ms
                            </span>
                          )}
                        </>
                      )}
                    </div>

                    {/* Message Bubble Container */}
                    <div
                      className={`p-4 rounded-2xl text-xs leading-relaxed max-w-2xl border transition-all ${
                        msg.role === 'user'
                          ? 'bg-amber-500/10 border-amber-500/30 text-gray-100 rounded-tr-none'
                          : 'glass-panel border-white/10 text-gray-200 rounded-tl-none shadow-lg'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{msg.content}</div>

                      {/* Code Block Renderer */}
                      {msg.codeBlock && (
                        <div className="mt-3 rounded-xl overflow-hidden border border-white/10 bg-black/60 font-mono text-[11px]">
                          <div className="bg-white/5 px-3 py-1.5 flex items-center justify-between border-b border-white/10 text-gray-400">
                            <span className="flex items-center gap-1.5">
                              <FileCode className="w-3.5 h-3.5 text-amber-400" />
                              {msg.codeBlock.language}
                            </span>
                            <button
                              onClick={() => handleCopyCode(msg.codeBlock!.code, msg.id)}
                              className="flex items-center gap-1 text-[10px] text-gray-400 hover:text-white transition-colors"
                            >
                              {copiedCodeId === msg.id ? (
                                <>
                                  <Check className="w-3 h-3 text-green-400" />
                                  <span className="text-green-400">Copied!</span>
                                </>
                              ) : (
                                <>
                                  <Copy className="w-3 h-3" />
                                  <span>Copy</span>
                                </>
                              )}
                            </button>
                          </div>
                          <pre className="p-3 overflow-x-auto text-amber-200/90 leading-normal">
                            <code>{msg.codeBlock.code}</code>
                          </pre>
                        </div>
                      )}

                      {/* Citation Accordion Cards */}
                      {msg.citations && msg.citations.length > 0 && (
                        <div className="mt-4 pt-3 border-t border-white/10 space-y-2">
                          <div className="text-[11px] font-semibold text-amber-400 flex items-center gap-1.5">
                            <Database className="w-3.5 h-3.5" />
                            RAG Citations & Grounding Sources ({msg.citations.length})
                          </div>
                          <div className="space-y-1.5">
                            {msg.citations.map((cit, idx) => (
                              <div
                                key={idx}
                                className="bg-black/40 border border-white/10 rounded-xl p-2.5 text-[11px] transition-all"
                              >
                                <div
                                  onClick={() => setExpandedCitationId(expandedCitationId === `${msg.id}_${idx}` ? null : `${msg.id}_${idx}`)}
                                  className="flex items-center justify-between cursor-pointer text-gray-300 hover:text-white"
                                >
                                  <span className="flex items-center gap-2 font-medium">
                                    <FileText className="w-3.5 h-3.5 text-amber-400" />
                                    {cit.document_name} {cit.page && <span className="text-gray-500">(p. {cit.page})</span>}
                                  </span>
                                  <div className="flex items-center gap-2">
                                    <span className="px-1.5 py-0.5 rounded bg-green-500/20 text-green-400 font-mono text-[10px]">
                                      {(cit.relevance_score * 100).toFixed(0)}% Match
                                    </span>
                                    {expandedCitationId === `${msg.id}_${idx}` ? (
                                      <ChevronUp className="w-3.5 h-3.5 text-gray-400" />
                                    ) : (
                                      <ChevronDown className="w-3.5 h-3.5 text-gray-400" />
                                    )}
                                  </div>
                                </div>
                                {expandedCitationId === `${msg.id}_${idx}` && (
                                  <div className="mt-2 pt-2 border-t border-white/5 text-gray-400 bg-white/5 p-2 rounded-lg italic leading-relaxed">
                                    "{cit.snippet}"
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )
          )}

          {/* --------------------------------------------------------------------- */}
          {/* TAB 2: CHARACTER PROFILE CONSISTENCY ENGINE                           */}
          {/* --------------------------------------------------------------------- */}
          {activeTab === 'characters' && (
            <div className="max-w-5xl mx-auto space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-white flex items-center gap-2">
                    <UserCheck className="w-6 h-6 text-amber-400" />
                    Character Profile Consistency Engine
                  </h2>
                  <p className="text-xs text-gray-400">
                    Lock identity, regional attire, synthetic voice models, and DPDP consent compliance across video renders.
                  </p>
                </div>
                <button className="px-4 py-2 bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-600 hover:to-yellow-700 text-black font-semibold rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-amber-500/20 transition-all">
                  <Plus className="w-4 h-4" /> Add Character Profile
                </button>
              </div>

              {/* Character Profile Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {characters.map((char) => (
                  <div
                    key={char.id}
                    className="glass-panel glass-panel-hover p-5 rounded-2xl border border-white/10 flex flex-col justify-between space-y-4"
                  >
                    <div>
                      {/* Avatar Header */}
                      <div className="flex items-center gap-3 mb-3">
                        <div className={`h-12 w-12 rounded-xl bg-gradient-to-br ${char.avatarGradient} border border-amber-500/40 flex items-center justify-center font-bold text-amber-400 text-base shadow-md`}>
                          {char.name[0]}
                        </div>
                        <div>
                          <h3 className="font-bold text-sm text-white flex items-center gap-2">
                            {char.name}
                            <span className="text-[10px] bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full border border-green-500/30 flex items-center gap-1">
                              <CheckCircle2 className="w-3 h-3" /> {char.status}
                            </span>
                          </h3>
                          <p className="text-[11px] text-amber-400 font-medium">{char.region}</p>
                        </div>
                      </div>

                      <p className="text-xs text-gray-300 leading-relaxed mb-4">
                        {char.description}
                      </p>

                      {/* Attribute Badges */}
                      <div className="space-y-2 text-[11px] bg-black/40 p-3 rounded-xl border border-white/5">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Attire Lock:</span>
                          <span className="text-gray-200 font-medium">{char.attire}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Voice TTS:</span>
                          <span className="text-amber-400 font-mono">{char.voice}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Keyframe Locks:</span>
                          <span className="text-gray-200 font-mono">{char.keyframeLockCount} Keyframes</span>
                        </div>
                      </div>
                    </div>

                    {/* Interactive Voice Audio Preview Button */}
                    <div className="pt-2 border-t border-white/10 flex items-center justify-between">
                      <button
                        onClick={() => setPlayingVoiceId(playingVoiceId === char.id ? null : char.id)}
                        className={`w-full py-2 px-3 rounded-xl border text-xs font-medium flex items-center justify-center gap-2 transition-all ${
                          playingVoiceId === char.id
                            ? 'bg-amber-500/20 border-amber-500/40 text-amber-300'
                            : 'bg-white/5 border-white/10 text-gray-300 hover:text-white hover:bg-white/10'
                        }`}
                      >
                        {playingVoiceId === char.id ? (
                          <>
                            <Pause className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
                            <span>Playing Neural Sample...</span>
                          </>
                        ) : (
                          <>
                            <Volume2 className="w-3.5 h-3.5 text-amber-400" />
                            <span>Test Voice Clone</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* --------------------------------------------------------------------- */}
          {/* TAB 3: CULTURALLY GROUNDED MEDIA STUDIO                              */}
          {/* --------------------------------------------------------------------- */}
          {activeTab === 'media' && (
            <div className="max-w-5xl mx-auto space-y-6">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Video className="w-6 h-6 text-amber-400" />
                  Culturally Grounded Media Studio
                </h2>
                <p className="text-xs text-gray-400">
                  Generate Indian regional visual assets, aspect-ratio formatted storyboards, and high-fidelity video clips.
                </p>
              </div>

              {/* Media Prompt Controls Panel */}
              <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-gray-300 flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-amber-400" />
                    Multimodal Storyboard Prompt Generator
                  </span>
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] text-gray-400">Aspect Ratio:</span>
                    {(['16:9', '9:16', '1:1', '21:9'] as const).map((ratio) => (
                      <button
                        key={ratio}
                        onClick={() => setMediaAspectRatio(ratio)}
                        className={`px-2.5 py-1 rounded-lg text-xs font-mono transition-all border ${
                          mediaAspectRatio === ratio
                            ? 'bg-amber-500/20 border-amber-500/40 text-amber-300'
                            : 'bg-black/40 border-white/10 text-gray-400 hover:text-white'
                        }`}
                      >
                        {ratio}
                      </button>
                    ))}
                  </div>
                </div>

                <textarea
                  value={mediaPrompt}
                  onChange={(e) => setMediaPrompt(e.target.value)}
                  placeholder="Describe regional scene prompt (e.g. Modern Kerala tech hub office during golden hour with Meera in handloom saree)..."
                  className="w-full h-24 bg-black/50 border border-white/10 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-amber-500/50 resize-none"
                />

                {/* Cultural Presets & Camera Options */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="text-[11px] text-gray-400 mb-1 block">Regional Cultural Preset:</label>
                    <select
                      value={mediaPreset}
                      onChange={(e) => setMediaPreset(e.target.value)}
                      className="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500/40"
                    >
                      <option value="Kerala Backwaters Twilight">Kerala Backwaters Twilight</option>
                      <option value="Jaipur Palace Dawn">Jaipur Palace Dawn</option>
                      <option value="Mumbai Tech Hub Dusk">Mumbai Tech Hub Dusk</option>
                      <option value="Kolkata Heritage Golden Hour">Kolkata Heritage Golden Hour</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-[11px] text-gray-400 mb-1 block">Camera Angle & Lighting:</label>
                    <select
                      value={cameraAngle}
                      onChange={(e) => setCameraAngle(e.target.value)}
                      className="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500/40"
                    >
                      <option value="Eye-Level Cinematic">Eye-Level Cinematic</option>
                      <option value="Drone Aerial Sweep">Drone Aerial Sweep</option>
                      <option value="Low Angle Dynamic">Low Angle Dynamic</option>
                      <option value="Macro Close-Up Detail">Macro Close-Up Detail</option>
                    </select>
                  </div>
                </div>

                <div className="flex justify-end gap-3 pt-2">
                  <button className="px-4 py-2.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-xs font-medium text-white flex items-center gap-2 transition-all">
                    <ImageIcon className="w-4 h-4 text-amber-400" /> Generate Image Frame
                  </button>
                  <button className="px-4 py-2.5 bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-600 hover:to-yellow-700 text-black font-semibold rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-amber-500/20 transition-all">
                    <Video className="w-4 h-4" /> Render Storyboard Video Clip
                  </button>
                </div>
              </div>

              {/* Rendered Asset Showcase */}
              <div>
                <h3 className="text-sm font-semibold text-white mb-3">Rendered Visual Assets</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {generatedAssets.map((asset) => (
                    <div
                      key={asset.id}
                      className="glass-panel p-4 rounded-2xl border border-white/10 space-y-3"
                    >
                      {/* Visual Mock Canvas Box */}
                      <div className={`h-48 rounded-xl bg-gradient-to-br ${asset.gradientBg} border border-white/10 flex flex-col justify-between p-4 relative overflow-hidden group`}>
                        <div className="flex items-center justify-between z-10">
                          <span className="px-2 py-0.5 rounded bg-black/60 border border-white/10 text-amber-400 font-mono text-[10px]">
                            {asset.preset}
                          </span>
                          <span className="px-2 py-0.5 rounded bg-black/60 border border-white/10 text-gray-300 font-mono text-[10px]">
                            {asset.aspectRatio}
                          </span>
                        </div>

                        <div className="z-10 flex items-center justify-between">
                          <span className="text-[11px] text-gray-300 font-medium line-clamp-1 bg-black/50 px-2 py-1 rounded">
                            {asset.prompt}
                          </span>
                          <button className="p-2 rounded-xl bg-amber-500 text-black font-bold hover:scale-105 transition-all shadow-lg">
                            <Play className="w-4 h-4 fill-black" />
                          </button>
                        </div>
                      </div>

                      <div className="flex items-center justify-between text-xs text-gray-400">
                        <span>{asset.timestamp}</span>
                        <div className="flex items-center gap-3">
                          <button className="hover:text-white flex items-center gap-1">
                            <Download className="w-3.5 h-3.5" /> Save
                          </button>
                          <button className="hover:text-white flex items-center gap-1">
                            <Share2 className="w-3.5 h-3.5" /> Share
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* --------------------------------------------------------------------- */}
          {/* TAB 4: PHASE 2 FINE-TUNING REGISTRY & ADAPTER BENCHMARKS              */}
          {/* --------------------------------------------------------------------- */}
          {activeTab === 'models' && (
            <div className="max-w-5xl mx-auto space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-bold text-white flex items-center gap-2">
                    <Layers className="w-6 h-6 text-amber-400" />
                    Phase 2 Fine-Tuning Registry & LoRA Benchmarks
                  </h2>
                  <p className="text-xs text-gray-400">
                    Track custom open-weight Indic LoRA adapters, BLEU translation scores, canary allocations, and GPU training curves.
                  </p>
                </div>
                <button className="px-4 py-2 bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-600 hover:to-yellow-700 text-black font-semibold rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-amber-500/20 transition-all">
                  <Plus className="w-4 h-4" /> Deploy Custom LoRA Adapter
                </button>
              </div>

              {/* Adapter Cards List */}
              <div className="space-y-4">
                {adapters.map((lora) => (
                  <div
                    key={lora.id}
                    className="glass-panel p-6 rounded-2xl border border-white/10 space-y-4"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-bold text-sm text-white flex items-center gap-2">
                          {lora.name}
                          <span className={`text-[10px] px-2 py-0.5 rounded-full border font-mono ${
                            lora.status === 'Production'
                              ? 'bg-green-500/20 text-green-400 border-green-500/30'
                              : lora.status === 'Canary Testing'
                              ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
                              : 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                          }`}>
                            {lora.status}
                          </span>
                        </h3>
                        <p className="text-xs text-gray-400">Base Model: <span className="text-gray-200">{lora.baseModel}</span></p>
                      </div>

                      <div className="text-right">
                        <div className="text-xs text-gray-400">Canary Allocation</div>
                        <div className="text-base font-bold text-amber-400 font-mono">{lora.canaryTraffic}% Traffic</div>
                      </div>
                    </div>

                    {/* Benchmark Metrics Grid */}
                    <div className="grid grid-cols-4 gap-3 text-xs">
                      <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                        <div className="text-gray-400 mb-1">BLEU Score</div>
                        <div className="text-base font-bold text-white font-mono">{lora.bleuScore}</div>
                      </div>
                      <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                        <div className="text-gray-400 mb-1">Indic Accuracy</div>
                        <div className="text-base font-bold text-green-400 font-mono">{lora.accuracy}%</div>
                      </div>
                      <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                        <div className="text-gray-400 mb-1">Training Loss</div>
                        <div className="text-base font-bold text-amber-400 font-mono">{lora.loss}</div>
                      </div>
                      <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                        <div className="text-gray-400 mb-1">Epochs</div>
                        <div className="text-base font-bold text-gray-200 font-mono">{lora.epochsCompleted} / {lora.totalEpochs}</div>
                      </div>
                    </div>

                    {/* Progress Bar for Training */}
                    {lora.status === 'Training' && (
                      <div className="space-y-1.5 pt-2">
                        <div className="flex justify-between text-[11px] text-gray-400">
                          <span>Training Progress (Epoch 4/10)</span>
                          <span className="text-amber-400 font-mono">40%</span>
                        </div>
                        <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden border border-white/10">
                          <div className="bg-gradient-to-r from-amber-500 to-yellow-400 h-full w-[40%] animate-pulse"></div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* --------------------------------------------------------------------- */}
        {/* FLOATING GLASS CHAT INPUT BAR (For Chat Tab)                         */}
        {/* --------------------------------------------------------------------- */}
        {activeTab === 'chat' && (
          <div className="p-4 absolute bottom-0 left-0 right-0 pointer-events-none flex justify-center z-30">
            <form
              onSubmit={handleSendMessage}
              className="w-full max-w-3xl pointer-events-auto glass-input-bar rounded-2xl p-2 flex items-center gap-2"
            >
              <button
                type="button"
                className="p-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                title="Attach Document for RAG Context"
              >
                <Paperclip className="w-4 h-4" />
              </button>

              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder="Ask Voriq AI in English or Romanised Indic (e.g. Hinglish, Manglish)..."
                className="flex-1 bg-transparent border-none text-xs text-white focus:outline-none px-2 py-1.5 placeholder-gray-500"
              />

              <button
                type="button"
                className="p-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/10 transition-colors hidden sm:block"
                title="Voice Input"
              >
                <Mic className="w-4 h-4" />
              </button>

              <button
                type="submit"
                disabled={isGenerating || !inputQuery.trim()}
                className="bg-gradient-to-tr from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 disabled:opacity-40 text-black font-bold p-2.5 rounded-xl transition-all shadow-lg shadow-amber-500/20 flex items-center justify-center"
              >
                {isGenerating ? (
                  <RefreshCw className="w-4 h-4 animate-spin text-black" />
                ) : (
                  <Send className="w-4 h-4 fill-black" />
                )}
              </button>
            </form>
          </div>
        )}

      </main>

      {/* ========================================================================= */}
      {/* 3. RIGHT SIDEBAR: Agent Activity Reasoning & Trace Drawer                 */}
      {/* ========================================================================= */}
      {rightSidebarOpen && (
        <aside className="w-80 flex-shrink-0 glass-panel border-l border-white/10 p-4 flex flex-col justify-between z-20 overflow-y-auto">
          <div>
            {/* Header */}
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-white/10">
              <div className="flex items-center gap-2 text-xs font-bold text-amber-400 uppercase tracking-wider">
                <Terminal className="w-4 h-4" />
                Agent Activity Trace
              </div>
              <button
                onClick={() => setRightSidebarOpen(false)}
                className="text-gray-500 hover:text-white p-1 rounded-lg"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Trace Step Pipeline */}
            <div className="space-y-3 mb-6">
              {agentSteps.map((step, idx) => (
                <div
                  key={idx}
                  className="bg-black/40 p-3 rounded-xl border border-white/10 text-xs space-y-1 transition-all"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-white flex items-center gap-1.5">
                      {step.status === 'done' ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-green-400" />
                      ) : step.status === 'running' ? (
                        <RefreshCw className="w-3.5 h-3.5 text-amber-400 animate-spin" />
                      ) : (
                        <span className="h-2 w-2 rounded-full bg-gray-600"></span>
                      )}
                      {step.step}
                    </span>
                    <span className="text-[10px] font-mono text-amber-400/80">{step.time}</span>
                  </div>
                  <p className="text-[11px] text-gray-400 pl-5 leading-relaxed">
                    {step.detail}
                  </p>
                </div>
              ))}
            </div>

            {/* Toggle Raw JSON Inspector */}
            <button
              onClick={() => setShowRawLogs(!showRawLogs)}
              className="w-full py-2 px-3 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-xs text-gray-300 font-mono flex items-center justify-between transition-colors mb-4"
            >
              <span>{showRawLogs ? 'Hide Raw Execution JSON' : 'Inspect Raw Log JSON'}</span>
              <FileCode className="w-3.5 h-3.5 text-amber-400" />
            </button>

            {showRawLogs && (
              <div className="bg-black/80 p-3 rounded-xl border border-white/10 text-[10px] font-mono text-green-400 overflow-x-auto max-h-48 mb-4">
                <pre>{JSON.stringify({ tenant: "Bharat AI Org", model: selectedModel, rag_docs: 14, steps: agentSteps }, null, 2)}</pre>
              </div>
            )}
          </div>

          {/* Security Assurance Card */}
          <div className="bg-amber-500/10 p-3.5 rounded-xl border border-amber-500/30 text-[11px] text-gray-300 space-y-1.5">
            <div className="font-semibold text-amber-400 flex items-center gap-1.5">
              <ShieldAlert className="w-3.5 h-3.5" />
              Voriq Security Assurance
            </div>
            <div className="text-[10px] text-gray-400 space-y-1">
              <div>✓ DPDP Act 2023 Ephemeral Inference</div>
              <div>✓ Air-Gapped Tenant Data Isolation</div>
              <div>✓ Certified Synthetic Consent Logs</div>
            </div>
          </div>
        </aside>
      )}

    </div>
  );
}
