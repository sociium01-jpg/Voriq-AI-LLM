import pytest
from vorik_schemas.provider_schemas import ProviderType, JobState, TrainingJobRequest
from interfaces import TrainingProvider
from mock_local.provider import MockLocalProvider
from vertex_ai.provider import VertexAIProvider
from gke.provider import GKEProvider
from runpod.provider import RunPodProvider
from on_prem.provider import OnPremisesProvider

import sys, os
sys.path.insert(0, os.path.abspath("services/training-providers"))

PROVIDERS_TO_TEST: list[type[TrainingProvider]] = [
    MockLocalProvider,
    VertexAIProvider,
    GKEProvider,
    RunPodProvider,
    OnPremisesProvider,
]

@pytest.mark.anyio
@pytest.mark.parametrize("provider_cls", PROVIDERS_TO_TEST)
async def test_provider_contract_interface(provider_cls):
    provider: TrainingProvider = provider_cls()

    # 1. Validate Configuration
    config_valid = await provider.validate_configuration()
    assert config_valid is True

    # 2. Estimate Cost
    req = TrainingJobRequest(
        job_id="job_contract_test",
        organisation_id="org_test",
        workspace_id="ws_test",
        training_type="qlora",
        base_model="meta-llama/Llama-3.3-70B-Instruct",
        dataset_uri="storage://datasets/test.jsonl",
        output_uri="storage://models/output/"
    )
    cost = await provider.estimate_cost(req)
    assert cost.total_estimated_cost >= 0.0

    # 3. Submit Job
    res = await provider.submit_training_job(req)
    assert res.job_id == "job_contract_test"
    assert res.status in [JobState.RUNNING, JobState.SUBMITTED]
    assert len(res.provider_job_id) > 0

    # 4. Get Status
    status = await provider.get_job_status(res.provider_job_id)
    assert status.state in [JobState.RUNNING, JobState.SUBMITTED]

    # 5. Resource Metrics
    metrics = await provider.get_resource_metrics(res.provider_job_id)
    assert metrics.gpu_utilization_pct >= 0.0

    # 6. Artifacts
    artifacts = await provider.download_artifacts(res.provider_job_id)
    assert len(artifacts) >= 1

    # 7. Cancel Job
    cancelled = await provider.cancel_job(res.provider_job_id)
    assert cancelled is True
