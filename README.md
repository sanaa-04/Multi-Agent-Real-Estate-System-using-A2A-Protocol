# Federated Multi-Agent Real Estate System

This project implements a **Federated Multi-Agent System** designed to handle real estate workflows, including customer onboarding, property registration, and market intelligence analysis. It uses a decentralized architecture where specialized agents collaborate via a standardized communication protocol.

## 🚀 Key Features

-   **Federated Architecture**: Independent agents for Customer, Deal, and Marketing management.
-   **Orchestration with LangGraph**: Uses a graph-based state machine to coordinate agent tasks.
-   **Local LLM Integration**: Powered by **Ollama** (Gemma:2b) for privacy and local execution.
-   **RAG (Retrieval-Augmented Generation)**: Marketing agent utilizes **ChromaDB** for persistent market intelligence storage and retrieval.
-   **Robust Protocol**: Custom agent-to-agent (A2A) protocol built on FastAPI and HTTPX.

## 🏗 Project Structure

```text
├── concierge_agent/    # Main orchestrator using LangGraph
├── customer_agent/     # Manages customer data (SQLite)
├── deal_agent/         # Manages property/deal data (SQLite)
├── marketing_agent/    # Market analysis & RAG (ChromaDB + LLM)
├── shared/             # Common models and communication protocol
└── run_workflow.py     # Main entry point to run the system
```

## 🛠 Prerequisites

-   Python 3.9+
-   [Ollama](https://ollama.com/) installed and running.
-   Required LLM model: `ollama pull gemma:2b`

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    cd Assignment
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🚦 How to Run

### 1. Start the Agent Servers
Each agent runs as an independent microservice. Open separate terminals and run:

-   **Customer Agent**: `python customer_agent/main.py` (Port 8001)
-   **Deal Agent**: `python deal_agent/main.py` (Port 8002)
-   **Marketing Agent**: `python marketing_agent/main.py` (Port 8003)

### 2. Execute the Workflow
Once the agents are running, execute the main orchestrator:
```bash
python run_workflow.py
```

## 🧪 Workflow Logic

1.  **Discovery**: The Concierge scans the network to find available agents.
2.  **Customer Node**: Sends a task to the Customer Agent to register a new client.
3.  **Deal Node**: Sends a task to the Deal Agent to register a property.
4.  **Marketing Node**: Sends a task to the Marketing Agent to analyze market trends for the property.
5.  **Response Node**: Aggregates all results and uses the LLM to generate a final summary.

## 🛡 Robustness Features

-   **Error Handling**: The protocol layer includes fallback mechanisms for JSON failures and agent timeouts.
-   **Memory Efficiency**: Optimized to run on systems with limited RAM (~4GB) by utilizing smaller quantized models.
-   **Decentralized State**: Each agent maintains its own database, ensuring data sovereignty.
