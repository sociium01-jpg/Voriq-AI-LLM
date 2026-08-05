from typing import Dict, Any, List, Optional
from vorik_schemas.models import ModelRoute, LanguageEnum, ScriptEnum

AVAILABLE_MODELS = {
    "llm_primary": "meta-llama/Llama-3.3-70B-Instruct",
    "llm_fallback": "mistralai/Mistral-7B-Instruct-v0.3",
    "llm_indic_lora": "vorik-indic-adapter-v1",
    "image_primary": "stabilityai/stable-diffusion-xl-base-1.0",
    "video_primary": "ali-vilab/text-to-video-ms-1.7b",
}

class ModelRouter:
    """Provider-independent dynamic model gateway and adapter selector"""

    def __init__(self):
        self.circuit_breaker_active = False

    def route_request(
        self,
        task_type: str,
        language: LanguageEnum,
        script: ScriptEnum,
        is_romanised: bool = False,
        domain: Optional[str] = None
    ) -> ModelRoute:
        adapters = []

        # Indic language adapter routing
        if language != LanguageEnum.ENGLISH or is_romanised:
            adapters.append(f"{language.value}-romanised-adapter" if is_romanised else f"{language.value}-native-adapter")

        # Domain adapter routing
        if domain:
            adapters.append(f"{domain}-domain-adapter")

        base_model = AVAILABLE_MODELS["llm_primary"]
        fallback = AVAILABLE_MODELS["llm_fallback"]

        if self.circuit_breaker_active:
            base_model = fallback

        return ModelRoute(
            task_type=task_type,
            language=language.value,
            script=script.value,
            complexity="medium" if len(adapters) > 0 else "standard",
            domain=domain,
            base_model=base_model,
            adapters=adapters,
            tools=["web_search"] if task_type == "research" else [],
            temperature=0.7,
            max_tokens=2048,
            fallback_model=fallback
        )

    def trigger_circuit_breaker(self, active: bool = True):
        self.circuit_breaker_active = active
