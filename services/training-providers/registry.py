from datetime import datetime
from typing import Dict, List, Optional
from vorik_schemas.provider_schemas import ProviderType, ProviderProfile, ProviderHealth

DEFAULT_PROVIDERS: Dict[ProviderType, ProviderProfile] = {
    ProviderType.VERTEX_AI: ProviderProfile(
        provider_id="prov_vertex_ai",
        name="Google Vertex AI Custom Training",
        provider_type=ProviderType.VERTEX_AI,
        enabled=True,
        supported_regions=["us-central1", "asia-south1", "europe-west4"],
        supported_gpus=["NVIDIA_A100_80GB", "NVIDIA_H100_80GB", "NVIDIA_T4", "NVIDIA_L4"],
        max_gpu_count=16,
        spot_supported=True,
        distributed_supported=True,
        cost_per_gpu_hour=3.67,
        current_health=ProviderHealth(
            provider_type=ProviderType.VERTEX_AI,
            is_healthy=True,
            authentication_status="authenticated",
            available_gpus={"NVIDIA_A100_80GB": 32, "NVIDIA_H100_80GB": 8},
            supported_regions=["us-central1", "asia-south1"],
            last_checked_at=datetime.utcnow()
        )
    ),
    ProviderType.GKE_GPU: ProviderProfile(
        provider_id="prov_gke_gpu",
        name="Google Kubernetes Engine (GKE GPU Node Pools)",
        provider_type=ProviderType.GKE_GPU,
        enabled=True,
        supported_regions=["asia-south1", "us-central1"],
        supported_gpus=["NVIDIA_A100_80GB", "NVIDIA_L4"],
        max_gpu_count=64,
        spot_supported=True,
        distributed_supported=True,
        cost_per_gpu_hour=2.95,
        current_health=ProviderHealth(
            provider_type=ProviderType.GKE_GPU,
            is_healthy=True,
            authentication_status="authenticated",
            available_gpus={"NVIDIA_A100_80GB": 64},
            supported_regions=["asia-south1"],
            last_checked_at=datetime.utcnow()
        )
    ),
    ProviderType.RUNPOD: ProviderProfile(
        provider_id="prov_runpod",
        name="RunPod Secure Cloud GPUs",
        provider_type=ProviderType.RUNPOD,
        enabled=True,
        supported_regions=["us-east", "eu-central"],
        supported_gpus=["NVIDIA_A100_80GB", "NVIDIA_RTX_4090"],
        max_gpu_count=8,
        spot_supported=True,
        distributed_supported=False,
        cost_per_gpu_hour=1.89,
        current_health=ProviderHealth(
            provider_type=ProviderType.RUNPOD,
            is_healthy=True,
            authentication_status="authenticated",
            available_gpus={"NVIDIA_A100_80GB": 16},
            supported_regions=["us-east"],
            last_checked_at=datetime.utcnow()
        )
    ),
    ProviderType.ON_PREM_GPU: ProviderProfile(
        provider_id="prov_on_prem",
        name="Voriq On-Premises Air-Gapped GPU Cluster",
        provider_type=ProviderType.ON_PREM_GPU,
        enabled=True,
        supported_regions=["local-datacenter"],
        supported_gpus=["NVIDIA_H100_80GB", "NVIDIA_A100_80GB"],
        max_gpu_count=32,
        spot_supported=False,
        distributed_supported=True,
        cost_per_gpu_hour=0.0,
        current_health=ProviderHealth(
            provider_type=ProviderType.ON_PREM_GPU,
            is_healthy=True,
            authentication_status="authenticated",
            available_gpus={"NVIDIA_H100_80GB": 16},
            supported_regions=["local-datacenter"],
            last_checked_at=datetime.utcnow()
        )
    ),
    ProviderType.MOCK_LOCAL: ProviderProfile(
        provider_id="prov_mock_local",
        name="Local Development Mock Provider",
        provider_type=ProviderType.MOCK_LOCAL,
        enabled=True,
        supported_regions=["localhost"],
        supported_gpus=["CPU", "MOCK_GPU"],
        max_gpu_count=4,
        spot_supported=False,
        distributed_supported=False,
        cost_per_gpu_hour=0.0,
        current_health=ProviderHealth(
            provider_type=ProviderType.MOCK_LOCAL,
            is_healthy=True,
            authentication_status="authenticated",
            available_gpus={"MOCK_GPU": 4},
            supported_regions=["localhost"],
            last_checked_at=datetime.utcnow()
        )
    ),
}

class ProviderRegistry:
    """Registry maintaining active cloud & on-premises GPU training provider profiles"""

    def __init__(self):
        self.providers: Dict[ProviderType, ProviderProfile] = DEFAULT_PROVIDERS.copy()

    def get_provider_profile(self, provider_type: ProviderType) -> Optional[ProviderProfile]:
        return self.providers.get(provider_type)

    def list_active_providers() -> List[ProviderProfile]:
        return [p for p in self.providers.values() if p.enabled and p.current_health.is_healthy]
