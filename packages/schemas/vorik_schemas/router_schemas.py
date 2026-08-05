from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

RoutingMode = Literal[
    'auto', 'fast', 'reasoning', 'research', 'coding', 
    'creative', 'vision', 'image', 'video', 'voice', 'agent', 'private'
]

PrivacyLevel = Literal[
    'public_api', 'private_cloud', 'dedicated_tenant', 'on_premise', 'air_gapped'
]

class ModelRegistration(BaseModel):
    model_id: str
    provider: str
    model_family: str
    version: str = "1.0.0"
    capabilities: List[str] = Field(default_factory=lambda: ["text", "chat"])
    languages: List[str] = Field(default_factory=lambda: ["en", "hi", "ml", "ta", "te"])
    modalities: List[str] = Field(default_factory=lambda: ["text"])
    context_length: int = 128000
    tool_use_support: bool = True
    structured_output_support: bool = True
    cost_per_1k_input_tokens: float = 0.001
    cost_per_1k_output_tokens: float = 0.002
    latency_p95_ms: float = 450.0
    availability_sla: float = 99.9
    data_retention_policy: str = "zero_retention"
    deployment_region: str = "asia-south1"
    safety_rating: str = "high"
    evaluation_score: float = 92.5
    licence: str = "Apache-2.0"
    commercial_use_allowed: bool = True
    privacy_level: PrivacyLevel = "public_api"
    active_status: bool = True

class RoutingRequest(BaseModel):
    user_id: str
    tenant_id: str
    request_text: str
    mode: RoutingMode = "auto"
    preferred_language: Optional[str] = None
    has_attachments: bool = False
    requires_realtime: bool = False
    privacy_requirement: PrivacyLevel = "public_api"
    max_budget_usd: Optional[float] = 1.0
    max_latency_ms: Optional[int] = 5000

class RoutingDecision(BaseModel):
    selected_model_id: str
    selected_provider: str
    selected_adapter: Optional[str] = None
    selected_agent_id: str
    required_tools: List[str] = Field(default_factory=list)
    required_retrieval_sources: List[str] = Field(default_factory=list)
    fallback_model_id: str
    timeout_seconds: int = 30
    estimated_cost_usd: float = 0.0005
    routing_reason: str
    confidence_score: float = 0.95
    privacy_level_applied: PrivacyLevel = "public_api"
