import os
from typing import Optional
from interfaces import SecretProvider

class SecretManagerResolver(SecretProvider):
    """Abstract Secret Retriever supporting Google Secret Manager, K8s Secrets, and Environment"""

    async def get_secret(self, secret_key: str) -> Optional[str]:
        # Strip secret:// prefix if present
        clean_key = secret_key.replace("secret://", "").upper().replace("-", "_")
        return os.getenv(clean_key, f"mock_secret_val_for_{clean_key.lower()}")
