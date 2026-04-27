# Project Constitution: Local & Open‑Source AI Stack

## Project Tree
LocalAI-Stack/ # Repository root (tracked source)
├── .localai/ # [git‑ignored] User data, models, secrets, persistent volumes
│ ├── data/
│ │ └── services/ # Runtime data per service
│ │ ├── ollama‑gpu/
│ │ ├── ollama‑cpu/
│ │ ├── openwebui‑gpu/
│ │ ├── openwebui‑cpu/
│ │ ├── n8n/
│ │ ├── postgres/
│ │ ├── timescaledb/
│ │ ├── pgvector/
│ │ ├── redis/
│ │ ├── grafana/
│ │ ├── searxng/
│ │ ├── stable-diffusion/
│ │ ├── comfyui/
│ │ ├── invokeai/
│ │ ├── flowise/
│ │ ├── langflow/
│ │ ├── jupyterhub/
│ │ ├── localai/
│ │ ├── perplexica/
│ │ └── supervisord/
│ ├── models/ # Large model files (shared between CPU/GPU variants)
│ │ └── ollama/
│ └── secrets/ # Environment secrets (git‑ignored)
│ ├── .env # Actual credentials (never committed)
│ └── ssl/ # TLS certificates (optional)
├── .repo/ # [git‑ignored] Third‑party repositories
├── .spec/ # [git‑ignored] User spec overrides (optional)
├── docs/ # MkDocs documentation source (tracked)
├── localai/ # Dashboard application & core logic (tracked)
│ ├── agents/
│ ├── assets/
│ ├── config/ # Default configuration templates
│ ├── scripts/ # Scripts managed by supervisord
│ ├── utils/
├── services/ # Docker definitions (tracked)
│ └── <service>/ # Each service’s docker‑compose.yaml, Dockerfile, etc.
├── .env.example # Environment template (tracked)
├── .gitignore
├── docker-compose.yaml # Root compose file (includes services)
├── LICENSE
├── mkdocs.yml
└── Readme.md


**Mirror directories** (`localai/` ↔ `.localai/`, etc.) enforce separate ownership: the tracked folder contains distributable source; the hidden folder contains user‑specific state (git‑ignored). This allows clean upstream updates without overwriting local data.

---

## 1. Preamble & Purpose

This document is the supreme law of the **LocalAI Stack** project. It defines the immutable rules for architecture, development, and operation. Every design choice, line of code, configuration file, or deployment script must conform to it.

**Scope**  
- Governs the entire repository and its ecosystem of services, scripts, documentation, and local deployment.  
- Overrides any personal preference, external tutorial, or non‑project practice.  
- Binding for all agents (human and automated) involved in development.  
- Complements the detailed technical specification in `.spec/spec.md`; in any conflict, this Constitution takes precedence.

---

## 2. Fundamental Principles (Non‑Negotiable)

### 2.1 Data Sovereignty & Local‑First Operation
- **Local default**: all inference runs on local hardware; sensitive data never leaves the machine without explicit user consent.  
- **No unsolicited external API calls** to third‑party LLM providers (OpenAI, Anthropic, etc.) unless the user deliberately configures such access as an additional feature.  
- The stack is fully functional without internet connectivity, yet supports optional remote models under user‑controlled settings, preserving data sovereignty and privacy.

### 2.2 Mirrored Directory Isolation
- The project enforces strict separation between **distributable source** and **user‑specific state** via mirrored folders:  
  - `name/`  → base content tracked in Git (templates, default configurations).  
  - `.name/` → user‑owned, git‑ignored (real data, models, secrets, personal services).  
- Key pairs: `localai/` ↔ `.localai/`, `services/` ↔ `.services/` (optional), `spec/` ↔ `.spec/` (optional).  
- This pattern allows the main repository to be updated from upstream without overwriting local configurations or user data.

### 2.3 Clean Containerization & Strict Orchestration
- All runtime components run in minimal Docker containers, built from official images or custom Dockerfiles in `/services/<service>/`.  
- **Docker Compose v2** (`docker compose`) is the sole orchestration mechanism.  
- Every service‑level `docker-compose.yaml` resides **mandatorily** under `/services/`; they are integrated into the project via `include` in the root `docker-compose.yaml`.  
- No service file may declare an explicit shared network; all containers rely on the default network created by the root Compose project.

### 2.4 Spec‑Driven Development (SDD)
Every change follows this cycle:  
1. **Read** `.spec/spec.md` and this Constitution to understand constraints.  
2. **Update** `.spec/tasks.md` with the new task.  
3. **Implement** adhering to all rules.  
4. **Commit** atomically using the *Conventional Commits* standard.  
5. **`Readme.md`** is updated **only when explicitly requested**.

### 2.5 External Documentation & Self‑Descriptive Code
- **Explanatory comments are forbidden** inside service definitions, Dockerfiles, scripts, or source files.  
- All explanations, runbooks, architectural decisions, and API documentation live in:  
  - The MkDocs site (`/docs`) built with Material for MkDocs.  
  - OpenAPI specifications consumed by the integrated Swagger UI.  
- Code must be self‑documenting through clear naming and strong typing.

### 2.6 Microservices & Radical Modularity
- Each functional unit (inference, UI, database, automation) is a separate, loosely‑coupled service.  
- Business logic and agent code (`localai/`) is split into small, independent modules to facilitate maintenance, testing, and incremental improvement.

### 2.7 Unified Process Supervision
- All long‑running user scripts (workers, agents, watchers) run inside a dedicated **supervisord** container.  
- `supervisord` manages all processes inside that container, with its Web GUI enabled for visual monitoring.  
- Custom user scripts that need supervision must reside in the shared Python environment of that container (i.e., under `localai/scripts/` and mounted accordingly).

---

## 3. Infrastructure & System Constraints
- **Operating System:** Pop!_OS (Debian/Ubuntu‑based).  
- **GPU Architecture:** NVIDIA RTX 4060 (8 GB VRAM). Prioritize CUDA‑accelerated libraries and the NVIDIA Container Toolkit.  
- **Package Management:** **STRICTLY FORBIDDEN** to use `snap` or `flatpak`. Use `apt` for system packages, or direct binaries/custom shell scripts.  
- **Docker Infrastructure:** Docker Compose v2 only. All `docker-compose.yaml` files are placed under `/services/`; the root `docker-compose.yaml` pulls them via `include`.  
- **GPU Services:** Every GPU‑dependent service must include explicit device passthrough (`deploy.resources.reservations.devices`).  
- **Profiles:** Only two profiles exist: `cpu` and `gpu-nvidia`.

---

## 4. Data Persistence & Security
- **Persistent Root:** All runtime data, models, and secrets live under `.localai/`, which is **git‑ignored**.  
  - Service‑specific data: `.localai/data/services/<service>`.  
  - Ollama models: `.localai/models/ollama/`.  
  - Stable Diffusion models: `.localai/data/services/stable-diffusion/` (shared with ComfyUI and InvokeAI).  
  - Secrets: `.localai/secrets/.env` (the template `.env.example` is tracked at the project root).  
- **No environment variable** is required to locate the persistent root; the relative path is fixed to `.localai/`.  
- **Portability:** The entire project root (including `.localai`, `.repo`, `.spec`) can be backed up or moved as a self‑contained unit.  
- **User‑Specific Customization:** Any configuration, data, or scripts that are user‑specific (supervisord program definitions, runtime data, uploaded files) must be placed under `.localai/`, never in tracked directories.  
- **Local Secrets:** Sensitive credentials never enter version control. The actual `.env` resides in `.localai/secrets/`. The root `.env.example` documents all required variables.  
- **Databases:** The stack uses **PostgreSQL** (with TimescaleDB extension) and **pgvector**. Native web administration (pgAdmin, optional Adminer) is provided.

---

## 5. Architecture & Execution Strategy
- **Minimal Images:** All services use clean, minimal Docker images. Custom builds are defined in `/services/<name>/`.  
- **Supervisord Container:** The `supervisord` service (built from `/services/supervisord/Dockerfile`) hosts all Python/Bash business logic. Inside it, `supervisord` manages multiple process groups. The supervisor web UI is accessible via Traefik.  
- **Unified Python Environment:** All scripts running inside the supervision container share a single virtual environment (managed by `poetry` or `pipenv`).  
- **Microservices Decoupling:** Each script is a small, focused module; heavy functions and classes are split into separate files under `localai/`.  
- **Single‑Line Service Selection:** Adding a new service means placing its `docker-compose` file in `/services/<name>/` and referencing it via `include` in the root compose file.  
- **Documents‑First:** No explanatory comments in code or configuration; all knowledge lives in MkDocs and OpenAPI specs.

---

## 6. Development Philosophy
- **Local‑First Inference:** No external LLM API calls unless explicitly configured by the user.  
- **Spec‑Driven Workflow:** Always read `.spec/spec.md` and update `.spec/tasks.md` only when asked. Only update `Readme.md` when asked.  
- **Version Control:** Atomic commits using Conventional Commits.  
- **Unified Documentation:** Swagger UI embeds OpenAPI docs into the MkDocs site. OpenAPI specifications are required for any new HTTP API.  
- **Central Dashboard:** The LocalAI Dashboard (`localai.localhost`) provides a real‑time canvas for widgets, service links, observability, and configuration. New services must be discoverable by the dashboard (via Docker socket or health endpoints).  
- **Language Policy:** Default languages are **Python** (3.11+, PEP 8, type‑hinted) and **Bash** (with `set -eou pipefail`). Any other language requires explicit permission.

---

## 7. Technology Stack & Tooling (Fixed)
- **Inference Engine:** Ollama (preferred models: `llama3`, `qwen2.5-coder`).  
- **Logic & Agents:** Pi Agent Framework.  
- **Workflow Automation:** n8n (self‑hosted).  
- **Reverse Proxy:** Traefik v3.  
- **Databases:** PostgreSQL + TimescaleDB + pgvector; Redis for caching.  
- **Monitoring:** Grafana, Jaeger.  
- **Documentation:** Material for MkDocs with embedded Swagger UI (`mkdocs-swagger-ui-tag`).  
- **Dashboard:** LocalAI (FastAPI + Jinja2), custom‑built in `/localai`.  
- **Code Environment:** VS Code with Aider integration.

---

## 8. Filesystem Organization (Tracked Directories)
- `/services/` – All Docker‑related definitions; each subdirectory contains `docker-compose.yaml` plus any required `Dockerfile`.  
- `/localai/` – Dashboard app, agents, assets, utility code, and script skeletons. The `data/` subdirectory contains only templates; actual data goes in `.localai/data/`.  
- `/docs/` – All MkDocs markdown files and OpenAPI specs.  
- `/.spec/` – (Tracked) Core specifications and task tracking; the ignored `.spec/` may hold local overrides.

---

## 9. Prohibitions (Zero Tolerance)
- Using `snap` or `flatpak` for package management.  
- Calling external cloud AI APIs without explicit user authorization.  
- Adding explanatory comments inside code, Dockerfiles, or compose files.  
- Declaring explicit networks in service‑level compose files.  
- Writing application logic in languages other than Python/Bash without prior approval.  
- Placing `docker-compose.yaml` files outside the `/services/` tree.  
- Storing persistent data, models, or secrets anywhere other than the git‑ignored `.localai/` directory.  
- Modifying `Readme.md` without a direct request.

---

## 10. Agent Implementation Directive
> Before generating any code, review this Constitution. Any proposal that violates these principles must be rejected.  
> Ensure all composition changes update the root `docker-compose.yaml` includes and that all persistent data targets `.localai/`.  
> Keep all explanatory content in MkDocs/OpenAPI; never pollute source files with comments.  
> Do not proceed until `.spec/tasks.md` accurately reflects the current task. Only update `Readme.md` when explicitly instructed.

---
*This Constitution completely replaces any previous version. The SDD cycle remains the mandatory workflow: read spec, update tasks, implement, commit atomically.*
