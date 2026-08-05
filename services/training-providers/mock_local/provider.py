import uuid
from datetime import datetime
from typing import AsyncIterator, List
from vorik_schemas.provider_schemas import (
    ProviderType, JobState, TrainingJobRequest, TrainingJobResult, TrainingJobStatus,
    CostEstimate, ResourceMetrics, ModelArtifact
)
from interfaces import TrainingProvider

class MockLocalProvider(TrainingProvider):
    """Local mock training provider for unit tests and local Docker validation"""

    def __init__(self):
        self.jobs = {}

    async def validate_configuration(self) -> bool:
        return True

    async def estimate_cost(self, request: TrainingJobRequest) -> CostEstimate:
        return CostEstimate(
            provider_type=ProviderType.MOCK_LOCAL,
            estimated_gpu_hours=1.0,
            gpu_cost=0.0,
            storage_cost=0.0,
            network_cost=0.0,
            total_estimated_cost=0.0
        )

    async def submit_training_job(self, request: TrainingJobRequest) -> TrainingJobResult:
        prov_id = f"mock_job_{uuid.uuid4().hex[:8]}"
        self.jobs[prov_id] = {
            "request": request,
            "status": JobState.RUNNING,
            "submitted_at": datetime.utcnow()
        }
        return TrainingJobResult(
            job_id=request.job_id,
            provider_type=ProviderType.MOCK_LOCAL,
            provider_job_id=prov_id,
            status=JobState.RUNNING,
            submitted_at=datetime.utcnow(),
            message=f"Submitted mock job {prov_id} locally.",
            output_uri=request.output_uri
        )

    async def get_job_status(self, provider_job_id: str) -> TrainingJobStatus:
        job = self.jobs.get(provider_job_id)
        if not job:
            return TrainingJobStatus(
                job_id="unknown",
                provider_job_id=provider_job_id,
                state=JobState.FAILED,
                error_message="Job not found",
                updated_at=datetime.utcnow()
            )
        return TrainingJobStatus(
            job_id=job["request"].job_id,
            provider_job_id=provider_job_id,
            state=JobState.RUNNING,
            progress_percentage=45.0,
            current_epoch=1,
            total_epochs=3,
            current_step=450,
            total_steps=1000,
            train_loss=0.34,
            updated_at=datetime.utcnow()
        )

    async def stream_logs(self, provider_job_id: str) -> AsyncIterator[str]:
        logs = [
            f"[MockProvider]: Epoch 1/3 started for {provider_job_id}",
            "[MockProvider]: Step 100/1000 - Loss: 0.82",
            "[MockProvider]: Step 450/1000 - Loss: 0.34 (Checkpoint saved)"
        ]
        for line in logs:
            yield line

    async def cancel_job(self, provider_job_id: str) -> bool:
        if provider_job_id in self.jobs:
            self.jobs[provider_job_id]["status"] = JobState.CANCELLED
            return True
        return False

    async def resume_job(self, provider_job_id: str, checkpoint_uri: str) -> TrainingJobResult:
        return await self.submit_training_job(self.jobs[provider_job_id]["request"])

    async def download_artifacts(self, provider_job_id: str) -> List[ModelArtifact]:
        return [
            ModelArtifact(
                artifact_id="art-01",
                name="adapter_model.safetensors",
                uri="storage://models/mock/adapter_model.safetensors",
                file_type="safetensors",
                checksum="sha256_mock_hash_123",
                size_bytes=128000000
            )
        ]

    async def get_resource_metrics(self, provider_job_id: str) -> ResourceMetrics:
        return ResourceMetrics(
            gpu_utilization_pct=88.5,
            gpu_memory_used_gb=24.0,
            gpu_memory_total_gb=80.0,
            cpu_utilization_pct=42.0,
            ram_used_gb=16.0,
            network_tx_gb=1.2
        )
