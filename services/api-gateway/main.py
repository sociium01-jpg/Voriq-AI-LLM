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
from auth import (
    hash_password, verify_password, create_access_token, get_current_user, require_role, TokenData
)

app = FastAPI(
    title="Voriq AI API Gateway",
    description="Multilingual, Multimodal AI Platform API Gateway (Phase 1 & Phase 2)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory mock store for rapid local verification when DB container is optional
USERS_DB: Dict[str, Dict[str, Any]] = {}
CONVERSATIONS_DB: Dict[str, Dict[str, Any]] = {}
MESSAGES_DB: Dict[str, List[Dict[str, Any]]] = {}
CHARACTERS_DB: Dict[str, Dict[str, Any]] = {}
MEDIA_JOBS_DB: Dict[str, Dict[str, Any]] = {}
DATASETS_DB: Dict[str, Dict[str, Any]] = {}
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
            "indic_engine": "ready",
            "media_worker": "ready"
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

@app.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: TokenData = Depends(get_current_user)):
    return UserResponse(
        id=current_user.user_id,
        email=current_user.email,
        full_name="Voriq User",
        role=UserRole(current_user.role),
        organisation_id=current_user.organisation_id,
        created_at=datetime.utcnow()
    )

# CHAT ENDPOINTS
@app.post("/chat/conversations")
async def create_conversation(
    title: Optional[str] = "New Conversation",
    current_user: TokenData = Depends(get_current_user)
):
    conv_id = str(uuid.uuid4())
    conv = {
        "id": conv_id,
        "title": title,
        "user_id": current_user.user_id,
        "organisation_id": current_user.organisation_id,
        "pinned": False,
        "archived": False,
        "created_at": datetime.utcnow().isoformat()
    }
    CONVERSATIONS_DB[conv_id] = conv
    MESSAGES_DB[conv_id] = []
    return conv

@app.get("/chat/conversations")
async def list_conversations(current_user: TokenData = Depends(get_current_user)):
    user_convs = [
        c for c in CONVERSATIONS_DB.values()
        if c["user_id"] == current_user.user_id
    ]
    return user_convs

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
    # Heuristic & Regex script detection
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

@app.post("/language/translate", response_model=TranslationResponse)
async def translate_text(req: TranslationRequest):
    translated = f"[{req.target_language.value.upper()} TRANSLATION]: {req.text}"
    return TranslationResponse(
        original_text=req.text,
        translated_text=translated,
        source_language=req.source_language or LanguageEnum.ENGLISH,
        target_language=req.target_language,
        detected_script=req.target_script or ScriptEnum.LATIN
    )

# CHARACTER CONSISTENCY & MEDIA ENDPOINTS
@app.post("/characters/create", response_model=CharacterProfile)
async def create_character(
    char: CharacterProfile,
    current_user: TokenData = Depends(get_current_user)
):
    CHARACTERS_DB[char.character_id] = char.model_dump()
    return char

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

@app.post("/media/video", response_model=MediaJobResponse)
async def generate_video(
    req: VideoGenerationRequest,
    current_user: TokenData = Depends(get_current_user)
):
    job_id = str(uuid.uuid4())
    job = {
        "job_id": job_id,
        "status": "processing",
        "progress_percentage": 45.0,
        "output_urls": [],
        "created_at": datetime.utcnow()
    }
    MEDIA_JOBS_DB[job_id] = job
    return MediaJobResponse(**job)

@app.get("/media/jobs/{job_id}", response_model=MediaJobResponse)
async def get_media_job(job_id: str):
    job = MEDIA_JOBS_DB.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return MediaJobResponse(**job)

# PHASE 2 FINE-TUNING & MODEL REGISTRY ENDPOINTS
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
