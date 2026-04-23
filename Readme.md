# Local & Open-Source AI Stack

A self‑hosted, modular AI inference and automation platform that runs entirely on local hardware, with strict data sovereignty and minimal external dependencies.  
This project follows a **Spec‑Driven Development (SDD)** workflow and adheres to the [Project Constitution](.spec/instructions.md).

## 🏗️ Architecture

The stack is built around **Docker Compose** micro‑services, each running in its own container, orchestrated via a central `docker‑compose.yml` file.  
Key architectural principles:

- **Container‑First:** All services run inside Docker containers.
- **Host‑Path Persistence:** Persistent data lives under `.LocalAI/` directory relative to the project root (configurable via `LOCALAI_DATA` environment variable).
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
├── docker/                   # Base Dockerfiles & environment templates
├── scripts/                  # Maintenance & automation bash scripts
├── src/                      # Core application logic (modular Python)
│   └── pipes/                # Pipe implementations (e.g., n8n_pipe)
├── assets/                   # Static assets (logos, etc.)
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
   mkdir -p ~/.LocalAI/{models,services,data,secrets}
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
   - Ollama API: `http://localhost:11434` (CPU) or `:11435` (GPU)

## 🔧 Core Services

| Service | Role | Image | Port | Host Data Path |
|---------|------|-------|------|----------------|
| traefik | Reverse Proxy | `traefik:latest` | 80, 443 | – |
| ollama‑cpu | LLM Inference (CPU) | `ollama/ollama` | 11434 | `~/.LocalAI/models/ollama` |
| ollama‑gpu | LLM Inference (GPU) | `ollama/ollama` | 11435 | `~/.LocalAI/models/ollama` |
| openwebui‑cpu | Web UI (CPU) | `ghcr.io/open‑webui/open‑webui:main` | 3030 | `~/.LocalAI/services/openwebui` |
| openwebui‑gpu | Web UI (GPU) | `ghcr.io/open‑webui/open‑webui:main` | 3031 | `~/.LocalAI/services/openwebui` |
| supervisord | Process Supervisor | Custom (see `docker/Dockerfile.supervisord`) | 9001 | `~/.LocalAI/scripts` |
| redis | In‑Memory Cache | `redis:7‑alpine` | 6379 | `~/.LocalAI/data/redis` |
| *[many more]* | … | … | … | … |

> **Note:** The project includes placeholders for many additional services (PostgreSQL, Qdrant, n8n, Jaeger, Grafana, etc.). Uncomment the corresponding lines in `docker‑compose.yml` and create the missing service definitions under `/services/` to enable them.

## 📋 Development Workflow

This project uses **Spec‑Driven Development (SDD)**:

1. **Read** `.spec/spec.md` for architectural constraints.
2. **Update** `.spec/tasks.md` with the new task.
3. **Implement** changes in the appropriate directory (`/services/`, `/src/`, `/scripts/`).
4. **Verify** changes work in the local Docker environment.
5. **Commit** with a conventional‑commit message.

All scripts that implement business logic must be placed under `/scripts/` (for bash) or `/src/` (for Python) and are expected to be run inside the **supervisord container**, which provides a unified Python environment and process monitoring.

## 🔐 Security & Data Persistence

- **Secrets** are stored in `~/.LocalAI/secrets/` (outside the repository).
- **Environment variables** are defined in `.env` (git‑ignored) with an `.env.example` template.
- **Model weights** and other large files reside in `~/.LocalAI/models/`.
- **Service‑specific data** (databases, configuration) is kept in `~/.LocalAI/services/` and `~/.LocalAI/data/`.

## 📄 License

MIT – see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Please read the [Project Constitution](.spec/instructions.md) before proposing changes.  
Follow the SDD workflow and ensure all Docker Compose files are placed under `/services/`.  
GPU‑dependent services must include explicit GPU passthrough configuration.