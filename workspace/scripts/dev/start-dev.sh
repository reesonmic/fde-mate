#!/usr/bin/env bash
#
# start-dev.sh - Quick development environment startup script
#
# Usage:
#   ./start-dev.sh              # Start all services with Docker
#   ./start-dev.sh --native     # Start with native services (no Docker for apps)
#   ./start-dev.sh --stop       # Stop all dev containers
#   ./start-dev.sh --logs       # Show logs for all services
#   ./start-dev.sh --restart    # Restart all services
#
# Features:
# - Optimized for fast iteration with hot reload
# - Persistent dependency caching via named volumes
# - Parallel service startup for dependencies
# - Health check monitoring before starting app services

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
COMPOSE_FILE="$WORKSPACE_DIR/infra/docker-compose/docker-compose.dev.yml"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Show usage
usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  (none)       Start all services in Docker with hot reload"
    echo "  --native     Start dependencies in Docker, apps natively"
    echo "  --stop       Stop and remove all dev containers"
    echo "  --logs       Show logs for all services"
    echo "  --restart    Restart all services"
    echo "  --build      Force rebuild of all service images"
    echo "  --down       Stop and remove containers with volumes"
    echo "  -h, --help   Show this help message"
    echo ""
    echo "Services:"
    echo "  - MySQL (port 3306)"
    echo "  - Redis (port 6379)"
    echo "  - Elasticsearch (port 9200)"
    echo "  - Milvus (port 19530)"
    echo "  - API (port 8080) - with hot reload"
    echo "  - AI Orchestrator (port 8090) - with hot reload"
    echo "  - Web (port 5173) - with hot reload"
    echo ""
    echo "URLs when running:"
    echo "  Web UI:      http://localhost:5173"
    echo "  API Docs:    http://localhost:8080/docs"
    echo "  API Health:  http://localhost:8080/health"
    echo "  AI Health:   http://localhost:8090/health"
}

# Check if Docker is running
check_docker() {
    if ! docker info &>/dev/null; then
        log_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Start services with Docker
docker_start() {
    check_docker

    log_info "Starting FDE Mate development environment..."
    log_info "Compose file: $COMPOSE_FILE"

    cd "$WORKSPACE_DIR/infra/docker-compose"

    # Pull latest images for dependencies
    log_info "Pulling dependency images..."
    docker compose -f "$COMPOSE_FILE" pull mysql redis 2>/dev/null || true

    # Build app images if needed
    if [[ "${1:-}" == "--build" ]]; then
        log_info "Building service images..."
        docker compose -f "$COMPOSE_FILE" build --no-cache
    else
        log_info "Building service images (using cache)..."
        docker compose -f "$COMPOSE_FILE" build
    fi

    # Start dependencies first
    log_info "Starting database and cache services..."
    docker compose -f "$COMPOSE_FILE" up -d mysql redis elasticsearch milvus

    # Wait for dependencies to be healthy
    log_info "Waiting for dependencies to be ready..."
    local max_wait=120
    local waited=0

    while ! docker compose -f "$COMPOSE_FILE" ps | grep -q "healthy"; do
        if [[ $waited -ge $max_wait ]]; then
            log_error "Dependencies failed to start within ${max_wait}s"
            log_info "Check logs with: $0 --logs"
            exit 1
        fi
        echo -n "."
        sleep 2
        waited=$((waited + 2))
    done
    echo ""  # New line after dots
    log_success "Dependencies are ready!"

    # Run database migrations
    log_info "Running database migrations..."
    docker compose -f "$COMPOSE_FILE" run --rm api poetry run alembic upgrade head 2>/dev/null || \
        log_warn "Migrations completed with warnings or already applied"

    # Start app services
    log_info "Starting application services with hot reload..."
    docker compose -f "$COMPOSE_FILE" up -d api ai-orchestrator web

    # Wait a moment for services to initialize
    sleep 3

    # Check if services are running
    if docker compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        echo ""
        log_success "=== All services started successfully! ==="
        echo ""
        echo -e "  ${GREEN}Web UI:${NC}      http://localhost:5173"
        echo -e "  ${GREEN}API Docs:${NC}    http://localhost:8080/docs"
        echo -e "  ${GREEN}API Health:${NC}  http://localhost:8080/health"
        echo -e "  ${GREEN}AI Health:${NC}   http://localhost:8090/health"
        echo ""
        log_info "View logs with: ./start-dev.sh --logs"
        log_info "Stop services with: ./start-dev.sh --stop"
        echo ""
    else
        log_error "Some services failed to start. Check logs with: $0 --logs"
        exit 1
    fi
}

# Stop services
docker_stop() {
    check_docker
    log_info "Stopping development services..."
    docker compose -f "$COMPOSE_FILE" stop
    log_success "Services stopped."
}

# Stop and remove containers
docker_down() {
    check_docker
    log_warn "Stopping and removing containers..."
    docker compose -f "$COMPOSE_FILE" down
    log_success "Containers removed."
}

# Stop and remove containers AND volumes (DANGER: data loss)
docker_down_volumes() {
    check_docker
    log_warn "This will REMOVE ALL DATA (MySQL, Redis, ES, Milvus)"
    read -p "Are you sure? Type 'yes' to continue: " confirm
    if [[ "$confirm" == "yes" ]]; then
        docker compose -f "$COMPOSE_FILE" down -v
        log_success "Containers and volumes removed."
    else
        log_info "Cancelled."
    fi
}

# Show logs
docker_logs() {
    check_docker
    log_info "Showing logs (Ctrl+C to exit)..."
    docker compose -f "$COMPOSE_FILE" logs -f --tail=100
}

# Start services natively (dependencies in Docker, apps on host)
native_start() {
    check_docker

    log_info "Starting dependencies in Docker..."
    cd "$WORKSPACE_DIR/infra/docker-compose"

    # Start only database and cache services
    docker compose -f "$COMPOSE_FILE" up -d mysql redis elasticsearch milvus

    # Wait for dependencies
    log_info "Waiting for dependencies to be ready..."
    local max_wait=120
    local waited=0

    while ! docker compose -f "$COMPOSE_FILE" ps | grep -q "healthy"; do
        if [[ $waited -ge $max_wait ]]; then
            log_error "Dependencies failed to start within ${max_wait}s"
            exit 1
        fi
        echo -n "."
        sleep 2
        waited=$((waited + 2))
    done
    echo ""
    log_success "Dependencies are ready!"

    echo ""
    log_info "Now start services natively in separate terminals:"
    echo ""
    echo "  # Terminal 1 - API:"
    echo "  cd $WORKSPACE_DIR/api && poetry install && poetry run uvicorn app.main:app --reload --port 8080"
    echo ""
    echo "  # Terminal 2 - AI Orchestrator:"
    echo "  cd $WORKSPACE_DIR/ai-orchestrator && poetry install && poetry run uvicorn app.main:app --reload --port 8090"
    echo ""
    echo "  # Terminal 3 - Web:"
    echo "  cd $WORKSPACE_DIR/web && npm install && npm run dev:real"
    echo ""
}

# Main command handler
case "${1:-}" in
    "-h" | "--help" | "help")
        usage
        exit 0
        ;;
    "--stop" | "stop")
        docker_stop
        exit 0
        ;;
    "--down" | "down")
        docker_down
        exit 0
        ;;
    "--down-volumes")
        docker_down_volumes
        exit 0
        ;;
    "--logs" | "logs")
        docker_logs
        exit 0
        ;;
    "--restart" | "restart")
        docker_down
        docker_start
        ;;
    "--build" | "build")
        docker_start "--build"
        ;;
    "--native" | "native")
        native_start
        ;;
    "")
        docker_start
        ;;
    *)
        log_error "Unknown option: $1"
        usage
        exit 1
        ;;
esac
