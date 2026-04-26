# Local & Open-Source AI Stack

A self‑hosted, modular AI inference and automation platform that runs entirely on local hardware, with strict data sovereignty and minimal external dependencies.  
This project follows a **Spec‑Driven Development (SDD)** workflow and adheres to the [Project Constitution](.spec/instructions.md).

## 🏗️ Architecture

The stack is built around **Docker Compose** micro‑services, each running in its own container, orchestrated via a central `docker‑compose.yml` file.  
Key architectural principles:

- **Container‑First:** All services run inside Docker containers.
- **Persistent Data:** All runtime data lives inside the `.docker/data/services/` directory, which is git‑ignored. No environment variable is needed — the stack always uses this fixed path.
- **Supervisord Supervision:** All application scripts are managed by `supervisord` inside a dedicated container.
- **Spec‑Driven Development:** Every change follows the SDD cycle (read spec → update tasks → implement → commit).

## 📁 Project Structure

```
.
├── .spec/                     # Project intelligence, constitution, specs, tasks
├── services/                  # All Docker Compose service definitions
│   ├── ollama/               # LLM inference (CPU/GPU)
│   ├── openwebui/            # Web UI for LLMs (CPU/GPU)
│   ├── traefik/              # Reverse proxy & load balancer
│   ├── supervisord/          # Process supervision container
│   ├── redis/                # In‑memory cache (example)
│   └── [service]/            # Other services (see below)
├── scripts/                  # Maintenance & automation bash scripts
├── src/                      # Core application logic (modular Python)
│   └── pipes/                # Pipe implementations (e.g., n8n_pipe)
├── assets/                   # Static assets (logos, etc.)
├── docs/                     # MkDocs documentation source
├── mkdocs.yml                # Material for MkDocs configuration
├── .docker/                  # Runtime persistent data (git‑ignored)
├── .repo/                    # External repository cache (git‑ignored)
└── docker‑compose.yml        # Root composition that includes all services
```

## 🚀 Getting Started

### Prerequisites

- **Docker** & **Docker Compose** (v2+)
- **NVIDIA Container Toolkit** (for GPU‑accelerated services)
- **Linux** (tested on Pop!_OS / Ubuntu)

### Launch the Stack

1. **Clone the repository** and navigate into it:
   ```bash
   git clone https://github.com/your‑org/localai‑stack.git
   cd localai‑stack
   ```

2. **Create the host data directories** (optional – they will be created automatically on first run):
   ```bash
   mkdir -p .docker/data/services
   ```

3. **Start the services** (this will pull images and start containers):
   ```bash
   docker‑compose up –detach
   ```

4. **Access the services** (via Traefik):
   - Traefik dashboard: `http://traefik.localhost`
   - OpenWebUI (CPU): `http://open‑cpu.localhost`
   - OpenWebUI (GPU): `http://open‑gpu.localhost`
   - Supervisord web UI: `http://supervisord.localhost` (user `admin`, password `localai`)
   - Supervisord Monitor: `http://supervisord-monitor.localhost`
   - LocalAI Dashboard: `http://dashboard.localhost`
   - Ollama API: `http://localhost:11434` (CPU) or `:11435` (GPU)

## 🔧 Core Services

| Service | Role | Image | Port | Host Data Path |
|---------|------|-------|------|----------------|
| traefik | Reverse Proxy | `traefik:latest` | 80, 443 | – |
| ollama‑cpu | LLM Inference (CPU) | `ollama/ollama` | 11434 | ./.docker/data/services/ollama |
| ollama‑gpu | LLM Inference (GPU) | `ollama/ollama` | 11435 | ./.docker/data/services/ollama |
| openwebui‑cpu | Web UI (CPU) | `ghcr.io/open‑webui/open‑webui:main` | 3030 | ./.docker/data/services/openwebui‑cpu |
| openwebui‑gpu | Web UI (GPU) | `ghcr.io/open‑webui/open‑webui:main` | 3031 | ./.docker/data/services/openwebui‑gpu |
| supervisord | Process Supervisor | Custom (services/supervisord/Dockerfile.supervisord) | 9001 | ./.docker/data/services/supervisord |
| supervisord‑monitor | Supervisor Web UI Monitoring | `dockage/supervisor‑web:2.2.0` | 80 | – |
| localai | LocalAI Dashboard & Workspace Canvas | Custom (localai) | 8081 | ./.docker/data/services/localai |
| postgres | Relational Database | `postgres:16` | 5432 | ./.docker/data/services/postgres |
| timescaledb | Time‑Series Database | `timescale/timescaledb:latest-pg16` | 5433 | ./.docker/data/services/timescaledb |
| pgvector | Vector‑Enabled PostgreSQL | `pgvector/pgvector:pg16` | 5434 | ./.docker/data/services/pgvector |
| mkdocs | Documentation Site (Material for MkDocs) | `squidfunk/mkdocs-material:latest` | 8001 | `./docs`, `./mkdocs.yml` |
| redis | In‑Memory Cache | `redis:7‑alpine` | 6379 | ./.docker/data/services/redis |

> **Note:** Service activation is controlled by `.env` → `COMPOSE_FILE`. Add or remove service compose files in that single line (colon-separated) to customize the stack for your environment.

### Service Selection (Single Line)

The stack composition is defined by the `COMPOSE_FILE` variable in `.env`.

- Add a service: append `:services/<service>/docker-compose-<service>.yaml`
- Remove a service: delete its path from `COMPOSE_FILE`
- Keep `docker-compose.yml` as the first entry

### Compose Network Behavior

Service compose files do not declare an explicit shared network.

- The merged `COMPOSE_FILE` project creates and manages the shared default network.
- Services communicate using Docker DNS names (`service-name`) on that network.

### Documentation Service

The stack includes a **Material for MkDocs** service to maintain full project documentation.

- Service file: `services/mkdocs/docker-compose-mkdocs.yaml`
- Config file: `mkdocs.yml`
- Docs content: `docs/`
- Access URLs:
  - `http://localhost:8001`
  - `http://mkdocs.localhost` (when Traefik is enabled)

### Swagger UI + MkDocs Integration

Interactive API documentation is embedded directly into the MkDocs portal.

- Plugin: `mkdocs-swagger-ui-tag`
- API page: `docs/api-reference.md`
- OpenAPI source: `docs/specs/openapi.yaml`

This keeps architecture guides, runbooks, and live API testing in one place.

### Documentation-First Convention

- Keep implementation files free of explanatory inline comments.
- Put architecture, service behavior, and operational context in `docs/`.
- Put API contract details in `docs/specs/openapi.yaml`.

## 📋 Development Workflow

This project uses **Spec‑Driven Development (SDD)**:

1. **Read** `.spec/spec.md` for architectural constraints.
2. **Update** `.spec/tasks.md` with the new task.
3. **Implement** changes in the appropriate directory (`/services/`, `/src/`, `/scripts/`).
4. **Verify** changes work in the local Docker environment.
5. **Commit** with a conventional‑commit message.

All scripts that implement business logic must be placed under `/scripts/` (for bash) or `/src/` (for Python) and are expected to be run inside the **supervisord container**, which provides a unified Python environment and process monitoring.

## 🔐 Security & Data Persistence

- **Secrets** are stored in `.docker/secrets/` (git‑ignored).
- **Environment variables** are defined in `.env` (git‑ignored) with an `.env.example` template.
- **Model weights** and other large files reside in `.docker/data/services/ollama` (and other service directories under `.docker/data/services/`).
- **Service‑specific data** (databases, configuration) is kept in `.docker/data/services/<service‑name>/`.

## 📄 License

MIT – see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Please read the [Project Constitution](.spec/instructions.md) before proposing changes.  
Follow the SDD workflow and ensure all Docker Compose files are placed under `/services/`.  
GPU‑dependent services must include explicit GPU passthrough configuration.
