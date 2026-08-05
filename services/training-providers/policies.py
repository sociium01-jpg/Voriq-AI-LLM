from typing import List, Optional
from pydantic import BaseModel, Field
from vorik_schemas.provider_schemas import ProviderType, TrainingJobRequest

class ProviderPolicy(BaseModel):
    policy_id: str
    organisation_id: Optional[str] = None
    workspace_id: Optional[str] = None
    allowed_providers: List[ProviderType] = Field(
        default_factory=lambda: [
            ProviderType.VERTEX_AI, ProviderType.GKE_GPU, ProviderType.RUNPOD,
            ProviderType.ON_PREM_GPU, ProviderType.MOCK_LOCAL
        ]
    )
    blocked_providers: List[ProviderType] = Field(default_factory=list)
    max_budget_usd: float = 500.0
    max_gpus_per_job: int = 16
    spot_allowed: bool = True
    required_data_residency: Optional[str] = None  # e.g., "in" for India

class PolicyEngine:
    """Enforces Platform, Organisation, Workspace, and Job level provider security rules"""

    def validate_request(self, request: TrainingJobRequest, policy: ProviderPolicy) -> bool:
        # Check budget limits
        if request.budget_limit and request.budget_limit > policy.max_budget_usd:
            raise ValueError(f"Job budget {request.budget_limit} exceeds max policy budget {policy.max_budget_usd}")

        # Check max GPUs allowed
        if request.gpu_count > policy.max_gpus_per_job:
            raise ValueError(f"Requested {request.gpu_count} GPUs exceeds max policy limit of {policy.max_gpus_per_job}")

        # Check spot rules
        if request.spot_allowed and not policy.spot_allowed:
            raise ValueError("Spot instances are disabled by organization policy")

        return True
