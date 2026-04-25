from fastapi import FastAPI
from langchain_ollama import OllamaLLM
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import AgentCard, A2ATask, A2AResponse, A2AArtifact
from marketing_agent.rag_service import rag_service

app = FastAPI()
llm = OllamaLLM(model="gemma:2b")

@app.get("/.well-known/agent.json")
async def get_agent_card():
    with open("marketing_agent/agent.json", "r") as f:
        return json.load(f)

@app.post("/")
async def handle_task(task: A2ATask):
    if task.capability == "analyze_market":
        data = task.input_data
        property_id = data.get("property_id")
        prop_data = data.get("property_data", {})
        
        # Generate insight using LLM
        prompt = f"Analyze the following real estate property and provide market insights, trends, and risk signals: {json.dumps(prop_data)}"
        insight = llm.invoke(prompt)
        
        # Store in RAG
        ids = rag_service.store_insight(property_id, insight)
        
        return A2AResponse(
            task_id=task.task_id,
            status="success",
            artifacts=[
                A2AArtifact(
                    artifact_id=f"art_insight_{property_id}",
                    type="market_insight",
                    content={"insight": insight, "chunk_ids": ids}
                )
            ]
        )
    
    elif task.capability == "query_market_data":
        query = task.input_data.get("query")
        results = rag_service.query_insights(query)
        
        return A2AResponse(
            task_id=task.task_id,
            status="success",
            artifacts=[
                A2AArtifact(
                    artifact_id=f"art_query_{task.task_id}",
                    type="query_results",
                    content={"results": results}
                )
            ]
        )
    
    return A2AResponse(
        task_id=task.task_id,
        status="error",
        error_message=f"Capability {task.capability} not found"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
