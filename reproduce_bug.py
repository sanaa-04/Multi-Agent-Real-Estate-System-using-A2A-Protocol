import asyncio
import httpx
from shared.models import A2ATask, A2AResponse
from shared.protocol import send_task

async def test():
    task = A2ATask(task_id="test", capability="test", input_data={})
    # This URL should return 500 or 404
    url = "http://localhost:8003" 
    print("Sending task...")
    try:
        resp = await send_task(url, task)
        print(f"Response: {resp}")
        print(f"Status: {resp.status}")
    except Exception as e:
        print(f"CAUGHT: {e}")

if __name__ == "__main__":
    asyncio.run(test())
