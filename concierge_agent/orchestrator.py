from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
import uuid
import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import A2ATask, AgentCard
from shared.protocol import send_task
from concierge_agent.discovery import get_all_agents

class AgentState(TypedDict):
    user_request: str
    agents: Dict[str, AgentCard]
    customer_id: str
    property_id: str
    market_insight: str
    query_results: List[str]
    final_response: str
    errors: List[str]

# Define Nodes
async def discover_agents_node(state: AgentState):
    agents = await get_all_agents()
    return {"agents": agents}

async def onboard_customer_node(state: AgentState):
    agents = state.get("agents", {})
    if "CustomerOnboardingAgent" not in agents:
        return {"errors": ["CustomerOnboardingAgent not discovered"]}
    
    agent = agents["CustomerOnboardingAgent"]
    # In a real scenario, extract data from user_request using LLM
    # For now, we simulate extracting specific data
    task = A2ATask(
        task_id=str(uuid.uuid4()),
        capability="onboard_customer",
        input_data={
            "name": "John Doe",
            "email": "john@example.com",
            "budget": 500000,
            "preferences": "Modern apartments in NYC"
        }
    )
    
    response = await send_task(agent.endpoint, task)
    if response.status == "success":
        cid = response.artifacts[0].content["customer_id"]
        return {"customer_id": cid}
    else:
        return {"errors": [f"Customer onboarding failed: {response.error_message}"]}

async def onboard_deal_node(state: AgentState):
    agents = state.get("agents", {})
    if "DealOnboardingAgent" not in agents:
        return {"errors": ["DealOnboardingAgent not discovered"]}
    
    agent = agents["DealOnboardingAgent"]
    task = A2ATask(
        task_id=str(uuid.uuid4()),
        capability="onboard_deal",
        input_data={
            "address": "123 Wall St, New York, NY",
            "price": 450000,
            "details": "2 Bed, 2 Bath, 1200 sqft"
        }
    )
    
    response = await send_task(agent.endpoint, task)
    if response.status == "success":
        pid = response.artifacts[0].content["property_id"]
        return {"property_id": pid}
    else:
        return {"errors": [f"Deal onboarding failed: {response.error_message}"]}

async def marketing_analysis_node(state: AgentState):
    agents = state.get("agents", {})
    if "MarketingIntelligenceAgent" not in agents:
        return {"errors": ["MarketingIntelligenceAgent not discovered"]}
    
    agent = agents["MarketingIntelligenceAgent"]
    task = A2ATask(
        task_id=str(uuid.uuid4()),
        capability="analyze_market",
        input_data={
            "property_id": state["property_id"],
            "property_data": {
                "address": "123 Wall St, New York, NY",
                "price": 450000
            }
        }
    )
    
    response = await send_task(agent.endpoint, task)
    if response.status == "success":
        insight = response.artifacts[0].content["insight"]
        return {"market_insight": insight}
    else:
        return {"errors": [f"Marketing analysis failed: {response.error_message}"]}

async def generate_response_node(state: AgentState):
    llm = OllamaLLM(model="gemma:2b")
    prompt = f"""
    You are a Real Estate Concierge. Summarize the onboarding process for the user.
    Customer ID: {state.get('customer_id')}
    Property ID: {state.get('property_id')}
    Market Insight: {state.get('market_insight')}
    
    Provide a professional summary.
    """
    response = llm.invoke(prompt)
    return {"final_response": response}

# Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("discover", discover_agents_node)
workflow.add_node("customer", onboard_customer_node)
workflow.add_node("deal", onboard_deal_node)
workflow.add_node("marketing", marketing_analysis_node)
workflow.add_node("response", generate_response_node)

workflow.set_entry_point("discover")
workflow.add_edge("discover", "customer")
workflow.add_edge("customer", "deal")
workflow.add_edge("deal", "marketing")
workflow.add_edge("marketing", "response")
workflow.add_edge("response", END)

orchestrator = workflow.compile()
