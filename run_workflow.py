
import asyncio
import os
import sys

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from concierge_agent.orchestrator import orchestrator

async def main():
    print("Starting Federated Multi-Agent Workflow...")
    
    initial_state = {
        "user_request": "I want to onboard a new customer John Doe and analyze a property at 123 Wall St.",
        "agents": {},
        "customer_id": "",
        "property_id": "",
        "market_insight": "",
        "query_results": [],
        "final_response": "",
        "errors": []
    }
    
    try:
        async for output in orchestrator.astream(initial_state):
            for key, value in output.items():
                print(f"\n--- Node: {key} ---")
                if "errors" in value and value["errors"]:
                    print(f"Errors: {value['errors']}")
                else:
                    if "customer_id" in value: print(f"Customer ID: {value['customer_id']}")
                    if "property_id" in value: print(f"Property ID: {value['property_id']}")
                    if "final_response" in value: print(f"Final Response: {value['final_response']}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
