#!/bin/bash

# QECopilot - Local Development Setup Script (No Docker Required)
# This script sets up the complete project for local development
echo "Hello from VS Code Terminal!"
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT=$(pwd)

# Function to print colored messages
print_message() {
    echo -e "${2}${1}${NC}"
}

print_message "========================================" "$GREEN"
print_message "QECopilot - Local Development Setup" "$GREEN"
print_message "========================================" "$GREEN"

# Check prerequisites
check_prerequisites() {
    print_message "\n📋 Checking prerequisites..." "$YELLOW"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_message "❌ Python 3 is not installed. Please install Python 3.9 or higher." "$RED"
        exit 1
    fi
    python_version=$(python3 --version | cut -d' ' -f2)
    print_message "✅ Python found: $python_version" "$GREEN"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_message "❌ pip is not installed. Please install pip." "$RED"
        exit 1
    fi
    print_message "✅ pip found: $(pip3 --version)" "$GREEN"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_message "⚠️  Node.js is not installed. Frontend setup will be skipped." "$YELLOW"
        SKIP_FRONTEND=true
    else
        print_message "✅ Node.js found: $(node --version)" "$GREEN"
    fi
    
    # Check PostgreSQL
    if ! command -v psql &> /dev/null; then
        print_message "⚠️  PostgreSQL client not found. Will provide instructions for installation." "$YELLOW"
        INSTALL_POSTGRES=true
    else
        print_message "✅ PostgreSQL client found" "$GREEN"
    fi
}

# Create directory structure
create_directory_structure() {
    print_message "\n📁 Creating directory structure..." "$YELLOW"
    
    directories=(
        "backend/services/qe_copilot/agents"
        "backend/services/qe_copilot/api/v1"
        "backend/services/qe_copilot/config"
        "backend/services/qe_copilot/core"
        "backend/services/qe_copilot/mcp"
        "backend/services/qe_copilot/prompts"
        "backend/services/qe_copilot/rag"
        "backend/services/qe_copilot/services"
        "backend/services/qe_copilot/tests/test_agents"
        "backend/services/qe_copilot/tests/test_services"
        "backend/services/qe_copilot/tests/test_api"
        "backend/services/qe_copilot/utils"
        "backend/services/shared/middleware"
        "backend/services/shared/exceptions"
        "backend/services/shared/logging"
        "backend/scripts"
        "backend/alembic/versions"
        "frontend/src/components"
        "frontend/src/pages"
        "frontend/src/services"
        "frontend/src/styles"
        "frontend/public"
        "workspace/uploads"
        "workspace/exports"
        "workspace/temp"
        "docs"
        "logs"
        "data/chroma_db"
        "data/postgres"
        "knowledge_base"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        echo "  ✓ Created $dir"
    done
    
    # Create __init__.py files for Python packages
    find backend -type d -name "*.pyc" -prune -o -type d -exec touch {}/__init__.py \; 2>/dev/null || true
    
    print_message "✅ Directory structure created successfully" "$GREEN"
}

# Setup Python virtual environment
setup_python_env() {
    print_message "\n🐍 Setting up Python environment..." "$YELLOW"
    
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_message "  ✓ Virtual environment created" "$GREEN"
    else
        print_message "  ✓ Virtual environment already exists" "$GREEN"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Create requirements.txt if it doesn't exist
    if [ ! -f "requirements.txt" ]; then
        cat > requirements.txt << 'EOF'
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
httpx==0.25.2
aiofiles==23.2.1

# Database
sqlalchemy==2.0.23
alembic==1.12.1
asyncpg==0.29.0
psycopg2-binary==2.9.9

# LLM & AI
langchain==0.1.0
langchain-community==0.0.10
langchain-openai==0.0.5
openai==1.6.1
ollama==0.1.7

# Vector Store & Embeddings
chromadb==0.4.22
sentence-transformers==2.2.2

# Data Processing
pandas==2.1.4
openpyxl==3.1.2
python-docx==1.1.0
PyPDF2==3.0.1

# Caching
redis==5.0.1
aiocache==0.12.2

# Utilities
pydantic==2.5.2
pyyaml==6.0.1
click==8.1.7

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Development
black==23.12.0
flake8==6.1.0
mypy==1.7.1
ipython==8.19.0
EOF
        print_message "  ✓ requirements.txt created" "$GREEN"
    fi
    
    # Install dependencies
    print_message "  Installing Python packages..." "$YELLOW"
    pip install -r requirements.txt
    
    print_message "✅ Python environment setup complete" "$GREEN"
    
    cd ..
}

# Setup local PostgreSQL
setup_postgresql() {
    print_message "\n🐘 Setting up PostgreSQL..." "$YELLOW"
    
    if [ "$INSTALL_POSTGRES" = true ]; then
        print_message "  PostgreSQL installation instructions:" "$BLUE"
        print_message "  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib" "$NC"
        print_message "  macOS: brew install postgresql" "$NC"
        print_message "  Windows: Download from https://www.postgresql.org/download/windows/" "$NC"
        print_message "\n  After installation, run this script again." "$YELLOW"
        return
    fi
    
    # Check if PostgreSQL is running
    if ! pg_isready -q 2>/dev/null; then
        print_message "  Starting PostgreSQL service..." "$YELLOW"
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo systemctl start postgresql
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew services start postgresql
        fi
    fi
    
    # Create database and user
    print_message "  Creating database and user..." "$YELLOW"
    
    # Create setup SQL script
    cat > backend/scripts/setup_local_db.sql << 'EOF'
-- Create user if not exists
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'qubeai') THEN
      CREATE ROLE qubeai LOGIN PASSWORD 'qubeai_local_2024';
   END IF;
END
$do$;

-- Create database if not exists
SELECT 'CREATE DATABASE qubeai OWNER qubeai'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'qubeai')\gexec

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE qubeai TO qubeai;
EOF
    
    # Execute SQL script
    sudo -u postgres psql -f backend/scripts/setup_local_db.sql 2>/dev/null || psql -U postgres -f backend/scripts/setup_local_db.sql 2>/dev/null || true
    
    print_message "✅ PostgreSQL setup complete" "$GREEN"
}

# Setup Redis
setup_redis() {
    print_message "\n📦 Setting up Redis..." "$YELLOW"
    
    # Check if Redis is installed
    if ! command -v redis-server &> /dev/null; then
        print_message "  Redis installation instructions:" "$BLUE"
        print_message "  Ubuntu/Debian: sudo apt-get install redis-server" "$NC"
        print_message "  macOS: brew install redis" "$NC"
        print_message "  Windows: Download from https://github.com/microsoftarchive/redis/releases" "$NC"
        print_message "\n  Redis is optional. Continuing setup..." "$YELLOW"
        return
    fi
    
    # Start Redis if not running
    if ! pgrep -x redis-server > /dev/null; then
        print_message "  Starting Redis..." "$YELLOW"
        redis-server --daemonize yes
    fi
    
    print_message "✅ Redis is running" "$GREEN"
}

# Setup Ollama
setup_ollama() {
    print_message "\n🤖 Setting up Ollama..." "$YELLOW"
    
    # Check if Ollama is installed
    if ! command -v ollama &> /dev/null; then
        print_message "  Installing Ollama..." "$YELLOW"
        
        if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
            curl -fsSL https://ollama.ai/install.sh | sh
        else
            print_message "  Please download Ollama from: https://ollama.ai/download" "$BLUE"
            return
        fi
    fi
    
    # Start Ollama service
    print_message "  Starting Ollama service..." "$YELLOW"
    ollama serve > logs/ollama.log 2>&1 &
    sleep 3
    
    # Pull default model
    print_message "  Pulling llama2 model (this may take a few minutes)..." "$YELLOW"
    ollama pull llama2
    
    print_message "✅ Ollama setup complete" "$GREEN"
}

# Setup ChromaDB
setup_chromadb() {
    print_message "\n🎨 Setting up ChromaDB..." "$YELLOW"
    
    cd backend
    source venv/bin/activate
    
    # Create ChromaDB startup script
    cat > scripts/start_chromadb.py << 'EOF'
#!/usr/bin/env python3

import chromadb
from chromadb.config import Settings
import os

# Create persistent client
persist_directory = os.path.join(os.path.dirname(__file__), '../../data/chroma_db')
os.makedirs(persist_directory, exist_ok=True)

client = chromadb.PersistentClient(
    path=persist_directory,
    settings=Settings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

print(f"ChromaDB initialized at: {persist_directory}")
print("ChromaDB is ready for use!")

# Create default collections
collections = [
    "requirements_collection",
    "test_cases_collection",
    "bugs_collection",
    "knowledge_base_collection"
]

for collection_name in collections:
    try:
        client.create_collection(name=collection_name)
        print(f"  ✓ Created collection: {collection_name}")
    except:
        print(f"  ✓ Collection already exists: {collection_name}")
EOF
    
    chmod +x scripts/start_chromadb.py
    python scripts/start_chromadb.py
    
    print_message "✅ ChromaDB setup complete" "$GREEN"
    
    cd ..
}

# Create environment file
create_env_file() {
    print_message "\n📝 Creating environment configuration..." "$YELLOW"
    
    cat > backend/.env << 'EOF'
# Application Settings
APP_NAME=QECopilot
ENVIRONMENT=development

# Database (Local PostgreSQL)
DATABASE_URL=postgresql://qubeai:qubeai_local_2024@localhost:5432/qubeai

# Security
SECRET_KEY=local-dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Settings (Ollama - Local)
LLM_PROVIDER=ollama
LLM_MODEL=llama2
LLM_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4000

# Vector Database (Local ChromaDB)
VECTOR_DB_TYPE=chromadb
VECTOR_DB_PATH=../data/chroma_db
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Redis Cache (Optional)
REDIS_URL=redis://localhost:6379

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Logging
LOG_LEVEL=INFO
LOG_FILE=../logs/qeccopilot.log

# Worker Settings
WORKERS=2
EOF
    
    print_message "✅ Environment file created" "$GREEN"
}

# Initialize database
initialize_database() {
    print_message "\n🗄️ Initializing database..." "$YELLOW"
    
    cd backend
    source venv/bin/activate
    
    # Create alembic configuration
    if [ ! -f "alembic.ini" ]; then
        alembic init alembic
        
        # Update alembic.ini with database URL
        sed -i.bak 's|sqlalchemy.url = .*|sqlalchemy.url = postgresql://qubeai:qubeai_local_2024@localhost:5432/qubeai|' alembic.ini
    fi
    
    # Create initial migration
    cd services/qe_copilot
    
    # Run migrations
    alembic upgrade head 2>/dev/null || true
    
    print_message "✅ Database initialized" "$GREEN"
    
    cd $PROJECT_ROOT
}

# Setup Frontend
setup_frontend() {
    if [ "$SKIP_FRONTEND" = true ]; then
        print_message "\n⚠️  Skipping frontend setup (Node.js not installed)" "$YELLOW"
        return
    fi
    
    print_message "\n⚛️ Setting up frontend..." "$YELLOW"
    
    cd frontend
    
    # Create package.json if it doesn't exist
    if [ ! -f "package.json" ]; then
        cat > package.json << 'EOF'
{
  "name": "qeccopilot-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.2",
    "@mui/material": "^5.15.0",
    "@emotion/react": "^11.11.1",
    "@emotion/styled": "^11.11.0",
    "react-query": "^3.39.3",
    "react-hook-form": "^7.48.2",
    "recharts": "^2.10.3"
  },
  "devDependencies": {
    "@types/node": "^20.10.5",
    "@types/react": "^18.2.45",
    "@types/react-dom": "^18.2.18",
    "eslint": "^8.56.0",
    "eslint-config-next": "14.0.4",
    "typescript": "^5.3.3"
  }
}
EOF
    fi
    
    # Install dependencies
    print_message "  Installing Node packages..." "$YELLOW"
    npm install
    
    print_message "✅ Frontend setup complete" "$GREEN"
    
    cd ..
}

# Create startup scripts
create_startup_scripts() {
    print_message "\n📜 Creating startup scripts..." "$YELLOW"
    
    # Backend startup script
    cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
cd services/qe_copilot
uvicorn main:app --reload --host 0.0.0.0 --port 8080
EOF
    chmod +x start_backend.sh
    
    # Frontend startup script
    cat > start_frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run dev
EOF
    chmod +x start_frontend.sh
    
    # All services startup script
    cat > start_all.sh << 'EOF'
#!/bin/bash

echo "Starting QECopilot Services..."

# Start PostgreSQL
if command -v psql &> /dev/null; then
    if ! pg_isready -q; then
        echo "Starting PostgreSQL..."
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo systemctl start postgresql
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew services start postgresql
        fi
    fi
fi

# Start Redis
if command -v redis-server &> /dev/null; then
    if ! pgrep -x redis-server > /dev/null; then
        echo "Starting Redis..."
        redis-server --daemonize yes
    fi
fi

# Start Ollama
if command -v ollama &> /dev/null; then
    if ! pgrep -x ollama > /dev/null; then
        echo "Starting Ollama..."
        ollama serve > logs/ollama.log 2>&1 &
    fi
fi

# Start Backend
echo "Starting Backend (http://localhost:8080)..."
./start_backend.sh &

# Start Frontend
echo "Starting Frontend (http://localhost:3000)..."
./start_frontend.sh &

echo ""
echo "All services started!"
echo "Backend: http://localhost:8080"
echo "API Docs: http://localhost:8080/docs"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

wait
EOF
    chmod +x start_all.sh
    
    print_message "✅ Startup scripts created" "$GREEN"
}

# Main execution
main() {
    check_prerequisites
    create_directory_structure
    setup_python_env
    setup_postgresql
    setup_redis
    setup_ollama
    setup_chromadb
    create_env_file
    initialize_database
    setup_frontend
    create_startup_scripts
    
    print_message "\n========================================" "$GREEN"
    print_message "✅ QECopilot Local Setup Complete!" "$GREEN"
    print_message "========================================" "$GREEN"
    
    print_message "\n📚 Next Steps:" "$BLUE"
    print_message "  1. Start all services: ./start_all.sh" "$NC"
    print_message "  2. Or start individually:" "$NC"
    print_message "     - Backend: ./start_backend.sh" "$NC"
    print_message "     - Frontend: ./start_frontend.sh" "$NC"
    print_message "\n  3. Access the application:" "$NC"
    print_message "     - Frontend: http://localhost:3000" "$NC"
    print_message "     - API Docs: http://localhost:8080/docs" "$NC"
    print_message "     - Default login: Admin/Admin" "$NC"
    
    print_message "\n📝 Configuration:" "$BLUE"
    print_message "  - Edit backend/.env for configuration changes" "$NC"
    print_message "  - Logs are stored in ./logs/" "$NC"
    print_message "  - Data is stored in ./data/" "$NC"
    
    print_message "\n🐳 Docker Migration:" "$BLUE"
    print_message "  When ready to containerize, run:" "$NC"
    print_message "  ./scripts/dockerize.sh" "$NC"
}

# Run main function
main