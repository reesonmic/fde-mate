# FDE Mate Development Scripts

This directory contains optimized development scripts for the FDE Mate platform.

## Quick Start

```bash
# Start all services with hot reload
cd /Users/micreeson/Desktop/AI/fdework/workspace/scripts/dev
./start-dev.sh
```

Access the application:
- **Web UI**: http://localhost:5173
- **API Docs**: http://localhost:8080/docs
- **API Health**: http://localhost:8080/health
- **AI Orchestrator Health**: http://localhost:8090/health

## Available Commands

### start-dev.sh

Main development startup script with Docker support.

```bash
./start-dev.sh              # Start all services in Docker with hot reload
./start-dev.sh --native     # Start only dependencies in Docker, apps run natively
./start-dev.sh --stop       # Stop all dev containers
./start-dev.sh --logs       # Show real-time logs for all services
./start-dev.sh --restart    # Restart all services
./start-dev.sh --build      # Force rebuild of all Docker images
./start-dev.sh --down       # Stop and remove all containers and networks
```

### Traditional Scripts

- `start-all.sh` - Original script that starts services natively (no Docker)

## Architecture

### Dev Mode with Docker (Recommended)

**Advantages:**
- Fast startup using named volumes for dependency caching
- Hot reload for all services (code changes reflect immediately)
- Isolated environment matching production
- No local MySQL/Redis/ES installation needed

**How hot reload works:**
- **Web**: Source code mounted as volume, Vite detects changes and HMR updates page
- **API**: Source code mounted as volume, Uvicorn `--reload` restarts server
- **AI Orchestrator**: Same as API with Uvicorn reload

**Dependency caching:**
- `api-venv`: Python packages for API (cached after first install)
- `ai-venv`: Python packages for AI orchestrator (cached after first install)
- `web-node-modules`: Node.js packages (cached after first install)
- `web-vite-cache`: Vite build cache (faster subsequent builds)

### Native Mode (Alternative)

Dependencies run in Docker, application services run on host:

```bash
./start-dev.sh --native
```

Then in separate terminals:
```bash
# Terminal 1
export DATABASE_URL="mysql+aiomysql://root:fde2026dev@localhost:3306/fde_workbench"
export REDIS_URL="redis://localhost:6379/0"
cd /Users/micreeson/Desktop/AI/fdework/workspace/api && poetry install && poetry run uvicorn app.main:app --reload --port 8080

# Terminal 2
cd /Users/micreeson/Desktop/AI/fdework/workspace/ai-orchestrator && poetry install && poetry run uvicorn app.main:app --reload --port 8090

# Terminal 3
cd /Users/micreeson/Desktop/AI/fdework/workspace/web && npm install && npm run dev:real
```

## Docker Compose Files

### docker-compose.dev.yml

Located at: `/Users/micreeson/Desktop/AI/fdework/workspace/infra/docker-compose/docker-compose.dev.yml`

**Features:**
- All services with hot reload enabled
- Volume mounts for source code
- Named volumes for dependency caching
- Health checks for dependencies
- Celery worker included

**Services included:**
- `mysql` (port 3306)
- `redis` (port 6379)
- `elasticsearch` (port 9200)
- `milvus` (port 19530)
- `api` (port 8080)
- `ai-orchestrator` (port 8090)
- `web` (port 5173)
- `celery-worker` (background tasks)

### Manual Docker Compose (Advanced)

```bash
cd /Users/micreeson/Desktop/AI/fdework/workspace/infra/docker-compose

# Start all services
docker compose -f docker-compose.dev.yml up -d

# View logs
docker compose -f docker-compose.dev.yml logs -f api

# Stop all
docker compose -f docker-compose.dev.yml down

# Stop and remove data volumes (COMPLETE RESET)
docker compose -f docker-compose.dev.yml down -v
```

## Performance Optimizations

### .dockerignore Files

Each service has an optimized `.dockerignore` to minimize build context:

- **API**: `/Users/micreeson/Desktop/AI/fdework/workspace/api/.dockerignore`
- **AI Orchestrator**: `/Users/micreeson/Desktop/AI/fdework/workspace/ai-orchestrator/.dockerignore`
- **Web**: `/Users/micreeson/Desktop/AI/fdework/workspace/web/.dockerignore`

**Ignored items:**
- Git files (`.git/`, `.gitignore`)
- IDE files (`.idea/`, `.vscode/`)
- Dependencies (`node_modules/`, `.venv/`, `__pycache__/`)
- Test/CI files (`.github/`, `tests/` in production)
- Documentation (`*.md`, `docs/`)
- Build outputs (`dist/`, `build/`)
- Local config (`.env*`, except `.env.example`)

### Dockerfile Optimizations

**Web multi-stage build:**
1. `deps` stage: Install dependencies (cached unless package.json changes)
2. `dev` stage: Development server with hot reload
3. `builder` stage: Build for production
4. `production` stage: Caddy serving built files

**API Dockerfile.dev:**
- Poetry virtualenv in project for volume mounting
- Source code mounted, only deps installed in image
- No need to rebuild on code changes

## Troubleshooting

### Services not starting

```bash
# Check logs
./start-dev.sh --logs

# Specific service
docker logs fde-mate-api-dev
```

### Hot reload not working

**Web:**
- Check `CHOKIDAR_USEPOLLING=true` is set
- Ensure Docker Desktop file sharing includes the workspace path

**API/AI:**
- Check volume mount: `docker inspect fde-mate-api-dev | grep -A5 "Mounts"`
- Uvicorn uses `--reload-dir /app/app` to watch only app directory

### Clear all caches (nuclear option)

```bash
# Stop and remove all containers + volumes
./start-dev.sh --down

# Remove named volumes manually
docker volume rm fde-mate-dev_api-venv
docker volume rm fde-mate-dev_ai-venv
docker volume rm fde-mate-dev_web-node-modules
docker volume rm fde-mate-dev_web-vite-cache
```

### Port already in use

```bash
# Check what's using port 8080
lsof -i :8080

# Kill process or change port in docker-compose.dev.yml
```

## Tips

1. **First run will be slow** - Dependencies need to be installed and cached
2. **Subsequent runs are fast** - Named volumes persist packages between runs
3. **Code changes reflect immediately** - No container restart needed
4. **Database migrations run automatically** - On API startup
5. **Use `--logs` for debugging** - Real-time output from all services
