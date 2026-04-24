# LocalAI Stack Documentation

Welcome to the LocalAI Stack documentation.

This documentation is served by **Material for MkDocs** and is intended to be
the single source of truth for architecture, services, and operational
procedures.

Swagger UI is integrated directly into this site under `API Reference`.

## Quick Start

1. Ensure `services/mkdocs/docker-compose-mkdocs.yaml` is included in `.env` `COMPOSE_FILE`.
2. Start the stack:
   ```bash
   docker compose up -d
   ```
3. Open:
   - `http://localhost:8001`
   - `http://mkdocs.localhost` (if Traefik is running)
