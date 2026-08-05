from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator
from vorik_schemas.agent_schemas import AgentTask, AgentResponse, AgentTrace

class AgentRuntimeProvider(ABC):
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> AgentResponse:
        """Execute an agentic task and return structured response."""
        pass

    @abstractmethod
    async def stream_task_execution(self, task: AgentTask) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream step-by-step execution traces and tokens."""
        pass
