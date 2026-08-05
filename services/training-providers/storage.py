import os
from vorik_schemas.provider_schemas import ProviderType
from interfaces import StorageProvider

class CanonicalStorageResolver(StorageProvider):
    """Translates canonical storage:// URIs into provider-specific storage URIs"""

    def __init__(self, default_provider: ProviderType = ProviderType.VERTEX_AI):
        self.default_provider = default_provider

    def resolve_canonical_uri(self, canonical_uri: str, target_provider: Optional[ProviderType] = None) -> str:
        provider = target_provider or self.default_provider

        # Strip storage:// prefix
        path = canonical_uri.replace("storage://", "")

        if provider in [ProviderType.VERTEX_AI, ProviderType.GKE_GPU]:
            bucket = os.getenv("S3_BUCKET_NAME", "vorik-ai-artifacts")
            return f"gs://{bucket}/{path}"
        elif provider in [ProviderType.RUNPOD, ProviderType.LAMBDA_LABS, ProviderType.COREWEAVE]:
            bucket = os.getenv("S3_BUCKET_NAME", "vorik-ai-artifacts")
            return f"s3://{bucket}/{path}"
        elif provider == ProviderType.ON_PREM_GPU:
            return f"/mnt/onprem_storage/{path}"
        else:
            return f"./storage_local/{path}"

    async def upload_file(self, local_path: str, canonical_uri: str) -> str:
        resolved = self.resolve_canonical_uri(canonical_uri)
        return resolved

    async def download_file(self, canonical_uri: str, local_path: str) -> str:
        return local_path
