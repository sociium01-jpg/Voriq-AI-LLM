from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

AgentStatus = Literal[
    'draft', 'testing', 'evaluating', 'staging', 
    'canary', 'production', 'suspended', 'deprecated', 'retired'
]

AgentType = Literal[
    'supervisor', 'planner', 'research', 'coding', 'data_analyst', 
    'document', 'indian_language', 'translation', 'image_director', 
    'video_director', 'voice', 'marketing', 'finance', 'healthcare', 
    'business_operations', 'customer_support', 'verification', 'safety'
]

RiskClassification = Literal['low', 'medium', 'high', 'critical']

class ToolDefinition(BaseModel):
    tool_id: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    provider: str
    authentication_required: bool = False
    required_permissions: List[str] = Field(default_factory=list)
    tenant_scope: str = "default"
    risk_classification: RiskClassification = "low"
    timeout_seconds: int = 30
    retry_policy: Dict[str, Any] = Field(default_factory=lambda: {"max_retries": 3, "backoff": 2.0})
    rate_limit: Optional[str] = "100/min"
    cost_estimate_usd: float = 0.0
    idempotency_supported: bool = True
    approval_required: bool = False
    audit_required: bool = True
    enabled: bool = True
    version: str = "1.0.0"
    category: str = "business_workflow"

class AgentRegistration(BaseModel):
    agent_id: str
    agent_name: str
    agent_version: str = "1.0.0"
    agent_type: AgentType
    base_model: str
    model_adapter: Optional[str] = None
    system_instructions: str
    allowed_tools: List[str] = Field(default_factory=list)
    denied_tools: List[str] = Field(default_factory=list)
    max_execution_steps: int = 25
    max_runtime_seconds: int = 300
    token_limit: int = 16384
    budget_limit_usd: Optional[float] = 2.0
    memory_policy: Dict[str, Any] = Field(default_factory=lambda: {"ttl_days": 30, "tenant_isolated": True})
    approval_policy: Dict[str, Any] = Field(default_factory=lambda: {"require_human_on_high_risk": True})
    safety_policy: Dict[str, Any] = Field(default_factory=lambda: {"pii_redaction": True})
    supported_languages: List[str] = Field(default_factory=lambda: ["en", "hi", "ml", "ta", "te"])
    supported_domains: List[str] = Field(default_factory=lambda: ["general", "enterprise"])
    evaluation_results: Dict[str, Any] = Field(default_factory=dict)
    status: AgentStatus = "draft"
    created_by: str = "system"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PlanStep(BaseModel):
    step_id: str
    objective: str
    agent_id: str
    tool_name: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)
    expected_output: str
    retry_limit: int = 3
    verification_method: str = "deterministic"
    approval_required: bool = False
    status: Literal['pending', 'in_progress', 'completed', 'failed', 'awaiting_approval'] = 'pending'

class AgentPlan(BaseModel):
    goal: str
    assumptions: List[str] = Field(default_factory=list)
    steps: List[PlanStep] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    estimated_cost: Optional[float] = None
    estimated_runtime_seconds: Optional[int] = None
    approval_required: bool = False
    success_criteria: List[str] = Field(default_factory=list)

class AgentTask(BaseModel):
    task_id: str
    parent_task_id: Optional[str] = None
    requesting_agent_id: str
    target_agent_id: str
    objective: str
    context: Dict[str, Any] = Field(default_factory=dict)
    allowed_tools: List[str] = Field(default_factory=list)
    budget: Optional[float] = None
    deadline: Optional[str] = None
    success_criteria: List[str] = Field(default_factory=list)

class AgentResponse(BaseModel):
    task_id: str
    status: Literal['completed', 'failed', 'pending_approval']
    result: Any
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    unresolved_issues: List[str] = Field(default_factory=list)
    cost_usd: float = 0.0
    runtime_seconds: float = 0.0
    verification_status: Literal['passed', 'failed', 'skipped'] = 'passed'

class AgentTrace(BaseModel):
    trace_id: str
    user_id: str
    tenant_id: str
    routing_decision: Dict[str, Any]
    agent_selected: str
    model_selected: str
    plan: Optional[AgentPlan] = None
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    agent_handoffs: List[Dict[str, Any]] = Field(default_factory=list)
    approvals: List[Dict[str, Any]] = Field(default_factory=list)
    retries: int = 0
    errors: List[str] = Field(default_factory=list)
    verification_status: str = "passed"
    final_response: str
    token_usage: Dict[str, int] = Field(default_factory=dict)
    cost_usd: float = 0.0
    runtime_ms: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
