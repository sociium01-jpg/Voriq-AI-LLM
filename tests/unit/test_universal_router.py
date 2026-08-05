import pytest
from vorik_schemas.router_schemas import RoutingRequest
from services.model_router.universal_router import universal_router

def test_auto_mode_code_routing():
    req = RoutingRequest(
        user_id="u1",
        tenant_id="t1",
        request_text="def compute_fibonacci(n): return n if n <= 1 else compute_fibonacci(n-1)",
        mode="auto"
    )
    decision = universal_router.route_request(req)
    assert decision.selected_agent_id == "coding_agent"
    assert "code_sandbox" in decision.required_tools

def test_auto_mode_indic_routing():
    req = RoutingRequest(
        user_id="u1",
        tenant_id="t1",
        request_text="Enikku tomorrow meeting undu, prepare cheyyan help cheyyamo?",
        mode="auto"
    )
    decision = universal_router.route_request(req)
    assert decision.selected_model_id == "vorik-indic-v1"
    assert decision.selected_agent_id == "indian_language_agent"

def test_manual_mode_reasoning():
    req = RoutingRequest(
        user_id="u1",
        tenant_id="t1",
        request_text="Analyze Q3 market report",
        mode="reasoning"
    )
    decision = universal_router.route_request(req)
    assert decision.selected_model_id == "meta-llama-3.3-70b"

def test_manual_mode_private():
    req = RoutingRequest(
        user_id="u1",
        tenant_id="t1",
        request_text="Tenant sensitive financial data",
        mode="private"
    )
    decision = universal_router.route_request(req)
    assert decision.selected_provider == "vllm-local"
    assert decision.privacy_level_applied == "air_gapped"
