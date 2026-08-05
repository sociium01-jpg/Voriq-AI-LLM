from typing import Dict, Any, Tuple, Optional
from vorik_schemas.provider_schemas import ProviderType, TrainingJobRequest, CostEstimate
from registry import DEFAULT_PROVIDERS
from policies import ProviderPolicy, PolicyEngine

class TrainingProviderRouter:
    """Intelligent Provider Selection Engine matching job specs to optimal GPU cloud/on-prem provider"""

    def __init__(self):
        self.policy_engine = PolicyEngine()

    def route_training_job(
        self,
        request: TrainingJobRequest,
        policy: Optional[ProviderPolicy] = None
    ) -> Tuple[ProviderType, ProviderType, CostEstimate, str]:
        active_policy = policy or ProviderPolicy(policy_id="default")
        self.policy_engine.validate_request(request, active_policy)

        # Sensitive dataset or strict local residency requirement
        if request.data_residency_requirement == "on-prem" or "sensitive" in request.tags.get("classification", ""):
            primary = ProviderType.ON_PREM_GPU
            fallback = ProviderType.GKE_GPU
            reason = "Routed to On-Premises Air-Gapped GPU Cluster due to strict enterprise data residency policy."
        # Experimental low-cost QLoRA job
        elif request.training_type in ["qlora", "lora"] and request.gpu_count <= 2 and request.spot_allowed:
            primary = ProviderType.RUNPOD
            fallback = ProviderType.GKE_GPU
            reason = "Routed to RunPod Spot GPUs for maximum cost efficiency on small LoRA job."
        # Large distributed training or Cloud Storage dataset
        elif request.distributed_training or request.node_count > 1 or request.gpu_count >= 8:
            primary = ProviderType.VERTEX_AI
            fallback = ProviderType.GKE_GPU
            reason = "Routed to Google Vertex AI / GKE for multi-node distributed training and High-Performance NCCL interconnect."
        # Default production training route
        else:
            primary = ProviderType.VERTEX_AI
            fallback = ProviderType.RUNPOD
            reason = "Routed to Google Vertex AI as primary production cloud provider."

        # Verify allowed by policy
        if primary in active_policy.blocked_providers:
            primary = fallback

        prof = DEFAULT_PROVIDERS.get(primary, DEFAULT_PROVIDERS[ProviderType.MOCK_LOCAL])
        est_hours = (request.max_runtime_minutes / 60.0) * request.gpu_count
        est_cost = est_hours * prof.cost_per_gpu_hour

        estimate = CostEstimate(
            provider_type=primary,
            estimated_gpu_hours=est_hours,
            gpu_cost=est_cost,
            storage_cost=5.0,
            network_cost=2.0,
            total_estimated_cost=est_cost + 7.0
        )

        return primary, fallback, estimate, reason
