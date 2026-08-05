import pytest
from services.orchestration.tool_registry import tool_registry
from services.orchestration.tool_executor import ToolExecutor

@pytest.mark.anyio
async def test_low_risk_tool_execution():
    executor = ToolExecutor(tool_registry)
    res = await executor.execute_tool_call(
        tool_name="web_search",
        tool_inputs={"query": "DPDP Act startup guide"},
        user_id="user_1",
        tenant_id="tenant_1"
    )
    assert res["status"] == "completed"
    assert "output" in res

@pytest.mark.anyio
async def test_high_risk_human_approval_trigger():
    executor = ToolExecutor(tool_registry)
    res = await executor.execute_tool_call(
        tool_name="send_email",
        tool_inputs={"recipient": "test@domain.com", "subject": "Proposal"},
        user_id="user_1",
        tenant_id="tenant_1"
    )
    assert res["status"] == "awaiting_approval"
    assert "ticket_id" in res
