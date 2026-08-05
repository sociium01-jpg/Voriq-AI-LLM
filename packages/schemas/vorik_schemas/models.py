from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_OWNER = "org_owner"
    ORG_ADMIN = "org_admin"
    AI_ADMIN = "ai_admin"
    DATASET_REVIEWER = "dataset_reviewer"
    MODEL_ENGINEER = "model_engineer"
    SAFETY_REVIEWER = "safety_reviewer"
    BILLING_ADMIN = "billing_admin"
    TEAM_MANAGER = "team_manager"
    MEMBER = "member"
    VIEWER = "viewer"

class LanguageEnum(str, Enum):
    HINDI = "hindi"
    MALAYALAM = "malayalam"
    TAMIL = "tamil"
    TELUGU = "telugu"
    KANNADA = "kannada"
    MARATHI = "marathi"
    BENGALI = "bengali"
    GUJARATI = "gujarati"
    PUNJABI = "punjabi"
    URDU = "urdu"
    ODIA = "odia"
    ASSAMESE = "assamese"
    ENGLISH = "english"

class ScriptEnum(str, Enum):
    DEVANAGARI = "devanagari"
    MALAYALAM = "malayalam"
    TAMIL = "tamil"
    TELUGU = "telugu"
    KANNADA = "kannada"
    BENGALI = "bengali"
    GUJARATI = "gujarati"
    GURMUKHI = "gurmukhi"
    ARABIC = "arabic"
    LATIN = "latin"

# User & Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    preferred_language: LanguageEnum = LanguageEnum.ENGLISH

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: UserRole
    organisation_id: Optional[str] = None
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Language & Script Schemas
class LanguageDetectionResult(BaseModel):
    detected_language: LanguageEnum
    detected_script: ScriptEnum
    is_romanised: bool = False
    is_code_mixed: bool = False
    confidence_score: float = Field(ge=0.0, le=1.0)
    secondary_languages: List[str] = []

class TranslationRequest(BaseModel):
    text: str
    source_language: Optional[LanguageEnum] = None
    target_language: LanguageEnum
    target_script: Optional[ScriptEnum] = None
    preserve_terms: List[str] = []
    formality: str = "conversational"  # formal, conversational, simple

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: LanguageEnum
    target_language: LanguageEnum
    detected_script: ScriptEnum

# Model Gateway & Router
class ModelRoute(BaseModel):
    task_type: str
    language: str
    script: str
    complexity: str
    domain: Optional[str] = None
    base_model: str
    adapters: List[str] = []
    tools: List[str] = []
    temperature: float = 0.7
    max_tokens: int = 2048
    fallback_model: str = "fallback-default"
    sensitivity_level: str = "standard"

# Chat & Message
class ChatMessageCreate(BaseModel):
    conversation_id: Optional[str] = None
    content: str
    language_override: Optional[LanguageEnum] = None
    model_override: Optional[str] = None
    files: List[str] = []

class Citation(BaseModel):
    document_id: str
    document_name: str
    page_number: Optional[int] = None
    snippet: str
    score: float

class ChatMessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str  # user, assistant, system, tool
    content: str
    language: Optional[str] = None
    script: Optional[str] = None
    citations: List[Citation] = []
    model_used: Optional[str] = None
    token_count: int = 0
    created_at: datetime

# Document & RAG
class RAGQueryRequest(BaseModel):
    query: str
    workspace_id: str
    top_k: int = 5
    language_filter: Optional[LanguageEnum] = None

class RAGQueryResult(BaseModel):
    query: str
    retrieved_chunks: List[Dict[str, Any]]
    citations: List[Citation]

# Image & Video Subsystem
class CharacterProfile(BaseModel):
    character_id: str
    name: str
    region: str
    age_range: str
    skin_tone: str
    face_description: str
    hair: str
    wardrobe: str
    voice_language: str
    accent: str
    personality: str
    consent_status: str = "synthetic"

class ImageGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: str = ""
    aspect_ratio: str = "1:1"
    width: int = 1024
    height: int = 1024
    character_id: Optional[str] = None
    region_context: Optional[str] = "India General"
    num_outputs: int = 1

class VideoGenerationRequest(BaseModel):
    script: str
    character_ids: List[str] = []
    resolution: str = "1080p"
    duration_seconds: int = 5
    aspect_ratio: str = "16:9"

class MediaJobResponse(BaseModel):
    job_id: str
    status: str  # queued, processing, completed, failed
    progress_percentage: float = 0.0
    output_urls: List[str] = []
    error_message: Optional[str] = None
    created_at: datetime

# Phase 2 Fine-Tuning & Model Registry
class DatasetRecordCreate(BaseModel):
    name: str
    description: str
    language: LanguageEnum
    script: ScriptEnum
    domain: str
    task_type: str
    license_name: str
    commercial_use_approved: bool

class DatasetRecordResponse(BaseModel):
    dataset_id: str
    name: str
    version: str
    language: str
    quality_score: Optional[float] = None
    pii_scan_status: str
    copyright_review_status: str
    approved_for_training: bool
    row_count: int

class TrainingConfig(BaseModel):
    training_type: str  # sft, lora, qlora
    base_model: str
    dataset_id: str
    output_name: str
    learning_rate: float = 2e-4
    epochs: int = 3
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    max_sequence_length: int = 2048
    lora_rank: Optional[int] = 16
    lora_alpha: Optional[int] = 32

class ModelRecordResponse(BaseModel):
    model_id: str
    name: str
    base_model: str
    version: str
    supported_languages: List[str]
    status: str  # draft, training, staging, production
    deployment_stage: str
