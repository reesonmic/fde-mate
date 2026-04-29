#!/usr/bin/env bash
set -e

echo "=== FDE Mate Dev Environment ==="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Starting dependencies...${NC}"
cd "$WORKSPACE_DIR/infra/docker-compose"
docker compose -f docker-compose.deps.yml up -d

echo -e "${BLUE}Waiting for dependencies...${NC}"
sleep 5

echo -e "${BLUE}Starting API...${NC}"
cd "$WORKSPACE_DIR/api"
if command -v poetry &> /dev/null; then
    poetry install --no-interaction
    poetry run uvicorn app.main:app --reload --port 8080 &
else
    pip install -e .
    uvicorn app.main:app --reload --port 8080 &
fi
API_PID=$!

echo -e "${BLUE}Starting AI Orchestrator...${NC}"
cd "$WORKSPACE_DIR/ai-orchestrator"
if [ -d "app" ]; then
    if command -v poetry &> /dev/null; then
        poetry install --no-interaction
        poetry run uvicorn app.main:app --reload --port 8090 &
    else
        pip install -e .
        uvicorn app.main:app --reload --port 8090 &
    fi
else
    echo "AI Orchestrator not yet implemented, skipping..."
fi

echo -e "${BLUE}Starting Web...${NC}"
cd "$WORKSPACE_DIR/web"
npm install
npm run dev &
WEB_PID=$!

echo -e "${GREEN}=== All services started ===${NC}"
echo -e "  API:        http://localhost:8080"
echo -e "  AI Orch:    http://localhost:8090"
echo -e "  Web:        http://localhost:5173"
echo -e "  API Docs:   http://localhost:8080/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for any process to exit
wait
