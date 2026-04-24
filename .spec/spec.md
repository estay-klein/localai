# Local & Open-Source AI Stack - Technical Specification

## 1. Project Overview
**Project Name:** LocalAI Stack  
**Version:** 1.0.0  
**Purpose:** A self‑hosted, modular AI inference and automation platform that runs entirely on local hardware, with strict data sovereignty and minimal external dependencies.

## 2. Architecture Principles
- **Container‑First:** All services run inside Docker containers orchestrated by Docker Compose.
- **Micro‑Services:** Each functional unit (LLM inference, UI, database, automation) is a separate, loosely coupled service.
- **Host‑Path Persistence:** Persistent data (models, service state, secrets) lives under a directory defined by the `LOCALAI_DATA` environment variable (default: `../.LocalAI`). This makes the stack portable across users and systems.
- **Supervisord Supervision:** All script execution inside the main application container is managed by `supervisord`.
- **Spec‑Driven Development:** Every change follows the SDD cycle (read spec → update tasks → implement → commit).

## 3. Service Matrix
| Service | Role | Image | Port | Data Path | GPU Support | Profile |
|---------|------|-------|------|-----------|-------------|---------|
| traefik | Reverse Proxy & Load Balancer | traefik:v3.3 | 80, 443 | – | No | – |
| ollama‑gpu | LLM Inference Engine (GPU) | ollama/ollama | 11435 | `${LOCALAI_DATA}/models/ollama` | Yes (NVIDIA) | gpu‑nvidia |
| ollama‑cpu | LLM Inference Engine (CPU) | ollama/ollama | 11434 | `${LOCALAI_DATA}/models/ollama` | No | cpu |
| openwebui‑gpu | Web UI for LLMs (GPU) | ghcr.io/open‑webui/open‑webui:main | 3031→8080 | `${LOCALAI_DATA}/services/openwebui` | Yes | gpu‑nvidia |
| openwebui‑cpu | Web UI for LLMs (CPU) | ghcr.io/open‑webui/open‑webui:main | 3030→8080 | `${LOCALAI_DATA}/services/openwebui` | No | cpu |
| n8n | Workflow Automation | n8nio/n8n:latest | 5678 | `${LOCALAI_DATA}/services/n8n` | No | – |
| postgres | Primary Database | postgres:16 | 5432 | `${LOCALAI_DATA}/data/postgres` | No | – |
| timescaledb | Time-Series Database | timescale/timescaledb:latest-pg16 | 5433→5432 | `${LOCALAI_DATA}/data/timescaledb` | No | – |
| pgvector | Vector-Enabled PostgreSQL | pgvector/pgvector:pg16 | 5434→5432 | `${LOCALAI_DATA}/data/pgvector` | No | – |
| redis | In‑Memory Cache | redis:7‑alpine | 6379 | `${LOCALAI_DATA}/data/redis` | No | – |
| qdrant | Vector Database | qdrant/qdrant:latest | 6333 | `${LOCALAI_DATA}/data/qdrant` | No | – |
| jaeger | Distributed Tracing | jaegertracing/all‑in‑one:latest | 16686 | – | No | – |
| grafana | Monitoring & Dashboards | grafana/grafana‑oss:latest | 3000 | `${LOCALAI_DATA}/data/grafana` | No | – |
| searxng | Privacy‑First Search | searxng/searxng:latest | 8080 | `${LOCALAI_DATA}/data/searxng` | No | – |
| flowise | Low‑Code AI Builder | flowiseai/flowise:latest | 3002 | `${LOCALAI_DATA}/data/flowise` | No | – |
| langflow | LangChain Visual Editor | langflowai/langflow:latest | 7860 | `${LOCALAI_DATA}/data/langflow` | No | – |
| jupyterhub | Jupyter Notebooks | jupyterhub/jupyterhub:latest | 8000 | `${LOCALAI_DATA}/data/jupyterhub` | No | – |
| localai | Local AI API (Go‑based) – open‑source models with fine‑tuning | localai/localai:latest | 8080 | `${LOCALAI_DATA}/models/localai` | Yes | – |
| localai‑dashboard | Dashboard & Monitoring (FastAPI+Jinja2) | custom build | 8081 | `${LOCALAI_DATA}/services/localai‑dashboard` | No | – |
| swagger‑ui | Unified API Documentation | swaggerapi/swagger‑ui | 8082 | – | No | – |
| mkdocs | Documentation Site (Material for MkDocs + embedded Swagger UI) | custom build (`services/mkdocs/Dockerfile`) | 8001→8000 | `./docs`, `./mkdocs.yml` | No | – |
| browseruse | Browser Automation | browseruse/browseruse:latest | 3003 | – | No | – |
| perplexica | Perplexity‑style Search | perplexica/perplexica:latest | 3004 | `${LOCALAI_DATA}/data/perplexica` | No | – |
| supervisord | Process Supervision | custom build | 9001 | `${LOCALAI_DATA}/scripts`, `${LOCALAI_DATA}/data` | No | – |

## 4. Network Topology
- **Compose Project Network:** Services rely on the default network created by the merged `COMPOSE_FILE` project.
- **Traefik** acts as the single entry point; all external traffic routes through it.
- **Internal service‑to‑service communication** uses Docker DNS (`service‑name`) on the shared Compose project network.
- **GPU‑capable services** are placed on the `gpu‑nvidia` Docker profile and require explicit device passthrough.
- **CPU‑only services** use the `cpu` profile. The stack supports only these two profiles (`cpu` and `gpu‑nvidia`).

## 5. Data Persistence Layout
```
${LOCALAI_DATA} (default: ../.LocalAI)
├── models/
│   ├── ollama/          # Ollama model weights (shared between CPU/GPU) – includes custom fine‑tuned models
│   └── localai/         # Open‑source models with fine‑tuning (exclusive to LocalAI API)
├── services/
│   ├── openwebui/       # OpenWebUI configuration & database
│   ├── n8n/             # n8n workflows & credentials
│   ├── ollama‑cpu/      # Ollama CPU runtime data
│   ├── ollama‑gpu/      # Ollama GPU runtime data
│   └── [service‑name]/  # Other service‑specific data
├── data/
│   ├── postgres/        # PostgreSQL database files
│   ├── timescaledb/     # TimescaleDB database files
│   ├── pgvector/        # pgvector PostgreSQL database files
│   ├── redis/           # Redis RDB/AOF files
│   ├── qdrant/          # Qdrant collections
│   └── [service]/       # Persistent data for other services
└── secrets/
    ├── .env             # Environment variables (git‑ignored)
    └── ssl/             # TLS certificates (if any)
```

**User‑Specific Customization:** Any configuration, data, or scripts that are specific to the user executing the stack (e.g., supervisord program configurations, service‑specific runtime data, user‑uploaded files) must be placed under `${LOCALAI_DATA}/services/<service‑name>/`. The project directory contains only generic, shareable service definitions (Dockerfiles, docker‑compose files, default configurations). This ensures that the project remains clean and portable across different users and environments.

**Model Storage Note:** Custom fine‑tuned models for Ollama must be placed in `${LOCALAI_DATA}/models/ollama/` to be accessible by both Ollama CPU and GPU services. The `ollama/` directory is shared between CPU and GPU variants to avoid duplication and ensure models are available regardless of which profile is active.

## 6. Environment Variables
All sensitive configuration is stored in `.env` files outside the repository (in `${LOCALAI_DATA}/secrets/`). Each service’s Docker Compose file references these variables via `${VAR_NAME}`. An `.env.example` is kept in the repository for documentation.

**Key variable:**
- `LOCALAI_DATA` – root directory for all persistent data (default: `../.LocalAI`). Override this to place data elsewhere (e.g., `/opt/LocalAI`). This variable ensures **portability**: the project can exist in `/home/$user/LocalAI` while all persistent volumes reside in a sibling folder (`../.LocalAI`). **No giant models should ever be placed inside the project directory** – they belong under `${LOCALAI_DATA}/models/`.
- `COMPOSE_FILE` – canonical stack composition list. This variable must include `docker-compose.yml` plus the selected service compose files under `/services/`. Users should enable or disable services by editing this single line (add/remove file paths separated by `:`), without changing core orchestration files.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` – credentials for the PostgreSQL service.
- `TIMESCALEDB_DB`, `TIMESCALEDB_USER`, `TIMESCALEDB_PASSWORD` – credentials for the TimescaleDB service.
- `PGVECTOR_DB`, `PGVECTOR_USER`, `PGVECTOR_PASSWORD` – credentials for the pgvector service.

## 7. Supervisord Configuration
- **Container:** `supervisord‑container` (built from `/services/supervisord/Dockerfile.supervisord`)
- **Role:** Hosts all Python/Bash scripts that implement business logic, agent workflows, and automation.
- **Supervisord Web GUI:** Enabled on port 9001 inside the container, exposed via Traefik at `supervisord.localhost`.
- **Unified Python Environment:** All scripts share a single virtual environment managed by `poetry` or `pipenv`.
- **Process Groups:** Each logical unit (e.g., `agent‑llm`, `data‑pipeline`, `monitoring`) is a separate supervisord group.

## 8. Development & Deployment Workflow
1. **Spec‑Driven Development:**
   - Read `.spec/spec.md` for architectural constraints.
   - Update `.spec/tasks.md` with the new task.
   - Implement changes in the appropriate directory (`/services/`, `/src/`, `/scripts/`).
   - Verify changes work in the local Docker environment.
   - Commit with a conventional‑commit message.
2. **Local Deployment:**
   - Run `docker‑compose up –detach` from the project root.
   - Services start in order defined by dependencies.
   - Traefik dashboard available at `traefik.localhost`.
3. **Production Considerations:**
   - Use Traefik middlewares for authentication, rate limiting, and SSL.
   - Ensure GPU‑capable hosts have the NVIDIA Container Toolkit installed.
   - Backup the `${LOCALAI_DATA}` directory regularly.

## 9. Technology Stack
- **Orchestration:** Docker Compose (v2+)
- **Reverse Proxy:** Traefik v3
- **LLM Engine:** Ollama (primary), LocalAI (alternative)
- **Automation:** n8n (self‑hosted)
- **Agent Framework:** Pi Agent (Python‑based)
- **Vector DB:** Qdrant
- **Relational DB:** PostgreSQL
- **Time-Series DB:** TimescaleDB
- **Vector SQL DB:** PostgreSQL + pgvector
- **Cache:** Redis
- **Monitoring:** Grafana + Jaeger
- **Documentation:** Material for MkDocs + embedded Swagger UI (`mkdocs-swagger-ui-tag`)
- **Scripting:** Python 3.11+ (PEP 8, type‑hinted), Bash (with `set -eou pipefail`)

## 10. Dashboard & Monitoring

### 10.1 LocalAI Dashboard
A custom web application built with **FastAPI + Jinja2** that serves as the primary user interface for the stack. The dashboard is developed as project‑specific code (not a standard Docker image) and resides in a dedicated directory at the project root (`/localai/`).

**Core Features:**
- **Home with Service Links:** Provides direct hyperlinks to all running stack services (Open WebUI, Traefik, Supervisord, etc.), opening each link in a new browser tab.
- **Real‑Time Service Monitoring:** Displays live status of all Docker containers (running/stopped), resource consumption (CPU, memory, GPU), and streaming logs.
- **Auto‑Refresh:** The dashboard updates its monitoring data in real time without requiring a page reload (using WebSockets or Server‑Sent Events).
- **Unified Management:** Acts as a central control panel for starting/stopping services (via Docker API) and viewing aggregated logs.

**Implementation Notes:**
- The application is packaged as a Docker service built from a custom `Dockerfile` inside the `/localai/` directory.
- It communicates with the Docker daemon via the Docker socket (mounted read‑only) to obtain container status and metrics.
- The dashboard is exposed via Traefik at `dashboard.localhost` (port 8081) and does not require a separate profile.

### 10.2 Swagger UI Integration
Swagger UI is integrated directly into the MkDocs site using the `mkdocs-swagger-ui-tag` plugin. This keeps narrative documentation and interactive API exploration under one documentation portal.

**Purpose:**
- Centralized API documentation for developers and integrators.
- Live testing of endpoints directly from the browser.
- Unified navigation with architecture and operations docs in one site.

**Deployment:**
- Provided by the MkDocs container (`services/mkdocs/docker-compose-mkdocs.yaml`).
- OpenAPI source path: `docs/specs/openapi.yaml`.
- Embedded page: `docs/api-reference.md`.

## 11. Compliance & Constraints
- **No `snap`/`flatpak`** – use `apt` or direct binaries.
- **No external cloud AI APIs** (OpenAI, Anthropic, etc.) unless explicitly requested by the user.
- **All Docker Compose files** must reside under `/services/`.
- **GPU‑dependent services** must include explicit GPU passthrough configuration.
- **Python/Bash** are the default languages; any other language requires explicit permission.
- **Portable paths** – all volume bindings must use `${LOCALAI_DATA}` to ensure the stack works for any user. The project must exist in `/home/$user/LocalAI` while all persistent volumes reside in a sibling folder (`../.LocalAI`). **No giant models inside the project directory** – they belong under `${LOCALAI_DATA}/models/`.
- **No Inline Explanatory Comments** – Explanations must be kept in MkDocs/OpenAPI documentation, not in service or source files.
- **No Explicit Shared Network Blocks in Service Compose Files** – Service-level compose files must rely on the merged `COMPOSE_FILE` project network.

---

*This specification is a living document. Update it whenever architectural decisions change.*

### Recent Changes (2026‑04‑20)
- **Network name standardized** to `LocalAI` (capitalized) in `docker-compose.yml` and spec.
- **Active variables removed** from `.env` (USER, PASS, MAIL, POSTGRES_*) as they are not currently used.
- **Enhanced portability clarity** in `.spec/` documents: explicit rule that giant models must not reside inside the project directory.
- **Path principles reinforced**: project lives in `/home/$user/LocalAI`, persistent data in sibling folder `../.LocalAI`.
- **Network topology** updated to reflect the new network name `LocalAI`.
- **User‑specific customization clarified**: Added explicit rule that any user‑specific configuration, data, or scripts must be placed under `${LOCALAI_DATA}/services/<service‑name>/`, keeping the project directory clean and portable.
- **COMPOSE_FILE approach implemented**: Added `COMPOSE_FILE` variable in `.env` to merge service files, ensuring relative paths resolve correctly from project root.
- **Model storage path fixed**: Updated configuration to ensure models are stored in `${LOCALAI_DATA}/models/ollama` (outside project) not inside project directory.
- **Redis and supervisord profiles removed**: Clarified that only `cpu` and `gpu-nvidia` profiles exist in the stack.