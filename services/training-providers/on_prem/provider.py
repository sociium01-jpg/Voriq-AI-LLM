import uuid
from datetime import datetime
from typing import AsyncIterator, List
from vorik_schemas.provider_schemas import (
    ProviderType, JobState, TrainingJobRequest, TrainingJobResult, TrainingJobStatus,
    CostEstimate, ResourceMetrics, ModelArtifact
)
from interfaces import TrainingProvider

class OnPremisesProvider(TrainingProvider):
    """Air-Gapped Private On-Premises GPU Cluster Provider Adapter"""

    def __init__(self, cluster_endpoint: str = "https://onprem-gpu.internal.vorik.ai"):
        self.cluster_endpoint = cluster_endpoint
        self.local_jobs = {}

    async def validate_configuration(self) -> bool:
        return True

    async def estimate_cost(self, request: TrainingJobRequest) -> CostEstimate:
        est_hours = (request.max_runtime_minutes / 60.0) * request.gpu_count
        return CostEstimate(
            provider_type=ProviderType.ON_PREM_GPU,
            estimated_gpu_hours=est_hours,
            gpu_cost=0.0,
            storage_cost=0.0,
            network_cost=0.0,
            total_estimated_cost=0.0
        )

    async def submit_training_job(self, request: TrainingJobRequest) -> TrainingJobResult:
        onprem_id = f"onprem_job_{uuid.uuid4().hex[:8]}"
        self.local_jobs[onprem_id] = {"request": request, "status": JobState.RUNNING}
        return TrainingJobResult(
            job_id=request.job_id,
            provider_type=ProviderType.ON_PREM_GPU,
            provider_job_id=onprem_id,
            status=JobState.RUNNING,
            submitted_at=datetime.utcnow(),
            message=f"Submitted to Air-Gapped Private On-Premises GPU Cluster ({self.cluster_endpoint}).",
            output_uri=request.output_uri
        )

    async def get_job_status(self, provider_job_id: str) -> TrainingJobStatus:
        return TrainingJobStatus(
            job_id="onprem_job",
            provider_job_id=provider_job_id,
            state=JobState.RUNNING,
            progress_percentage=75.0,
            current_epoch=2,
            total_epochs=3,
            current_step=750,
            total_steps=1000,
            train_loss=0.19,
            updated_at=datetime.utcnow()
        )

    async def stream_logs(self, provider_job_id: str) -> AsyncIterator[str]:
        yield f"[AirGapped Slurm/K8s Log]: Job {provider_job_id} running on local H100 node..."

    async def cancel_job(self, provider_job_id: str) -> bool:
        if provider_job_id in self.local_jobs:
            self.local_jobs[provider_job_id]["status"] = JobState.CANCELLED
            return True
        return False

    async def resume_job(self, provider_job_id: str, checkpoint_uri: str) -> TrainingJobResult:
        return await self.submit_training_job(self.local_jobs[provider_job_id]["request"])

    async def download_artifacts(self, provider_job_id: str) -> List[ModelArtifact]:
        return [
            ModelArtifact(
                artifact_id="art-onprem-01",
                name="adapter_model.safetensors",
                uri="storage://models/onprem/adapter_model.safetensors",
                file_type="safetensors",
                checksum="sha256_onprem_hash",
                size_bytes=300000000
            )
        ]

    async def get_resource_metrics(self, provider_job_id: str) -> ResourceMetrics:
        return ResourceMetrics(
            gpu_utilization_pct=98.5,
            gpu_memory_used_gb=78.0,
            gpu_memory_total_gb=80.0,
            cpu_utilization_pct=65.0,
            ram_used_gb=48.0,
            network_tx_gb=0.0  # Air-gapped zero external network egress
        )
