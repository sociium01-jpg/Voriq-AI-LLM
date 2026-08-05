from typing import Dict, List, Optional
from vorik_schemas.agent_schemas import ToolDefinition

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {
            "web_search": ToolDefinition(
                tool_id="tool_web_search",
                name="web_search",
                description="Search real-time web sources and news.",
                input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
                output_schema={"type": "object", "properties": {"results": {"type": "array"}}},
                provider="bing_duckduckgo",
                category="Search",
                risk_classification="low"
            ),
            "code_sandbox": ToolDefinition(
                tool_id="tool_code_sandbox",
                name="code_sandbox",
                description="Safely execute code snippets in isolated container sandbox.",
                input_schema={"type": "object", "properties": {"code": {"type": "string"}, "language": {"type": "string"}}},
                output_schema={"type": "object", "properties": {"stdout": {"type": "string"}, "exit_code": {"type": "integer"}}},
                provider="docker_sandbox",
                category="Code execution",
                risk_classification="medium"
            ),
            "document_rag": ToolDefinition(
                tool_id="tool_document_rag",
                name="document_rag",
                description="Retrieve passages from uploaded tenant documents with exact line/page citations.",
                input_schema={"type": "object", "properties": {"query": {"type": "string"}, "doc_ids": {"type": "array"}}},
                output_schema={"type": "object", "properties": {"citations": {"type": "array"}}},
                provider="qdrant_pgvector",
                category="Retrieval",
                risk_classification="low"
            ),
            "send_email": ToolDefinition(
                tool_id="tool_send_email",
                name="send_email",
                description="Send outbound email to external recipient.",
                input_schema={"type": "object", "properties": {"recipient": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}},
                output_schema={"type": "object", "properties": {"message_id": {"type": "string"}}},
                provider="smtp_sendgrid",
                category="Email",
                risk_classification="high",
                approval_required=True
            ),
            "delete_data": ToolDefinition(
                tool_id="tool_delete_data",
                name="delete_data",
                description="Purge or delete records from production database or cloud bucket.",
                input_schema={"type": "object", "properties": {"target_resource": {"type": "string"}}},
                output_schema={"type": "object", "properties": {"deleted": {"type": "boolean"}}},
                provider="postgres_gcs",
                category="Database",
                risk_classification="critical",
                approval_required=True
            ),
            "spend_money": ToolDefinition(
                tool_id="tool_spend_money",
                name="spend_money",
                description="Authorize financial transaction or API subscription billing.",
                input_schema={"type": "object", "properties": {"amount_usd": {"type": "number"}, "vendor": {"type": "string"}}},
                output_schema={"type": "object", "properties": {"transaction_id": {"type": "string"}}},
                provider="stripe_gateway",
                category="Finance",
                risk_classification="critical",
                approval_required=True
            ),
            "create_cloud_resource": ToolDefinition(
                tool_id="tool_create_cloud_resource",
                name="create_cloud_resource",
                description="Provision new GKE GPU node pool, VM, or storage bucket.",
                input_schema={"type": "object", "properties": {"resource_type": {"type": "string"}, "specs": {"type": "object"}}},
                output_schema={"type": "object", "properties": {"resource_id": {"type": "string"}}},
                provider="gcp_terraform",
                category="Deployment",
                risk_classification="high",
                approval_required=True
            ),
            "clone_voice_face": ToolDefinition(
                tool_id="tool_clone_voice_face",
                name="clone_voice_face",
                description="Generate synthetic voice or visual face replica for media creation.",
                input_schema={"type": "object", "properties": {"character_id": {"type": "string"}}},
                output_schema={"type": "object", "properties": {"clone_id": {"type": "string"}}},
                provider="voriq_character_engine",
                category="Voice generation",
                risk_classification="critical",
                approval_required=True
            )
        }

    def get_tool(self, tool_name: str) -> Optional[ToolDefinition]:
        return self.tools.get(tool_name)

    def list_tools(self) -> List[ToolDefinition]:
        return list(self.tools.values())

tool_registry = ToolRegistry()
