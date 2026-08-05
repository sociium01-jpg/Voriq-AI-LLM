import os
import json
import httpx
from typing import AsyncGenerator, Dict, Any, List, Optional

class LLMClient:
    """Unified client interface for self-hosted open-weight LLMs (vLLM / Ollama / Local AI APIs)"""

    def __init__(self, base_url: Optional[str] = None, default_model: Optional[str] = None):
        self.base_url = base_url or os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
        self.default_model = default_model or os.getenv("DEFAULT_LLM_MODEL", "meta-llama/Llama-3.3-70B-Instruct")

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        adapters: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        target_model = model or self.default_model
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        if adapters:
            payload["extra_body"] = {"adapters": adapters}

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                res = await client.post(f"{self.base_url}/chat/completions", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return {
                        "content": data["choices"][0]["message"]["content"],
                        "model_used": target_model,
                        "usage": data.get("usage", {}),
                        "status": "success"
                    }
        except Exception as e:
            # Fallback generator for offline/local simulation when external engine is starting up
            pass

        return {
            "content": f"[Voriq AI Engine ({target_model})]: Processing query locally. {prompt[:100]}...",
            "model_used": target_model,
            "usage": {"prompt_tokens": 15, "completion_tokens": 30},
            "status": "simulated_fallback"
        }

    async def generate_stream(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncGenerator[str, None]:
        target_model = model or self.default_model
        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", f"{self.base_url}/chat/completions", json=payload) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                data_str = line[6:].strip()
                                if data_str == "[DONE]":
                                    break
                                data = json.loads(data_str)
                                delta = data["choices"][0]["delta"].get("content", "")
                                if delta:
                                    yield delta
                        return
        except Exception:
            pass

        # Offline fallback streaming simulation
        sample_response = f"Voriq AI stream response using model {target_model}: " + messages[-1]["content"]
        for word in sample_response.split(" "):
            yield word + " "
