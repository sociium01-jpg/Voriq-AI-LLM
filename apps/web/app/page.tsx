'use client';

import React, { useState } from 'react';
import {
  MessageSquare, Plus, Search, Sparkles, Image as ImageIcon, Video, FileText,
  Settings, UserCheck, Send, ShieldAlert, Cpu, Terminal, ArrowRight, CornerDownLeft,
  Volume2, Globe, Database, Layers
} from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  language?: string;
  citations?: { document_name: string; snippet: string }[];
}

export default function VoriqStudio() {
  const [activeTab, setActiveTab] = useState<'chat' | 'characters' | 'media' | 'models'>('chat');
  const [conversations, setConversations] = useState<{ id: string; title: string }[]>([]);
  const [currentConvId, setCurrentConvId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputQuery, setInputQuery] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedModel, setSelectedModel] = useState('vorik-indic-v1');
  const [languageOverride, setLanguageOverride] = useState('auto');
  const [agentSteps, setAgentSteps] = useState<string[]>([]);
  const [characterName, setCharacterName] = useState('Meera');

  const createNewConversation = () => {
    const id = `conv_${Date.now()}`;
    const newConv = { id, title: 'New Conversation' };
    setConversations([newConv, ...conversations]);
    setCurrentConvId(id);
    setMessages([]);
    setAgentSteps([]);
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputQuery.trim() || isGenerating) return;

    if (!currentConvId) {
      const id = `conv_${Date.now()}`;
      setConversations([{ id, title: inputQuery.slice(0, 30) + '...' }, ...conversations]);
      setCurrentConvId(id);
    }

    const userMsg: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: inputQuery
    };
    setMessages((prev) => [...prev, userMsg]);
    const currentInput = inputQuery;
    setInputQuery('');
    setIsGenerating(true);

    // Simulate Agent Step Breakdown
    setAgentSteps([
      'Step 1: Supervisor Router classifying query modality and Indic dialect...',
      'Step 2: Indic Engine detected text structure and script confidence (0.95)',
      'Step 3: Model Router assigned model: meta-llama/Llama-3.3-70B + Indic-Romanised-LoRA',
      'Step 4: Generating stateful response via LangGraph supervisor...'
    ]);

    setTimeout(() => {
      const isIndic = /kya|kar|enikku|vanakkam|namaste/i.test(currentInput);
      let replyContent = `Voriq AI Engine: I have processed your request "${currentInput}". `;
      if (isIndic) {
        replyContent += `\n\n🇮🇳 [Indic Language Intelligence]: Romanised/Code-mixed Indic query detected. Responding with high regional fidelity and cultural accuracy.`;
      } else {
        replyContent += `\n\nYour task has been routed through self-hosted open-weight foundation infrastructure. All model execution logs and citations are verified.`;
      }

      const assistantMsg: Message = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: replyContent,
        language: isIndic ? 'Indic (Romanised)' : 'English',
        citations: [
          { document_name: 'Voriq_Indic_Architecture.pdf', snippet: 'Indic language routing uses dual script-detection heuristics...' }
        ]
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsGenerating(false);
    }, 1200);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background text-primaryText font-sans">
      {/* LEFT SIDEBAR: Navigation & Conversations */}
      <aside className="w-64 flex-shrink-0 glass-panel border-r border-surfaceBorder flex flex-col justify-between p-4">
        <div>
          {/* Logo & Brand Header */}
          <div className="flex items-center gap-3 mb-6 px-2">
            <div className="h-9 w-9 rounded-xl bg-accent flex items-center justify-center font-bold text-white shadow-lg shadow-accent/20">
              V
            </div>
            <div>
              <h1 className="font-bold text-base tracking-wide text-white">Voriq AI Studio</h1>
              <p className="text-xs text-secondaryText">Phase 1 & Phase 2 Multimodal OS</p>
            </div>
          </div>

          {/* New Conversation Button */}
          <button
            onClick={createNewConversation}
            className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-surface hover:bg-surfaceBorder border border-surfaceBorder text-sm font-medium transition-all duration-200 mb-6 shadow-sm"
          >
            <Plus className="w-4 h-4 text-accent" />
            <span>New Workspace Thread</span>
          </button>

          {/* Navigation Tabs */}
          <nav className="space-y-1 mb-6">
            <button
              onClick={() => setActiveTab('chat')}
              className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
                activeTab === 'chat' ? 'bg-accent/15 text-accent font-medium' : 'text-secondaryText hover:text-white hover:bg-surface/50'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              <span>AI Chat & RAG Studio</span>
            </button>
            <button
              onClick={() => setActiveTab('characters')}
              className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
                activeTab === 'characters' ? 'bg-accent/15 text-accent font-medium' : 'text-secondaryText hover:text-white hover:bg-surface/50'
              }`}
            >
              <UserCheck className="w-4 h-4" />
              <span>Character Consistency</span>
            </button>
            <button
              onClick={() => setActiveTab('media')}
              className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
                activeTab === 'media' ? 'bg-accent/15 text-accent font-medium' : 'text-secondaryText hover:text-white hover:bg-surface/50'
              }`}
            >
              <Video className="w-4 h-4" />
              <span>Image & Video Studio</span>
            </button>
            <button
              onClick={() => setActiveTab('models')}
              className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors ${
                activeTab === 'models' ? 'bg-accent/15 text-accent font-medium' : 'text-secondaryText hover:text-white hover:bg-surface/50'
              }`}
            >
              <Layers className="w-4 h-4" />
              <span>Model Fine-Tuning & Registry</span>
            </button>
          </nav>

          {/* Conversations Thread List */}
          {activeTab === 'chat' && (
            <div>
              <div className="text-xs font-semibold text-secondaryText uppercase tracking-wider px-2 mb-2">
                Recent Conversations
              </div>
              <div className="space-y-1 overflow-y-auto max-h-56 pr-1">
                {conversations.length === 0 ? (
                  <div className="text-xs text-secondaryText px-2 py-4 italic text-center">
                    No active threads. Start a conversation!
                  </div>
                ) : (
                  conversations.map((c) => (
                    <button
                      key={c.id}
                      onClick={() => setCurrentConvId(c.id)}
                      className={`w-full text-left text-xs px-3 py-2 rounded-lg truncate transition-colors ${
                        currentConvId === c.id ? 'bg-surface text-white font-medium border border-surfaceBorder' : 'text-secondaryText hover:text-white'
                      }`}
                    >
                      {c.title}
                    </button>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Account / Tenant Card */}
        <div className="pt-4 border-t border-surfaceBorder flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-full bg-accent/20 border border-accent/40 flex items-center justify-center text-xs font-bold text-accent">
              IN
            </div>
            <div>
              <div className="text-xs font-medium text-white">Bharat AI Org</div>
              <div className="text-[10px] text-secondaryText">Super Admin Tenant</div>
            </div>
          </div>
          <Settings className="w-4 h-4 text-secondaryText cursor-pointer hover:text-white" />
        </div>
      </aside>

      {/* MAIN WORKSPACE AREA */}
      <main className="flex-1 flex flex-col justify-between overflow-hidden relative">
        {/* Top Control Header */}
        <header className="h-14 border-b border-surfaceBorder glass-panel px-6 flex items-center justify-between z-10">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-accent" />
              <select
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value)}
                className="bg-surface border border-surfaceBorder text-xs text-white rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-accent"
              >
                <option value="vorik-indic-v1">Voriq Indic Foundation V1 (70B)</option>
                <option value="meta-llama-3.3-70b">Meta Llama 3.3 70B Instruct</option>
                <option value="mistral-7b-indic">Mistral 7B + Hinglish LoRA</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-accent" />
              <select
                value={languageOverride}
                onChange={(e) => setLanguageOverride(e.target.value)}
                className="bg-surface border border-surfaceBorder text-xs text-white rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-accent"
              >
                <option value="auto">Auto Language Detection</option>
                <option value="hindi">Hindi (Devanagari / Hinglish)</option>
                <option value="malayalam">Malayalam (Malayalam / Manglish)</option>
                <option value="tamil">Tamil (Tamil / Tanglish)</option>
                <option value="telugu">Telugu (Telugu / Tenglish)</option>
              </select>
            </div>
          </div>

          <div className="flex items-center gap-3 text-xs text-secondaryText">
            <span className="flex items-center gap-1.5 bg-surface border border-surfaceBorder px-2.5 py-1 rounded-full">
              <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
              GPU Cluster: Ready
            </span>
            <span>Est. Cost: <strong className="text-white">$0.0004</strong> / msg</span>
          </div>
        </header>

        {/* Dynamic Content View based on Active Tab */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {activeTab === 'chat' && (
            messages.length === 0 ? (
              /* Empty Workspace Clean State */
              <div className="h-full flex flex-col items-center justify-center text-center max-w-xl mx-auto my-auto space-y-6 py-12">
                <div className="h-16 w-16 rounded-2xl bg-accent/10 border border-accent/30 flex items-center justify-center text-accent">
                  <Sparkles className="w-8 h-8" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white mb-2">Voriq AI Multimodal Studio</h2>
                  <p className="text-sm text-secondaryText">
                    India-first language intelligence, document RAG, character visual production, and fine-tuning engine.
                  </p>
                </div>
                <div className="grid grid-cols-2 gap-3 w-full">
                  <button
                    onClick={() => setInputQuery("Enikku tomorrow client meeting undu. Prepare cheyyan help cheyyamo?")}
                    className="p-3 glass-panel rounded-xl text-left border border-surfaceBorder hover:border-accent/40 text-xs transition-colors"
                  >
                    <div className="font-semibold text-accent mb-1">🇲🇱 Manglish / Code-Mixed</div>
                    <div className="text-secondaryText line-clamp-2">"Enikku tomorrow client meeting undu..."</div>
                  </button>
                  <button
                    onClick={() => setInputQuery("Analyze market trends for Indian fintech in 2026.")}
                    className="p-3 glass-panel rounded-xl text-left border border-surfaceBorder hover:border-accent/40 text-xs transition-colors"
                  >
                    <div className="font-semibold text-accent mb-1">📊 Market Intelligence</div>
                    <div className="text-secondaryText line-clamp-2">"Analyze market trends for Indian fintech..."</div>
                  </button>
                </div>
              </div>
            ) : (
              /* Chat Messages View */
              <div className="space-y-4 max-w-3xl mx-auto">
                {messages.map((m) => (
                  <div
                    key={m.id}
                    className={`flex flex-col p-4 rounded-2xl border text-sm ${
                      m.role === 'user'
                        ? 'bg-surface/80 border-surfaceBorder ml-auto max-w-xl text-right text-white'
                        : 'glass-panel border-accent/20 mr-auto max-w-2xl text-left'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs text-secondaryText mb-1.5">
                      <span className="font-semibold text-accent">{m.role === 'user' ? 'You' : 'Voriq AI Engine'}</span>
                      {m.language && <span className="bg-surface px-2 py-0.5 rounded text-[10px]">{m.language}</span>}
                    </div>
                    <div className="whitespace-pre-wrap leading-relaxed">{m.content}</div>

                    {m.citations && m.citations.length > 0 && (
                      <div className="mt-3 pt-2 border-t border-surfaceBorder text-xs text-secondaryText">
                        <div className="font-semibold text-accent mb-1">Citations & RAG Sources:</div>
                        {m.citations.map((c, i) => (
                          <div key={i} className="bg-surface p-2 rounded border border-surfaceBorder text-[11px] mb-1">
                            📄 <strong className="text-white">{c.document_name}</strong>: "{c.snippet}"
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )
          )}

          {activeTab === 'characters' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <UserCheck className="w-5 h-5 text-accent" />
                Character Consistency Profile Manager
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="glass-panel p-5 rounded-2xl border border-surfaceBorder space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-white">Meera (Kerala Profile)</h3>
                    <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full border border-green-500/30">Active Lock</span>
                  </div>
                  <div className="text-xs text-secondaryText space-y-1">
                    <div><strong>Region:</strong> Kerala (Central Kerala Accent)</div>
                    <div><strong>Attire:</strong> Contemporary Handloom Saree</div>
                    <div><strong>Voice:</strong> Malayalam TTS Engine</div>
                    <div><strong>Consent Status:</strong> Synthetic Verified</div>
                  </div>
                </div>

                <div className="glass-panel p-5 rounded-2xl border border-surfaceBorder space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-white">Arjun (Telangana Profile)</h3>
                    <span className="text-xs bg-accent/20 text-accent px-2 py-0.5 rounded-full border border-accent/30">Ready</span>
                  </div>
                  <div className="text-xs text-secondaryText space-y-1">
                    <div><strong>Region:</strong> Telangana (Hyderabad Urban)</div>
                    <div><strong>Attire:</strong> Smart Casual Blazer</div>
                    <div><strong>Voice:</strong> Telugu TTS Engine</div>
                    <div><strong>Consent Status:</strong> Synthetic Verified</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'media' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <Video className="w-5 h-5 text-accent" />
                Self-Hosted Media Production Studio
              </h2>
              <div className="glass-panel p-6 rounded-2xl border border-surfaceBorder space-y-4">
                <div className="text-sm font-semibold text-white">Generate Culturally Grounded Visual Asset</div>
                <textarea
                  placeholder="Describe scene prompt with Indian regional context (e.g. Modern Kerala tech hub office during golden hour)..."
                  className="w-full h-24 bg-surface border border-surfaceBorder rounded-xl p-3 text-xs text-white focus:outline-none focus:border-accent"
                ></textarea>
                <div className="flex justify-end gap-3">
                  <button className="px-4 py-2 bg-surface hover:bg-surfaceBorder border border-surfaceBorder rounded-xl text-xs text-white flex items-center gap-2">
                    <ImageIcon className="w-4 h-4 text-accent" /> Generate Image
                  </button>
                  <button className="px-4 py-2 bg-accent hover:bg-accentHover text-white rounded-xl text-xs font-semibold flex items-center gap-2 shadow-lg shadow-accent/20">
                    <Video className="w-4 h-4" /> Storyboard Video Render
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'models' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <Layers className="w-5 h-5 text-accent" />
                Phase 2 Fine-Tuning & Model Registry
              </h2>
              <div className="glass-panel p-6 rounded-2xl border border-surfaceBorder space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-white text-sm">Voriq Indic Foundation V1</h3>
                    <p className="text-xs text-secondaryText">Base: Meta Llama 3.3 70B | Adapters: Indic-Romanised-LoRA</p>
                  </div>
                  <span className="text-xs bg-green-500/20 text-green-400 px-3 py-1 rounded-full border border-green-500/30">Production Stage</span>
                </div>
                <div className="grid grid-cols-3 gap-3 text-xs">
                  <div className="bg-surface p-3 rounded-xl border border-surfaceBorder">
                    <div className="text-secondaryText mb-1">Translation BLEU</div>
                    <div className="text-base font-bold text-accent">42.1 Score</div>
                  </div>
                  <div className="bg-surface p-3 rounded-xl border border-surfaceBorder">
                    <div className="text-secondaryText mb-1">Indic Script Accuracy</div>
                    <div className="text-base font-bold text-green-400">99.2%</div>
                  </div>
                  <div className="bg-surface p-3 rounded-xl border border-surfaceBorder">
                    <div className="text-secondaryText mb-1">Canary Allocation</div>
                    <div className="text-base font-bold text-white">10.0% Traffic</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Bottom Input Area */}
        {activeTab === 'chat' && (
          <footer className="p-4 border-t border-surfaceBorder glass-panel">
            <form onSubmit={handleSendMessage} className="max-w-3xl mx-auto flex items-center gap-2">
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder="Ask Voriq AI in English or Romanised Indic (e.g. Hinglish, Manglish)..."
                className="flex-1 bg-surface border border-surfaceBorder rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-accent transition-colors"
              />
              <button
                type="submit"
                disabled={isGenerating || !inputQuery.trim()}
                className="bg-accent hover:bg-accentHover disabled:opacity-50 text-white p-3 rounded-xl transition-colors shadow-lg shadow-accent/20 flex items-center justify-center"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </footer>
        )}
      </main>

      {/* RIGHT SIDEBAR: Agent Activity Panel */}
      <aside className="w-72 flex-shrink-0 glass-panel border-l border-surfaceBorder p-4 hidden lg:flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-accent uppercase tracking-wider mb-4 pb-2 border-b border-surfaceBorder">
            <Terminal className="w-4 h-4" />
            Agent Activity & Reasoning
          </div>

          <div className="space-y-3">
            {agentSteps.length === 0 ? (
              <div className="text-xs text-secondaryText italic text-center py-8">
                Agent trace logs will appear here during query execution.
              </div>
            ) : (
              agentSteps.map((step, idx) => (
                <div key={idx} className="bg-surface p-2.5 rounded-xl border border-surfaceBorder text-xs space-y-1">
                  <div className="text-accent font-semibold flex items-center gap-1">
                    <span className="h-1.5 w-1.5 rounded-full bg-accent animate-ping"></span>
                    {step.split(':')[0]}
                  </div>
                  <div className="text-secondaryText leading-normal">{step.split(':')[1]}</div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="bg-surface/60 p-3 rounded-xl border border-surfaceBorder text-[11px] text-secondaryText space-y-1">
          <div className="font-semibold text-white">Voriq Security Assurance</div>
          <div>✓ Tenant Isolation Enforced</div>
          <div>✓ Zero Unverified Claims</div>
        </div>
      </aside>
    </div>
  );
}
