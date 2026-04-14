# Microservices Project

This project is a collection of microservices orchestrated using Docker Compose. The services are designed to work together to provide a comprehensive set of functionalities.

## Services

The following services are included in this project:

- **traefik**: A modern HTTP reverse proxy and load balancer that makes deploying microservices easy.
- **redis**: An in-memory data structure store, used as a database, cache, and message broker.
- **jaeger**: A distributed tracing system used for monitoring and troubleshooting microservices.
- **drawio**: A diagramming and charting tool.
- **excalidraw**: A virtual whiteboard tool for sketching hand-drawn diagrams.
- **searxng**: A privacy-respecting metasearch engine.
- **pgadmin**: A web interface for managing PostgreSQL databases.
- **wgeasy**: A simple web interface for managing WireGuard VPN configurations.
- **grafana**: An open-source platform for monitoring and observability.
- **crontabui**: A web interface for managing cron jobs.
- **ollama**: A tool for running and managing large language models.
- **openwebui**: A web interface for interacting with large language models.
- **localai**: A local AI service.
- **postgres**: A relational database management system.
- **qdrant**: A vector similarity search engine.
- **flowise**: A low-code platform for building AI applications.

Each service has its own `docker-compose.yaml` file located in its respective directory under the `services` directory.

## Network

The services communicate with each other using the `localai` network defined in the root `docker-compose.yml` file.

## Getting Started

To start the project, navigate to the root directory and run:

```bash
docker-compose up -d
```

To stop the project, run:

```bash
docker-compose down
```

For more details about each service, please refer to the README.md file located in each service's directory.