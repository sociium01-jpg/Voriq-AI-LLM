# Voriq AI Studio — Multilingual & Multimodal AI Platform

Voriq AI is an India-first, multimodal AI operating system designed for multilingual communication, knowledge work, business automation, visual media generation, and proprietary model development.

## Key Capabilities

- 🇮🇳 **Indian-Language Intelligence**: Native script support for 12+ Indic languages (Hindi, Malayalam, Tamil, Telugu, Kannada, Marathi, Bengali, Gujarati, Punjabi, Urdu, Odia, Assamese) + Romanised code-mixed variants (Hinglish, Manglish, Tanglish, Tenglish, etc.).
- 🤖 **LangGraph Multi-Agent Workflows**: Stateful multi-agent orchestration across 18 specialized agents with human-in-the-loop approvals.
- 📄 **Document Intelligence & RAG**: Multi-format document parser, pgvector hybrid search, and exact citation tracking.
- 🎨 **Self-Hosted Image Generation**: Context-aware prompt engine (Indian attire, regional architecture, lighting, professions) with reusable Character Consistency profiles.
- 🎬 **Self-Hosted Video Generation**: Asynchronous scene-by-scene video production pipeline (Brief → Script → Shot List → Keyframes → Motion Render).
- 🎙️ **Voice & Speech Framework**: STT with regional accent handling, TTS emotion controls, and automated subtitle generation.
- ⚙️ **Phase 2 Fine-Tuning Infrastructure**: SFT, LoRA/QLoRA training orchestrator, dataset governance (PII scanning, copyright/consent review), Model Registry, automated/human evaluation suites, and Canary/A/B deployment.

## Repository Structure

```text
bharat-ai/
├── apps/                 # Web Studio, Admin Dashboard, Documentation
├── services/             # FastAPI Services (Gateway, Orchestrator, Indic Engine, Router, etc.)
├── workers/              # Asynchronous Workers (LLM, Media GPU, Fine-Tuning)
├── packages/             # Shared Python & JS Packages (Schemas, Database, Model Clients)
├── datasets/             # Manifests, Schemas & Data Validators
├── models/               # Model Registry & Adapters
├── infrastructure/       # Docker, Kubernetes, Terraform & GPU Configs
└── tests/                # Unit, Integration, Language & Evaluation Tests
```

## Quickstart

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ & pnpm / npm
- Python 3.11+
- PostgreSQL with `pgvector` extension
- Redis

### Environment Setup
1. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```
2. Start infrastructure & services:
   ```bash
   docker-compose up -d
   ```
3. Run test suite:
   ```bash
   make test
   ```
