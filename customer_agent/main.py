from fastapi import FastAPI, HTTPException
import json
import os
import sys

# Add root to path to import shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import AgentCard, A2ATask, A2AResponse, A2AArtifact
from customer_agent.database import init_db, save_customer

app = FastAPI()

@app.get("/")              
def root():
    return {"status": "Customer Agent is running", "port": 8001}

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/.well-known/agent.json")
async def get_agent_card():
    with open("customer_agent/agent.json", "r") as f:
        return json.load(f)

@app.post("/")
async def handle_task(task: A2ATask):
    if task.capability == "onboard_customer":
        data = task.input_data
        try:
            # Validation
            if not all(k in data for k in ["name", "email", "budget"]):
                raise ValueError("Missing required fields: name, email, budget")
            
            if data["budget"] <= 0:
                raise ValueError("Budget must be greater than 0")

            customer_id = save_customer(
                name=data["name"],
                email=data["email"],
                budget=data["budget"],
                preferences=data.get("preferences", "")
            )

            return A2AResponse(
                task_id=task.task_id,
                status="success",
                artifacts=[
                    A2AArtifact(
                        artifact_id=f"art_{customer_id}",
                        type="customer_id",
                        content={"customer_id": customer_id}
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
    uvicorn.run(app, host="0.0.0.0", port=8001)
