from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AgentCapability(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]

class AgentCard(BaseModel):
    name: str
    role: str
    description: str
    endpoint: str
    capabilities: List[AgentCapability]

class A2ATask(BaseModel):
    task_id: str
    capability: str
    input_data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = {}

class A2AArtifact(BaseModel):
    artifact_id: str
    type: str
    content: Any
    metadata: Optional[Dict[str, Any]] = {}

class A2AResponse(BaseModel):
    task_id: str
    status: str # "success", "error"
    artifacts: List[A2AArtifact] = []
    error_message: Optional[str] = None
