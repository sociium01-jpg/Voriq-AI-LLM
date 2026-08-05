import os
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr

from vorik_schemas.models import (
    UserRole, LanguageEnum, ScriptEnum, UserCreate, UserResponse, TokenResponse,
    LanguageDetectionResult, TranslationRequest, TranslationResponse,
    ChatMessageCreate, ChatMessageResponse, Citation, RAGQueryRequest,
    CharacterProfile, ImageGenerationRequest, VideoGenerationRequest, MediaJobResponse,
    DatasetRecordCreate, DatasetRecordResponse, TrainingConfig, ModelRecordResponse
)
from vorik_schemas.agent_schemas import (
    AgentRegistration, ToolDefinition, AgentTask, AgentResponse, AgentTrace
)
from vorik_schemas.router_schemas import (
    RoutingRequest, RoutingDecision, RoutingMode, PrivacyLevel
)
from auth import (
    hash_password, verify_password, create_access_token, get_current_user, require_role, TokenData
)

from services.model_router.universal_router import universal_router
from services.orchestration.tool_registry import tool_registry
from services.orchestration.tool_executor import ToolExecutor
from services.orchestration.langgraph_runtime import langgraph_agent_runtime

app = FastAPI(
    title="Voriq AI Universal Intelligence Gateway",
    description="Universal Multi-Model & Agentic LLM Platform API Gateway",
    version="2.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tool_executor = ToolExecutor(tool_registry)

# In-memory mock store
USERS_DB: Dict[str, Dict[str, Any]] = {}
CONVERSATIONS_DB: Dict[str, Dict[str, Any]] = {}
MESSAGES_DB: Dict[str, List[Dict[str, Any]]] = {}
CHARACTERS_DB: Dict[str, Dict[str, Any]] = {}
MEDIA_JOBS_DB: Dict[str, Dict[str, Any]] = {}
DATASETS_DB: Dict[str, Dict[str, Any]] = {}
APPROVAL_QUEUE_DB: Dict[str, Dict[str, Any]] = {}
MODELS_DB: Dict[str, Dict[str, Any]] = {
    "vorik-indic-v1": {
        "model_id": "vorik-indic-v1",
        "name": "Voriq Indic Foundation V1",
        "base_model": "meta-llama/Llama-3.3-70B-Instruct",
        "version": "1.0.0",
        "supported_languages": ["hindi", "malayalam", "tamil", "telugu", "english"],
        "status": "production",
        "deployment_stage": "production",
        "created_by": "system",
    }
}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ApprovalReviewRequest(BaseModel):
    ticket_id: str
    action: str  # 'approve' or 'reject'
    notes: Optional[str] = None

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "api-gateway",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": "online",
            "redis": "online",
            "llm_router": "ready",
            "universal_router": "ready",
            "agent_runtime": "ready",
            "tool_executor": "ready"
        }
    }

# AUTH ENDPOINTS
@app.post("/auth/signup", response_model=TokenResponse)
async def signup(user_in: UserCreate):
    if user_in.email in USERS_DB:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    user_id = str(uuid.uuid4())
    org_id = str(uuid.uuid4())
    user_record = {
        "id": user_id,
        "email": user_in.email,
        "hashed_password": hash_password(user_in.password),
        "full_name": user_in.full_name,
        "role": UserRole.ORG_OWNER,
        "organisation_id": org_id,
        "created_at": datetime.utcnow()
    }
    USERS_DB[user_in.email] = user_record

    token = create_access_token({
        "sub": user_id,
        "email": user_in.email,
        "role": UserRole.ORG_OWNER.value,
        "organisation_id": org_id
    })

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            email=user_in.email,
            full_name=user_in.full_name,
            role=UserRole.ORG_OWNER,
            organisation_id=org_id,
            created_at=user_record["created_at"]
        )
    )

@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    user = USERS_DB.get(credentials.email)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token = create_access_token({
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"].value if isinstance(user["role"], UserRole) else user["role"],
        "organisation_id": user["organisation_id"]
    })

    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            organisation_id=user["organisation_id"],
            created_at=user["created_at"]
        )
    )

# UNIVERSAL ROUTER ENDPOINTS
@app.get("/router/modes")
async def list_routing_modes():
    return {
        "modes": ["auto", "fast", "reasoning", "research", "coding", "creative", "vision", "image", "video", "voice", "agent", "private"],
        "default": "auto"
    }

@app.post("/router/dispatch", response_model=RoutingDecision)
async def dispatch_request(req: RoutingRequest):
    return universal_router.route_request(req)

# AGENT & TOOL REGISTRY ENDPOINTS
@app.get("/agents/registry")
async def list_agents():
    return [
        {"agent_id": "supervisor", "name": "Supervisor Router Agent", "status": "production", "agent_type": "supervisor"},
        {"agent_id": "planner", "name": "Multi-Step Planner Agent", "status": "production", "agent_type": "planner"},
        {"agent_id": "research", "name": "Multi-Source Research Agent", "status": "production", "agent_type": "research"},
        {"agent_id": "coding", "name": "Polyglot Coding & Debug Agent", "status": "production", "agent_type": "coding"},
        {"agent_id": "indian_language", "name": "Indic Script & Code-Mixed Agent", "status": "production", "agent_type": "indian_language"},
        {"agent_id": "verification", "name": "Evidence Verification Agent", "status": "production", "agent_type": "verification"},
    ]

@app.get("/tools/registry")
async def list_tools():
    return tool_registry.list_tools()

@app.post("/tools/execute")
async def execute_tool(
    tool_name: str,
    tool_inputs: Dict[str, Any],
    current_user: TokenData = Depends(get_current_user)
):
    res = await tool_executor.execute_tool_call(
        tool_name=tool_name,
        tool_inputs=tool_inputs,
        user_id=current_user.user_id,
        tenant_id=current_user.organisation_id or "default_tenant"
    )
    if res.get("status") == "awaiting_approval":
        ticket_id = res["ticket_id"]
        APPROVAL_QUEUE_DB[ticket_id] = {
            "ticket_id": ticket_id,
            "user_id": current_user.user_id,
            "tenant_id": current_user.organisation_id or "default_tenant",
            "tool_name": tool_name,
            "tool_inputs": tool_inputs,
            "risk_level": "high",
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
    return res

# HUMAN APPROVAL QUEUE ENDPOINTS
@app.get("/approval/queue")
async def list_approval_queue(current_user: TokenData = Depends(get_current_user)):
    return list(APPROVAL_QUEUE_DB.values())

@app.post("/approval/review")
async def review_approval_ticket(
    req: ApprovalReviewRequest,
    current_user: TokenData = Depends(get_current_user)
):
    ticket = APPROVAL_QUEUE_DB.get(req.ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket["status"] = "approved" if req.action == "approve" else "rejected"
    ticket["reviewed_by"] = current_user.user_id
    ticket["review_notes"] = req.notes or ""
    return {"status": ticket["status"], "ticket_id": req.ticket_id}

# AGENT RUNTIME EXECUTION
@app.post("/agent/execute", response_model=AgentResponse)
async def execute_agent_task(
    task: AgentTask,
    current_user: TokenData = Depends(get_current_user)
):
    return await langgraph_agent_runtime.execute_task(task)

# MEDIA & CHARACTER ENDPOINTS
@app.post("/media/image", response_model=MediaJobResponse)
async def generate_image(
    req: ImageGenerationRequest,
    current_user: TokenData = Depends(get_current_user)
):
    job_id = str(uuid.uuid4())
    job = {
        "job_id": job_id,
        "status": "completed",
        "progress_percentage": 100.0,
        "output_urls": [f"https://vorik.ai/generated/images/{job_id}.png"],
        "created_at": datetime.utcnow()
    }
    MEDIA_JOBS_DB[job_id] = job
    return MediaJobResponse(**job)

# DATASET & FINE-TUNING ENDPOINTS
@app.post("/datasets/upload", response_model=DatasetRecordResponse)
async def upload_dataset(
    req: DatasetRecordCreate,
    current_user: TokenData = Depends(get_current_user)
):
    dataset_id = f"ds-{uuid.uuid4().hex[:8]}"
    record = {
        "dataset_id": dataset_id,
        "name": req.name,
        "version": "1.0.0",
        "language": req.language.value,
        "quality_score": 0.96,
        "pii_scan_status": "passed",
        "copyright_review_status": "approved",
        "approved_for_training": True,
        "row_count": 15000
    }
    DATASETS_DB[dataset_id] = record
    return DatasetRecordResponse(**record)

@app.post("/training/launch")
async def launch_training(
    cfg: TrainingConfig,
    current_user: TokenData = Depends(get_current_user)
):
    job_id = f"train-{uuid.uuid4().hex[:8]}"
    return {
        "job_id": job_id,
        "status": "training",
        "training_type": cfg.training_type,
        "base_model": cfg.base_model,
        "dataset_id": cfg.dataset_id,
        "message": f"Training job {job_id} launched successfully on GPU worker."
    }

# CHAT ENDPOINTS
@app.post("/chat/completions/stream")
async def stream_chat(
    msg: ChatMessageCreate,
    current_user: TokenData = Depends(get_current_user)
):
    conv_id = msg.conversation_id or str(uuid.uuid4())
    if conv_id not in CONVERSATIONS_DB:
        CONVERSATIONS_DB[conv_id] = {
            "id": conv_id,
            "title": msg.content[:30] + "...",
            "user_id": current_user.user_id,
            "organisation_id": current_user.organisation_id,
            "created_at": datetime.utcnow().isoformat()
        }
        MESSAGES_DB[conv_id] = []

    user_msg = {
        "id": str(uuid.uuid4()),
        "conversation_id": conv_id,
        "role": "user",
        "content": msg.content,
        "created_at": datetime.utcnow().isoformat()
    }
    MESSAGES_DB[conv_id].append(user_msg)

    async def generate_response():
        assistant_text = f"Voriq AI Agent: Received query '{msg.content}'. Processing with Indic Multilingual Engine..."
        for word in assistant_text.split(" "):
            yield f"data: {word} \n\n"
        yield "data: [DONE]\n\n"

        assistant_msg = {
            "id": str(uuid.uuid4()),
            "conversation_id": conv_id,
            "role": "assistant",
            "content": assistant_text,
            "created_at": datetime.utcnow().isoformat()
        }
        MESSAGES_DB[conv_id].append(assistant_msg)

    return StreamingResponse(generate_response(), media_type="text/event-stream")

# INDIC LANGUAGE ENGINE ENDPOINTS
@app.post("/language/detect", response_model=LanguageDetectionResult)
async def detect_language(text: str):
    has_devanagari = any('\u0900' <= char <= '\u097F' for char in text)
    has_malayalam = any('\u0D00' <= char <= '\u0D7F' for char in text)
    has_tamil = any('\u0B80' <= char <= '\u0BFF' for char in text)
    has_telugu = any('\u0C00' <= char <= '\u0C7F' for char in text)

    is_romanised = False
    is_code_mixed = False

    lower_text = text.lower()
    if not (has_devanagari or has_malayalam or has_tamil or has_telugu):
        if any(w in lower_text for w in ["kya", "kar", "rha", "hai", "bhai", "namaste", "chahiye"]):
            return LanguageDetectionResult(
                detected_language=LanguageEnum.HINDI,
                detected_script=ScriptEnum.LATIN,
                is_romanised=True,
                is_code_mixed=True,
                confidence_score=0.92,
                secondary_languages=["english"]
            )
        elif any(w in lower_text for w in ["enikku", "cheyyan", "undu", "nalla", "poya"]):
            return LanguageDetectionResult(
                detected_language=LanguageEnum.MALAYALAM,
                detected_script=ScriptEnum.LATIN,
                is_romanised=True,
                is_code_mixed=True,
                confidence_score=0.94,
                secondary_languages=["english"]
            )

    lang = LanguageEnum.ENGLISH
    script = ScriptEnum.LATIN
    if has_devanagari:
        lang, script = LanguageEnum.HINDI, ScriptEnum.DEVANAGARI
    elif has_malayalam:
        lang, script = LanguageEnum.MALAYALAM, ScriptEnum.MALAYALAM
    elif has_tamil:
        lang, script = LanguageEnum.TAMIL, ScriptEnum.TAMIL
    elif has_telugu:
        lang, script = LanguageEnum.TELUGU, ScriptEnum.TELUGU

    return LanguageDetectionResult(
        detected_language=lang,
        detected_script=script,
        is_romanised=is_romanised,
        is_code_mixed=is_code_mixed,
        confidence_score=0.95
    )

@app.get("/models/registry", response_model=List[ModelRecordResponse])
async def list_models():
    return [ModelRecordResponse(**m) for m in MODELS_DB.values()]

@app.get("/admin/metrics")
async def get_admin_metrics(current_user: TokenData = Depends(require_role(["super_admin", "org_owner", "ai_admin"]))):
    return {
        "active_users": len(USERS_DB),
        "total_conversations": len(CONVERSATIONS_DB),
        "gpu_workers": [
            {"id": "gpu-01", "name": "NVIDIA H100", "utilization": "42%", "status": "active"},
            {"id": "gpu-02", "name": "NVIDIA A100", "utilization": "78%", "status": "active"}
        ],
        "system_status": "operational"
    }
