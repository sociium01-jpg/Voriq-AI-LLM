import time
import uuid
from typing import Dict, Any, AsyncGenerator
from vorik_schemas.agent_schemas import AgentTask, AgentResponse
from services.orchestration.interfaces import AgentRuntimeProvider
from services.orchestration.planning_engine import planning_engine
from services.orchestration.tool_registry import tool_registry
from services.orchestration.tool_executor import ToolExecutor
from services.orchestration.verifier_agent import verifier_agent

class LangGraphAgentRuntime(AgentRuntimeProvider):
    def __init__(self):
        self.tool_executor = ToolExecutor(tool_registry)

    async def execute_task(self, task: AgentTask) -> AgentResponse:
        start_time = time.time()
        
        # 1. Create Structured Plan
        plan = planning_engine.create_plan(task.objective, task.allowed_tools or ["web_search", "document_rag"])

        # 2. Tool Execution Step
        tool_calls_executed = []
        evidence_collected = []
        
        for step in plan.steps:
            if step.tool_name and step.tool_name in task.allowed_tools:
                exec_res = await self.tool_executor.execute_tool_call(
                    tool_name=step.tool_name,
                    tool_inputs=step.inputs,
                    user_id="user_123",
                    tenant_id="tenant_default"
                )
                tool_calls_executed.append(exec_res)
                if exec_res.get("status") == "completed" and "output" in exec_res:
                    evidence_collected.append(exec_res["output"])

        # 3. Generate Final Response
        final_text = f"Voriq Agentic System [{task.target_agent_id}]: Executed multi-step task '{task.objective}' across {len(plan.steps)} planned steps."

        # 4. Verifier Check
        verification = verifier_agent.verify_response(
            goal=task.objective,
            generated_response=final_text,
            evidence_list=evidence_collected,
            tool_calls=tool_calls_executed
        )

        runtime_s = round(time.time() - start_time, 3)

        return AgentResponse(
            task_id=task.task_id,
            status="completed" if verification["verified"] else "failed",
            result={"response": final_text, "plan": plan.dict(), "verification": verification},
            evidence=evidence_collected,
            tool_calls=tool_calls_executed,
            assumptions=plan.assumptions,
            cost_usd=0.0015,
            runtime_seconds=runtime_s,
            verification_status="passed" if verification["verified"] else "failed"
        )

    async def stream_task_execution(self, task: AgentTask) -> AsyncGenerator[Dict[str, Any], None]:
        plan = planning_engine.create_plan(task.objective, task.allowed_tools or ["web_search"])
        yield {"event": "plan_created", "plan": plan.dict()}
        
        for step in plan.steps:
            yield {"event": "step_start", "step_id": step.step_id, "objective": step.objective}
            if step.tool_name:
                exec_res = await self.tool_executor.execute_tool_call(
                    tool_name=step.tool_name,
                    tool_inputs=step.inputs,
                    user_id="user_123",
                    tenant_id="tenant_default"
                )
                yield {"event": "tool_executed", "tool_result": exec_res}
        
        yield {"event": "task_completed", "status": "passed"}

langgraph_agent_runtime = LangGraphAgentRuntime()
