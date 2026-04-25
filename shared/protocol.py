import httpx
import logging
from typing import List, Optional
from .models import AgentCard, A2ATask, A2AResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("A2AProtocol")

async def discover_agent(url: str) -> Optional[AgentCard]:
    """Fetch Agent Card from the well-known endpoint."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{url.rstrip('/')}/.well-known/agent.json")
            if response.status_code == 200:
                return AgentCard(**response.json())
            else:
                logger.error(f"Failed to discover agent at {url}: {response.status_code}")
        except Exception as e:
            logger.error(f"Error discovering agent at {url}: {str(e)}")
    return None

async def send_task(agent_url: str, task: A2ATask) -> A2AResponse:
    """Send a task to an agent's main endpoint."""
    async with httpx.AsyncClient() as client:
        try:
            # Use model_dump() for Pydantic v2
            task_data = task.model_dump() if hasattr(task, 'model_dump') else task.dict()
            response = await client.post(agent_url, json=task_data, timeout=30.0)
            
            status_code = getattr(response, 'status_code', None)
            
            if status_code == 200:
                try:
                    return A2AResponse(**response.json())
                except Exception as e:
                    return A2AResponse(
                        task_id=task.task_id,
                        status="error",
                        error_message=f"Invalid JSON response from agent: {str(e)}"
                    )
            else:
                return A2AResponse(
                    task_id=task.task_id,
                    status="error",
                    error_message=f"Agent returned status code {status_code}: {getattr(response, 'text', 'No detail available')}"
                )
        except Exception as e:
            return A2AResponse(
                task_id=task.task_id,
                status="error",
                error_message=f"Communication error: {str(e)}"
            )
