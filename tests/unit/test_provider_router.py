import pytest
import sys, os
sys.path.insert(0, os.path.abspath("services/training-providers"))

from vorik_schemas.provider_schemas import ProviderType, TrainingJobRequest
from router import TrainingProviderRouter
from policies import ProviderPolicy

def test_router_sensitive_data_residency():
    router = TrainingProviderRouter()
    req = TrainingJobRequest(
        job_id="job_sensitive",
        organisation_id="org_enterprise",
        workspace_id="ws_01",
        training_type="sft",
        base_model="meta-llama/Llama-3.3-70B-Instruct",
        dataset_uri="storage://datasets/confidential.jsonl",
        output_uri="storage://models/sensitive/",
        data_residency_requirement="on-prem"
    )
    primary, fallback, est, reason = router.route_training_job(req)
    assert primary == ProviderType.ON_PREM_GPU
    assert "On-Premises" in reason

def test_router_qlora_low_cost():
    router = TrainingProviderRouter()
    req = TrainingJobRequest(
        job_id="job_qlora_test",
        organisation_id="org_dev",
        workspace_id="ws_01",
        training_type="qlora",
        base_model="mistralai/Mistral-7B-Instruct-v0.3",
        dataset_uri="storage://datasets/test.jsonl",
        output_uri="storage://models/output/",
        gpu_count=1,
        spot_allowed=True
    )
    primary, fallback, est, reason = router.route_training_job(req)
    assert primary == ProviderType.RUNPOD
    assert "RunPod" in reason

def test_router_distributed_training():
    router = TrainingProviderRouter()
    policy = ProviderPolicy(policy_id="distributed_policy", max_gpus_per_job=64)
    req = TrainingJobRequest(
        job_id="job_distributed",
        organisation_id="org_prod",
        workspace_id="ws_01",
        training_type="sft",
        base_model="meta-llama/Llama-3.3-70B-Instruct",
        dataset_uri="storage://datasets/large_corpus.jsonl",
        output_uri="storage://models/dist/",
        distributed_training=True,
        node_count=4,
        gpu_count=32
    )
    primary, fallback, est, reason = router.route_training_job(req, policy)
    assert primary == ProviderType.VERTEX_AI
    assert "Vertex AI" in reason

def test_policy_budget_enforcement():
    router = TrainingProviderRouter()
    policy = ProviderPolicy(policy_id="strict_budget", max_budget_usd=100.0)
    req = TrainingJobRequest(
        job_id="job_expensive",
        organisation_id="org_test",
        workspace_id="ws_01",
        training_type="sft",
        base_model="llama-70b",
        dataset_uri="storage://ds.jsonl",
        output_uri="storage://out/",
        budget_limit=250.0  # Exceeds max budget
    )
    with pytest.raises(ValueError, match="exceeds max policy budget"):
        router.route_training_job(req, policy)
