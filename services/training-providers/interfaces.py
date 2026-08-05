from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Dict, Any, Optional
from vorik_schemas.provider_schemas import (
    TrainingJobRequest, TrainingJobResult, TrainingJobStatus, CostEstimate,
    ResourceMetrics, ModelArtifact, ProviderHealth, InferenceDeploymentRequest,
    InferenceDeploymentResult
)

class TrainingProvider(ABC):
    """Common provider-independent interface for training execution engines"""

    @abstractmethod
    async def validate_configuration(self) -> bool:
        """Validate credentials, region, quotas, and provider configuration."""
        raise NotImplementedError

    @abstractmethod
    async def estimate_cost(self, request: TrainingJobRequest) -> CostEstimate:
        """Estimate GPU, storage, and networking costs before submission."""
        raise NotImplementedError

    @abstractmethod
    async def submit_training_job(self, request: TrainingJobRequest) -> TrainingJobResult:
        """Submit a training job to the selected provider."""
        raise NotImplementedError

    @abstractmethod
    async def get_job_status(self, provider_job_id: str) -> TrainingJobStatus:
        """Return the latest provider job state."""
        raise NotImplementedError

    @abstractmethod
    async def stream_logs(self, provider_job_id: str) -> AsyncIterator[str]:
        """Stream or poll training logs."""
        raise NotImplementedError

    @abstractmethod
    async def cancel_job(self, provider_job_id: str) -> bool:
        """Cancel a running training job."""
        raise NotImplementedError

    @abstractmethod
    async def resume_job(self, provider_job_id: str, checkpoint_uri: str) -> TrainingJobResult:
        """Resume a failed or cancelled job from a checkpoint."""
        raise NotImplementedError

    @abstractmethod
    async def download_artifacts(self, provider_job_id: str) -> List[ModelArtifact]:
        """Retrieve checkpoints, adapters, logs, and reports."""
        raise NotImplementedError

    @abstractmethod
    async def get_resource_metrics(self, provider_job_id: str) -> ResourceMetrics:
        """Return GPU, CPU, memory, and network utilisation."""
        raise NotImplementedError


class InferenceProvider(ABC):
    """Common provider-independent interface for model inference endpoints"""

    @abstractmethod
    async def deploy_endpoint(self, request: InferenceDeploymentRequest) -> InferenceDeploymentResult:
        """Deploy model weights and adapters to inference endpoint."""
        raise NotImplementedError

    @abstractmethod
    async def undeploy_endpoint(self, deployment_id: str) -> bool:
        """Teardown active inference endpoint."""
        raise NotImplementedError

    @abstractmethod
    async def get_endpoint_health(self, deployment_id: str) -> Dict[str, Any]:
        """Check status of deployed inference endpoint."""
        raise NotImplementedError


class StorageProvider(ABC):
    """Abstract canonical storage translator (translates storage:// to gs://, s3://, or local)"""

    @abstractmethod
    def resolve_canonical_uri(self, canonical_uri: str) -> str:
        """Translate storage://datasets/train.jsonl to provider specific URI."""
        raise NotImplementedError

    @abstractmethod
    async def upload_file(self, local_path: str, canonical_uri: str) -> str:
        """Upload local file to canonical storage target."""
        raise NotImplementedError

    @abstractmethod
    async def download_file(self, canonical_uri: str, local_path: str) -> str:
        """Download remote storage target to local file path."""
        raise NotImplementedError


class SecretProvider(ABC):
    """Abstract secret retriever (Google Secret Manager, HashiCorp Vault, K8s Secrets, Env)"""

    @abstractmethod
    async def get_secret(self, secret_key: str) -> Optional[str]:
        """Retrieve secret string securely by key."""
        raise NotImplementedError
