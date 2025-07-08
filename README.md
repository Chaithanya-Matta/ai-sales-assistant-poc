# AI Sales Assistant Proof of Concept

This repository contains a small proof of concept for an AI powered sales assistant. The backend is built with **FastAPI** and orchestrates several agent functions using **LangGraph**. It integrates with OpenAI for language models and Pinecone for vector search. A simple Streamlit frontend is included for interactive testing.

## Architecture overview

```
Client (Streamlit) -> FastAPI (/chat) -> LangGraph orchestrator -> agents
```

- **FastAPI** exposes a `/chat` endpoint in `routers/chat_router.py`. Requests are handled by the LangGraph orchestrator defined in `orchestrator/coordinator.py`.
- **Agents** in the `agents/` folder implement specific tasks such as address look‑up and upsell recommendations.
- **State management** is defined in `state/state.py` which tracks the conversation and which agent should run next.
- **Vector search** is configured in `config/vector_store_config.py` and uses Pinecone.
- **Database access** is set up in `config/postgres_config.py` and uses SQLAlchemy to connect to Postgres.

## Environment variables

Create a `.env` file in the project root and provide the following variables:

```bash
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_TEMPERATURE=1.0

PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_NAME=addresses

POSTGRES_DB_USER=admin
POSTGRES_DB_PASSWORD=admin
```

These variables are loaded in `config/settings.py` and used across the application.

## Running with Docker Compose

Build and start the FastAPI application together with a local Postgres instance:

```bash
docker-compose up --build
```

The API will be available on <http://localhost:8001> and Postgres on port `5432`.

## Example API request

Send a chat query to the assistant:

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"query": "I need an address in Seattle"}' \
     http://localhost:8001/chat
```

## Launching the Streamlit UI

Install dependencies (or use a virtual environment) and run:

```bash
FASTAPI_URL=http://localhost:8001 streamlit run ui/streamlit_app.py
```

This opens a browser window where you can interact with the assistant in a chat interface.
