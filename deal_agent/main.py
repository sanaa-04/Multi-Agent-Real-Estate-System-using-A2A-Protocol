from fastapi import FastAPI
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import AgentCard, A2ATask, A2AResponse, A2AArtifact
from deal_agent.database import init_db, save_property

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/.well-known/agent.json")
async def get_agent_card():
    with open("deal_agent/agent.json", "r") as f:
        return json.load(f)

@app.post("/")
async def handle_task(task: A2ATask):
    if task.capability == "onboard_deal":
        data = task.input_data
        try:
            if not all(k in data for k in ["address", "price"]):
                raise ValueError("Missing required fields: address, price")

            property_id = save_property(
                address=data["address"],
                price=data["price"],
                details=data.get("details", "")
            )

            return A2AResponse(
                task_id=task.task_id,
                status="success",
                artifacts=[
                    A2AArtifact(
                        artifact_id=f"art_{property_id}",
                        type="property_id",
                        content={"property_id": property_id}
                    )
                ]
            )
        except Exception as e:
            return A2AResponse(
                task_id=task.task_id,
                status="error",
                error_message=str(e)
            )
    
    return A2AResponse(
        task_id=task.task_id,
        status="error",
        error_message=f"Capability {task.capability} not found"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
