import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.protocol import discover_agent
from shared.models import AgentCard
from typing import Dict

# Pre-defined list of potential agent URLs (in a real system, this could be a registry)
AGENT_URLS = [
    "http://localhost:8001", # Customer Agent
    "http://localhost:8002", # Deal Agent
    "http://localhost:8003", # Marketing Agent
]

async def get_all_agents() -> Dict[str, AgentCard]:
    agents = {}
    for url in AGENT_URLS:
        card = await discover_agent(url)
        if card:
            agents[card.name] = card
    return agents
