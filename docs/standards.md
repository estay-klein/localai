# Standards

## Documentation-First Policy

This repository follows a documentation-first policy:

- Source and infrastructure files avoid explanatory inline comments.
- Explanations are maintained in MkDocs pages.
- API behavior is maintained in OpenAPI specs used by embedded Swagger UI.

## Compose Composition Policy

Stack composition is controlled by `.env` `COMPOSE_FILE`.

- Add a service by appending its compose file path.
- Remove a service by deleting its compose file path.
- Keep `docker-compose.yml` as the first entry.

## Network Policy

Service-level compose files do not declare shared network blocks.

- Services rely on the default shared network created by the merged Compose project.
- Service discovery uses Docker DNS service names in that project network.

## Where to Document Changes

- Architecture decisions: `docs/architecture.md`
- Service behavior and configuration: `docs/services.md`
- Runbooks and operations: `docs/operations.md`
- API endpoints: `docs/specs/openapi.yaml` and `docs/api-reference.md`
