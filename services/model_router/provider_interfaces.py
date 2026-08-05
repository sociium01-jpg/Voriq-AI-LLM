from abc import ABC, abstractmethod
from typing import Dict, Any, List, AsyncGenerator, Optional

class LLMProviderInterface(ABC):
    @abstractmethod
    async def generate_completion(
        self, prompt: str, model_id: str, max_tokens: int = 2048, temperature: float = 0.7
    ) -> Dict[str, Any]:
        """Generate a complete text completion."""
        pass

    @abstractmethod
    async def stream_completion(
        self, prompt: str, model_id: str, max_tokens: int = 2048, temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """Stream completion text tokens."""
        pass

class VisionProviderInterface(ABC):
    @abstractmethod
    async def analyze_image(
        self, image_url_or_bytes: Any, prompt: str, model_id: str
    ) -> Dict[str, Any]:
        """Analyze visual inputs and return structured understanding."""
        pass

class AudioProviderInterface(ABC):
    @abstractmethod
    async def speech_to_text(self, audio_bytes: bytes, language: str = "auto") -> Dict[str, Any]:
        """Transcribe speech to text."""
        pass

    @abstractmethod
    async def text_to_speech(self, text: str, voice_id: str, language: str) -> bytes:
        """Synthesize text to speech audio bytes."""
        pass

class MediaProviderInterface(ABC):
    @abstractmethod
    async def generate_image(self, prompt: str, preset: str, aspect_ratio: str) -> Dict[str, Any]:
        """Generate image visual artifact."""
        pass

    @abstractmethod
    async def generate_video(self, prompt: str, storyboard_script: str, aspect_ratio: str) -> Dict[str, Any]:
        """Generate video artifact."""
        pass

class EmbeddingProviderInterface(ABC):
    @abstractmethod
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for input texts."""
        pass
