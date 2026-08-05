import uuid
from datetime import datetime
from typing import AsyncIterator, List
from vorik_schemas.provider_schemas import (
    ProviderType, JobState, TrainingJobRequest, TrainingJobResult, TrainingJobStatus,
    CostEstimate, ResourceMetrics, ModelArtifact
)
from interfaces import TrainingProvider

class RunPodProvider(TrainingProvider):
    """RunPod Secure Cloud Pods & Spot GPU Provider Adapter"""

    def __init__(self, api_key: str = "runpod_mock_api_key"):
        self.api_key = api_key
        self.pods = {}

    async def validate_configuration(self) -> bool:
        return True

    async def estimate_cost(self, request: TrainingJobRequest) -> CostEstimate:
        est_hours = (request.max_runtime_minutes / 60.0) * request.gpu_count
        gpu_rate = 1.89
        return CostEstimate(
            provider_type=ProviderType.RUNPOD,
            estimated_gpu_hours=est_hours,
            gpu_cost=est_hours * gpu_rate,
            storage_cost=1.0,
            network_cost=0.5,
            total_estimated_cost=(est_hours * gpu_rate) + 1.5
        )

    async def submit_training_job(self, request: TrainingJobRequest) -> TrainingJobResult:
        pod_id = f"pod_{uuid.uuid4().hex[:10]}"
        self.pods[pod_id] = {"request": request, "status": JobState.RUNNING}
        return TrainingJobResult(
            job_id=request.job_id,
            provider_type=ProviderType.RUNPOD,
            provider_job_id=pod_id,
            status=JobState.RUNNING,
            submitted_at=datetime.utcnow(),
            message=f"RunPod GPU Pod {pod_id} created successfully.",
            output_uri=request.output_uri
        )

    async def get_job_status(self, provider_job_id: str) -> TrainingJobStatus:
        return TrainingJobStatus(
            job_id="runpod_job",
            provider_job_id=provider_job_id,
            state=JobState.RUNNING,
            progress_percentage=80.0,
            current_epoch=2,
            total_epochs=2,
            current_step=800,
            total_steps=1000,
            train_loss=0.22,
            updated_at=datetime.utcnow()
        )

    async def stream_logs(self, provider_job_id: str) -> AsyncIterator[str]:
        yield f"[RunPod Pod Log]: Container running job {provider_job_id}..."

    async def cancel_job(self, provider_job_id: str) -> bool:
        if provider_job_id in self.pods:
            self.pods[provider_job_id]["status"] = JobState.CANCELLED
            return True
        return False

    async def resume_job(self, provider_job_id: str, checkpoint_uri: str) -> TrainingJobResult:
        return await self.submit_training_job(self.pods[provider_job_id]["request"])

    async def download_artifacts(self, provider_job_id: str) -> List[ModelArtifact]:
        return [
            ModelArtifact(
                artifact_id="art-runpod-01",
                name="adapter_model.safetensors",
                uri="storage://models/runpod/adapter_model.safetensors",
                file_type="safetensors",
                checksum="sha256_runpod_hash",
                size_bytes=150000000
            )
        ]

    async def get_resource_metrics(self, provider_job_id: str) -> ResourceMetrics:
        return ResourceMetrics(
            gpu_utilization_pct=96.0,
            gpu_memory_used_gb=70.0,
            gpu_memory_total_gb=80.0,
            cpu_utilization_pct=38.0,
            ram_used_gb=18.0,
            network_tx_gb=2.0
        )
