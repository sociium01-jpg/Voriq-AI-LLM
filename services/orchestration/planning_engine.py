import uuid
from typing import List, Dict, Any
from vorik_schemas.agent_schemas import AgentPlan, PlanStep

class PlanningEngine:
    def create_plan(self, goal: str, available_tools: List[str]) -> AgentPlan:
        steps = []
        approval_required = False

        # Heuristic step generator for multi-step task planning
        if "web_search" in available_tools or "search" in goal.lower():
            steps.append(
                PlanStep(
                    step_id=f"step_{uuid.uuid4().hex[:6]}",
                    objective="Gather multi-source context and empirical evidence",
                    agent_id="research_agent",
                    tool_name="web_search",
                    inputs={"query": goal},
                    expected_output="Verified document & search snippets",
                    verification_method="citation_check"
                )
            )

        if "code_sandbox" in available_tools or "code" in goal.lower() or "script" in goal.lower():
            steps.append(
                PlanStep(
                    step_id=f"step_{uuid.uuid4().hex[:6]}",
                    objective="Generate, review, and execute code solution",
                    agent_id="coding_agent",
                    tool_name="code_sandbox",
                    inputs={"code_goal": goal},
                    expected_output="Clean passing unit test trace",
                    verification_method="unit_test"
                )
            )

        # Sensitive tool check for human approval trigger
        sensitive_keywords = ["send_email", "delete_data", "spend_money", "deploy_model", "create_cloud_resource"]
        if any(tool in available_tools for tool in sensitive_keywords) or any(k in goal.lower() for k in ["delete", "buy", "deploy", "email"]):
            approval_required = True
            steps.append(
                PlanStep(
                    step_id=f"step_{uuid.uuid4().hex[:6]}",
                    objective="Request Human Approval for sensitive business action",
                    agent_id="safety_agent",
                    tool_name="human_approval_gate",
                    inputs={"action_summary": goal},
                    expected_output="Human admin approval signature",
                    approval_required=True,
                    verification_method="approval_check"
                )
            )

        # Default synthesis step
        steps.append(
            PlanStep(
                step_id=f"step_{uuid.uuid4().hex[:6]}",
                objective="Synthesize final verified response with citations",
                agent_id="verification_agent",
                expected_output="Structured final response",
                verification_method="evidence_reconciliation"
            )
        )

        return AgentPlan(
            goal=goal,
            assumptions=["Model endpoints active", "Tenant privacy policies enforced"],
            steps=steps,
            required_tools=available_tools,
            estimated_cost=0.0015,
            estimated_runtime_seconds=5,
            approval_required=approval_required,
            success_criteria=["Goal completed without hallucinated tools", "Verification passed"]
        )

planning_engine = PlanningEngine()
