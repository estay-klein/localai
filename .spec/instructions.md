# Project Constitution: Local AI Community Manager

## 1. Environment & Hardware Constraints
- **OS:** Pop!_OS (Ubuntu/Debian based).
- **GPU:** NVIDIA RTX 4060 (8GB VRAM). Prioritize CUDA and NVIDIA Container Toolkit for AI workloads.
- **Package Management:** STRICTLY FORBIDDEN to use `snap`. Use `apt`, `flatpak`, or direct binaries/scripts.
- **Docker Configuration:** - The `data-root` is located at `/home/yei/.docker-data`.
    - Always use Docker Compose for service orchestration.
    - Ensure GPU passthrough is configured in `docker-compose.yml`.

## 2. Development Philosophy
- **Privacy-First:** All LLM inference must be local via Ollama. No external AI APIs (OpenAI, Anthropic) unless explicitly requested for testing.
- **Spec-Driven Development:** Before writing code, the agent must check `.spec/spec.md` and update `.spec/tasks.md`.
- **Atomic Commits:** Every task completed should result in a clean Git commit.

## 3. Tech Stack Prefs
- **LLM Engine:** Ollama (Models: Llama 3, Qwen 2.5 Coder).
- **Agent Framework:** ElizaOS (Primary) or CrewAI.
- **Automation:** n8n (Self-hosted via Docker).
- **IDE:** VS Code with Roo Code / Aider.

## 4. File Organization
- Keep scripts in `scripts/`.
- Docker configurations in `docker/` or root `docker-compose.yml`.
- Documentation and planning in `.spec/`.