# backend/scripts/start.sh

#!/bin/bash
set -e

echo "Starting QECopilot Backend Service..."

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "postgres" -U "qubeai" -c '\q'; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
cd /app
alembic upgrade head

# Load initial knowledge base
echo "Loading knowledge base..."
python -c "
from rag.knowledge_base import KnowledgeBase
from rag.rag_service import RAGService
import asyncio

async def load_kb():
    rag = RAGService()
    kb = KnowledgeBase(rag)
    await kb.load_testing_patterns()

asyncio.run(load_kb())
"

# Start the application
echo "Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8080 --workers ${WORKERS:-4} --log-level ${LOG_LEVEL:-info}

---