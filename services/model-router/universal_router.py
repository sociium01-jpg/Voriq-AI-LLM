import re
from typing import Dict, Any, List, Optional
from vorik_schemas.router_schemas import (
    RoutingRequest, RoutingDecision, RoutingMode, PrivacyLevel, ModelRegistration
)

class UniversalModelRouter:
    def __init__(self):
        self.model_registry: Dict[str, ModelRegistration] = {
            "vorik-indic-v1": ModelRegistration(
                model_id="vorik-indic-v1",
                provider="vllm-local",
                model_family="Llama-3.3",
                capabilities=["text", "chat", "multilingual", "code-mixed"],
                languages=["en", "hi", "ml", "ta", "te"],
                cost_per_1k_input_tokens=0.0005,
                cost_per_1k_output_tokens=0.001,
                privacy_level="on_premise"
            ),
            "meta-llama-3.3-70b": ModelRegistration(
                model_id="meta-llama-3.3-70b",
                provider="vertex-ai",
                model_family="Llama-3.3",
                capabilities=["text", "reasoning", "coding"],
                cost_per_1k_input_tokens=0.001,
                cost_per_1k_output_tokens=0.002,
                privacy_level="private_cloud"
            ),
            "mistral-7b-instruct": ModelRegistration(
                model_id="mistral-7b-instruct",
                provider="vllm-local",
                model_family="Mistral",
                capabilities=["text", "fast"],
                cost_per_1k_input_tokens=0.0002,
                cost_per_1k_output_tokens=0.0004,
                privacy_level="on_premise"
            ),
            "vorik-vision-pro-v2": ModelRegistration(
                model_id="vorik-vision-pro-v2",
                provider="vllm-local",
                model_family="Vision-Llama",
                capabilities=["vision", "image_understanding"],
                modalities=["text", "image"],
                cost_per_1k_input_tokens=0.0015,
                cost_per_1k_output_tokens=0.003,
                privacy_level="on_premise"
            )
        }

    def route_request(self, request: RoutingRequest) -> RoutingDecision:
        # 1. Check Privacy Constraints
        privacy_level = request.privacy_requirement
        
        # 2. Handle Manual Modes vs Auto Mode
        mode = request.mode

        if mode == "fast":
            return RoutingDecision(
                selected_model_id="mistral-7b-instruct",
                selected_provider="vllm-local",
                selected_agent_id="general_assistant",
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.0002,
                routing_reason="Fast Mode requested: routed to lightweight 7B model.",
                confidence_score=0.98,
                privacy_level_applied=privacy_level
            )

        if mode == "reasoning":
            return RoutingDecision(
                selected_model_id="meta-llama-3.3-70b",
                selected_provider="vertex-ai",
                selected_agent_id="supervisor",
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.0015,
                routing_reason="Reasoning Mode requested: routed to 70B deep reasoning model.",
                confidence_score=0.96,
                privacy_level_applied=privacy_level
            )

        if mode == "coding":
            return RoutingDecision(
                selected_model_id="meta-llama-3.3-70b",
                selected_provider="vertex-ai",
                selected_adapter="voriq-agent-code",
                selected_agent_id="coding_agent",
                required_tools=["code_sandbox", "git_repo_reader", "unit_test_runner"],
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.002,
                routing_reason="Coding Mode requested: routed to Coding Agent sandbox.",
                confidence_score=0.97,
                privacy_level_applied=privacy_level
            )

        if mode == "research":
            return RoutingDecision(
                selected_model_id="meta-llama-3.3-70b",
                selected_provider="vertex-ai",
                selected_agent_id="research_agent",
                required_tools=["web_search", "arxiv_fetcher", "document_rag"],
                required_retrieval_sources=["web_search", "qdrant_vector_store"],
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.0025,
                routing_reason="Research Mode requested: routed to multi-source Research Agent.",
                confidence_score=0.95,
                privacy_level_applied=privacy_level
            )

        if mode == "vision":
            return RoutingDecision(
                selected_model_id="vorik-vision-pro-v2",
                selected_provider="vllm-local",
                selected_agent_id="general_assistant",
                fallback_model_id="meta-llama-3.3-70b",
                estimated_cost_usd=0.002,
                routing_reason="Vision Mode requested: routed to Voriq Vision-Pro V2 model.",
                confidence_score=0.96,
                privacy_level_applied=privacy_level
            )

        if mode == "image":
            return RoutingDecision(
                selected_model_id="voriq-vision-generator",
                selected_provider="local-diffusers",
                selected_agent_id="image_director",
                required_tools=["image_generation_engine"],
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.005,
                routing_reason="Image Mode requested: routed to Image Director Agent.",
                confidence_score=0.99,
                privacy_level_applied=privacy_level
            )

        if mode == "video":
            return RoutingDecision(
                selected_model_id="voriq-video-generator",
                selected_provider="runpod-gpu",
                selected_agent_id="video_director",
                required_tools=["video_generation_engine", "storyboard_builder"],
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.02,
                routing_reason="Video Mode requested: routed to Video Director Agent.",
                confidence_score=0.99,
                privacy_level_applied=privacy_level
            )

        if mode == "private":
            return RoutingDecision(
                selected_model_id="vorik-indic-v1",
                selected_provider="vllm-local",
                selected_agent_id="general_assistant",
                fallback_model_id="mistral-7b-instruct",
                estimated_cost_usd=0.0005,
                routing_reason="Private Mode requested: routed strictly to Air-Gapped local vLLM.",
                confidence_score=1.0,
                privacy_level_applied="air_gapped"
            )

        # AUTO MODE (Default Intelligent Dispatched Routing)
        text = request.request_text.lower()

        # Code detection regex heuristic
        if re.search(r"(def |class |import |function |const |let |curl |select |where |<html)", text):
            return RoutingDecision(
                selected_model_id="meta-llama-3.3-70b",
                selected_provider="vertex-ai",
                selected_adapter="voriq-agent-code",
                selected_agent_id="coding_agent",
                required_tools=["code_sandbox", "unit_test_runner"],
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.0015,
                routing_reason="Auto Mode: Code syntax detected -> routed to Coding Agent.",
                confidence_score=0.94,
                privacy_level_applied=privacy_level
            )

        # Indic code-mixed language detection regex heuristic
        if re.search(r"(kya|karo|bhai|enikku|naale|cheyyamo|vanakkam|namaste|telipe)", text):
            return RoutingDecision(
                selected_model_id="vorik-indic-v1",
                selected_provider="vllm-local",
                selected_adapter="voriq-agent-general",
                selected_agent_id="indian_language_agent",
                fallback_model_id="meta-llama-3.3-70b",
                estimated_cost_usd=0.0005,
                routing_reason="Auto Mode: Indic Romanised code-mixed text detected -> routed to Voriq Indic Foundation V1.",
                confidence_score=0.96,
                privacy_level_applied=privacy_level
            )

        # Complex reasoning heuristic
        if re.search(r"(analyze|compare|proof|architect|evaluate|forecast|compliance)", text):
            return RoutingDecision(
                selected_model_id="meta-llama-3.3-70b",
                selected_provider="vertex-ai",
                selected_agent_id="supervisor",
                fallback_model_id="vorik-indic-v1",
                estimated_cost_usd=0.0015,
                routing_reason="Auto Mode: Complex analytical request detected -> routed to Deep Reasoning Model.",
                confidence_score=0.92,
                privacy_level_applied=privacy_level
            )

        # Default fallback general routing
        return RoutingDecision(
            selected_model_id="vorik-indic-v1",
            selected_provider="vllm-local",
            selected_agent_id="general_assistant",
            fallback_model_id="meta-llama-3.3-70b",
            estimated_cost_usd=0.0005,
            routing_reason="Auto Mode: General query -> routed to primary Voriq Indic Foundation V1.",
            confidence_score=0.90,
            privacy_level_applied=privacy_level
        )

# Global Router Instance
universal_router = UniversalModelRouter()
