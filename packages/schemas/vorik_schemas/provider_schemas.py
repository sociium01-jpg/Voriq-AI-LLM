from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ProviderType(str, Enum):
    VERTEX_AI = "vertex-ai"
    GKE_GPU = "gke-gpu"
    NVIDIA_DGX_CLOUD = "nvidia-dgx-cloud"
    RUNPOD = "runpod"
    LAMBDA_LABS = "lambda-labs"
    COREWEAVE = "coreweave"
    ON_PREM_GPU = "on-prem-gpu"
    MOCK_LOCAL = "mock-local"

class JobState(str, Enum):
    QUEUED = "queued"
    VALIDATING = "validating"
    PREPARING = "preparing"
    SUBMITTED = "submitted"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RESUMING = "resuming"

class TrainingJobRequest(BaseModel):
    job_id: str
    organisation_id: str
    workspace_id: str
    training_type: str  # sft, lora, qlora, dpo
    base_model: str
    dataset_uri: str  # storage://datasets/indic-v1/train.jsonl
    validation_dataset_uri: Optional[str] = None
    output_uri: str  # storage://models/voriq-indic-adapter/
    container_image: str = "vorik/training-runner:latest"
    entrypoint: List[str] = ["python", "-m", "vorik_trainer"]
    environment_variables: Dict[str, str] = Field(default_factory=dict)
    machine_profile: str = "n1-standard-8-gpu"
    gpu_type: str = "NVIDIA_A100_80GB"
    gpu_count: int = 1
    cpu_count: int = 8
    memory_gb: int = 32
    disk_gb: int = 100
    distributed_training: bool = False
    node_count: int = 1
    spot_allowed: bool = False
    max_runtime_minutes: int = 1440
    budget_limit: Optional[float] = None
    checkpoint_interval_steps: int = 500
    resume_checkpoint_uri: Optional[str] = None
    region_preferences: List[str] = Field(default_factory=lambda: ["us-central1", "asia-south1"])
    data_residency_requirement: Optional[str] = None
    tags: Dict[str, str] = Field(default_factory=dict)

class TrainingJobResult(BaseModel):
    job_id: str
    provider_type: ProviderType
    provider_job_id: str
    status: JobState
    submitted_at: datetime
    message: str
    output_uri: str
    estimated_cost: float = 0.0

class TrainingJobStatus(BaseModel):
    job_id: str
    provider_job_id: str
    state: JobState
    progress_percentage: float = 0.0
    current_epoch: int = 0
    total_epochs: int = 1
    current_step: int = 0
    total_steps: int = 1000
    train_loss: Optional[float] = None
    val_loss: Optional[float] = None
    error_message: Optional[str] = None
    updated_at: datetime

class CostEstimate(BaseModel):
    provider_type: ProviderType
    estimated_gpu_hours: float
    gpu_cost: float
    storage_cost: float
    network_cost: float
    total_estimated_cost: float
    currency: str = "USD"
    confidence_level: str = "high"

class ResourceMetrics(BaseModel):
    gpu_utilization_pct: float
    gpu_memory_used_gb: float
    gpu_memory_total_gb: float
    cpu_utilization_pct: float
    ram_used_gb: float
    network_tx_gb: float

class ModelArtifact(BaseModel):
    artifact_id: str
    name: str
    uri: str
    file_type: str  # safetensors, json, bin
    checksum: str
    size_bytes: int

class ProviderHealth(BaseModel):
    provider_type: ProviderType
    is_healthy: bool
    authentication_status: str
    available_gpus: Dict[str, int]
    supported_regions: List[str]
    last_checked_at: datetime

class ProviderProfile(BaseModel):
    provider_id: str
    name: str
    provider_type: ProviderType
    enabled: bool = True
    supported_regions: List[str]
    supported_gpus: List[str]
    max_gpu_count: int
    spot_supported: bool
    distributed_supported: bool
    cost_per_gpu_hour: float
    current_health: ProviderHealth

class InferenceDeploymentRequest(BaseModel):
    deployment_id: str
    model_id: str
    adapter_uris: List[str] = Field(default_factory=list)
    min_replicas: int = 1
    max_replicas: int = 4
    gpu_type: str = "NVIDIA_A100_80GB"
    region: str = "asia-south1"

class InferenceDeploymentResult(BaseModel):
    deployment_id: str
    endpoint_url: str
    provider_type: ProviderType
    status: str
