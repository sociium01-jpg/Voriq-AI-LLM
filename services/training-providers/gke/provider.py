import uuid
from datetime import datetime
from typing import AsyncIterator, List
from vorik_schemas.provider_schemas import (
    ProviderType, JobState, TrainingJobRequest, TrainingJobResult, TrainingJobStatus,
    CostEstimate, ResourceMetrics, ModelArtifact
)
from interfaces import TrainingProvider

class GKEProvider(TrainingProvider):
    """Google Kubernetes Engine (GKE) GPU Node Pool & PyTorchJob Provider Adapter"""

    def __init__(self, cluster_name: str = "vorik-gpu-cluster", namespace: str = "vorik-training"):
        self.cluster_name = cluster_name
        self.namespace = namespace
        self.k8s_jobs = {}

    async def validate_configuration(self) -> bool:
        return True

    async def estimate_cost(self, request: TrainingJobRequest) -> CostEstimate:
        est_hours = (request.max_runtime_minutes / 60.0) * request.gpu_count
        gpu_rate = 2.95
        return CostEstimate(
            provider_type=ProviderType.GKE_GPU,
            estimated_gpu_hours=est_hours,
            gpu_cost=est_hours * gpu_rate,
            storage_cost=2.0,
            network_cost=1.0,
            total_estimated_cost=(est_hours * gpu_rate) + 3.0
        )

    async def submit_training_job(self, request: TrainingJobRequest) -> TrainingJobResult:
        k8s_job_name = f"pytorch-job-{uuid.uuid4().hex[:8]}"
        
        # Manifest structure for K8s Job / PyTorchJob
        k8s_manifest = {
            "apiVersion": "kubeflow.org/v1",
            "kind": "PyTorchJob",
            "metadata": {
                "name": k8s_job_name,
                "namespace": self.namespace
            },
            "spec": {
                "pytorchReplicaSpecs": {
                    "Master": {
                        "replicas": 1,
                        "template": {
                            "spec": {
                                "containers": [{
                                    "name": "pytorch",
                                    "image": request.container_image,
                                    "resources": {
                                        "limits": {
                                            "nvidia.com/gpu": request.gpu_count
                                        }
                                    }
                                }]
                            }
                        }
                    }
                }
            }
        }

        self.k8s_jobs[k8s_job_name] = {
            "manifest": k8s_manifest,
            "request": request,
            "status": JobState.RUNNING
        }

        return TrainingJobResult(
            job_id=request.job_id,
            provider_type=ProviderType.GKE_GPU,
            provider_job_id=k8s_job_name,
            status=JobState.RUNNING,
            submitted_at=datetime.utcnow(),
            message=f"PyTorchJob {k8s_job_name} submitted to GKE cluster {self.cluster_name}.",
            output_uri=request.output_uri
        )

    async def get_job_status(self, provider_job_id: str) -> TrainingJobStatus:
        return TrainingJobStatus(
            job_id="gke_job",
            provider_job_id=provider_job_id,
            state=JobState.RUNNING,
            progress_percentage=50.0,
            current_epoch=1,
            total_epochs=2,
            current_step=500,
            total_steps=1000,
            train_loss=0.31,
            updated_at=datetime.utcnow()
        )

    async def stream_logs(self, provider_job_id: str) -> AsyncIterator[str]:
        yield f"[GKE kubectl logs]: Pod {provider_job_id}-master-0 starting..."

    async def cancel_job(self, provider_job_id: str) -> bool:
        if provider_job_id in self.k8s_jobs:
            self.k8s_jobs[provider_job_id]["status"] = JobState.CANCELLED
            return True
        return False

    async def resume_job(self, provider_job_id: str, checkpoint_uri: str) -> TrainingJobResult:
        return await self.submit_training_job(self.k8s_jobs[provider_job_id]["request"])

    async def download_artifacts(self, provider_job_id: str) -> List[ModelArtifact]:
        return [
            ModelArtifact(
                artifact_id="art-gke-01",
                name="adapter_model.safetensors",
                uri="storage://models/gke/adapter_model.safetensors",
                file_type="safetensors",
                checksum="sha256_gke_hash",
                size_bytes=200000000
            )
        ]

    async def get_resource_metrics(self, provider_job_id: str) -> ResourceMetrics:
        return ResourceMetrics(
            gpu_utilization_pct=91.0,
            gpu_memory_used_gb=68.0,
            gpu_memory_total_gb=80.0,
            cpu_utilization_pct=52.0,
            ram_used_gb=24.0,
            network_tx_gb=3.1
        )
