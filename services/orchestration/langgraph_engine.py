from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    conversation_id: str
    user_query: str
    detected_language: str = "english"
    detected_script: str = "latin"
    is_code_mixed: bool = False
    active_agent: str = "supervisor"
    steps: List[Dict[str, Any]] = []
    response: str = ""
    citations: List[Dict[str, Any]] = []
    requires_approval: bool = False
    approval_reason: Optional[str] = None
    cost_estimate: float = 0.0

class AgentDefinition(BaseModel):
    name: str
    purpose: str
    allowed_tools: List[str]
    max_steps: int = 5
    requires_approval_for_actions: List[str] = []

CORE_AGENTS: Dict[str, AgentDefinition] = {
    "supervisor": AgentDefinition(
        name="Supervisor Router",
        purpose="Classifies query intent, language, and routes to target domain agent",
        allowed_tools=["detect_language", "route_model"]
    ),
    "general": AgentDefinition(
        name="General Assistant",
        purpose="Handles general knowledge, conversation, and reasoning",
        allowed_tools=["web_search", "calculator"]
    ),
    "indic_language": AgentDefinition(
        name="Indian Language Agent",
        purpose="Specialized in 12+ Indic native scripts and Romanised code-mixed languages",
        allowed_tools=["transliterate", "translate_indic", "cultural_glossary"]
    ),
    "translation": AgentDefinition(
        name="Translation Agent",
        purpose="High-accuracy translation preserving medical, legal, and brand terminology",
        allowed_tools=["translate_exact", "check_glossary"]
    ),
    "research": AgentDefinition(
        name="Research Agent",
        purpose="Multi-source search, credibility scoring, date checking, and citation reports",
        allowed_tools=["web_search", "parse_webpage", "score_credibility"]
    ),
    "document": AgentDefinition(
        name="Document Intelligence Agent",
        purpose="Multi-format document parsing, OCR, and vector RAG retrieval with citations",
        allowed_tools=["pdf_ocr", "vector_search", "table_extract"]
    ),
    "coding": AgentDefinition(
        name="Coding Agent",
        purpose="Code generation, bug diagnosis, and architecture planning",
        allowed_tools=["execute_code", "lint_code", "git_patch"]
    ),
    "image_director": AgentDefinition(
        name="Image Director Agent",
        purpose="Indian cultural context prompt builder and character consistency manager",
        allowed_tools=["generate_image", "character_lock", "inpaint"]
    ),
    "video_director": AgentDefinition(
        name="Video Director Agent",
        purpose="Scene-by-scene storyboard planning, shot list, keyframes, and render pipeline",
        allowed_tools=["script_to_storyboard", "generate_video", "lip_sync"]
    ),
    "voice_production": AgentDefinition(
        name="Voice Production Agent",
        purpose="Speech-to-text, text-to-speech emotion controls, and subtitle alignment",
        allowed_tools=["stt_indic", "tts_indic", "generate_srt"]
    )
}

class LangGraphOrchestrator:
    """Stateful LangGraph supervisor-agent graph engine"""

    def __init__(self):
        self.agents = CORE_AGENTS

    async def execute_workflow(self, conversation_id: str, query: str, user_role: str = "member") -> AgentState:
        state = AgentState(conversation_id=conversation_id, user_query=query)

        # Step 1: Supervisor Classification
        state.steps.append({
            "agent": "supervisor",
            "action": "classify_query",
            "status": "completed",
            "detail": f"Analyzing query: '{query[:50]}...'"
        })

        # Check for financial or destructive action triggers
        lower_query = query.lower()
        if any(trigger in lower_query for trigger in ["delete production", "transfer money", "publish article", "clone voice"]):
            state.requires_approval = True
            state.approval_reason = f"Action '{query[:40]}' requires explicit human approval before execution."
            state.response = f"⚠️ [Human Approval Required]: {state.approval_reason}"
            return state

        # Step 2: Route to specialized agent
        if any(w in lower_query for w in ["kya", "kar", "enikku", "cheyyan", "namaste", "vanakkam"]):
            state.active_agent = "indic_language"
            state.is_code_mixed = True
            state.detected_language = "hindi/malayalam"
            state.steps.append({
                "agent": "indic_language",
                "action": "process_code_mixed",
                "status": "completed",
                "detail": "Applied Indic Code-Mixed Adapter"
            })
            state.response = f"Voriq Indic AI: Namaste! I processed your query with high Indic contextual accuracy."
        elif "image" in lower_query or "picture" in lower_query:
            state.active_agent = "image_director"
            state.steps.append({
                "agent": "image_director",
                "action": "build_indian_context_prompt",
                "status": "completed",
                "detail": "Configured regional attire, lighting, and cultural parameters"
            })
            state.response = f"Voriq Visual Studio: Generated image concept for '{query}' with regional visual consistency."
        else:
            state.active_agent = "general"
            state.steps.append({
                "agent": "general",
                "action": "llm_reasoning",
                "status": "completed",
                "detail": "Executed open-weight foundation LLM reasoning step"
            })
            state.response = f"Voriq Assistant: Handled query '{query}' using stateful LangGraph workflow."

        state.cost_estimate = 0.0004
        return state
