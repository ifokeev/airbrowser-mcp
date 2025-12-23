# Contributing

## Development setup

- `docker compose up --build`
- Dashboard: `http://localhost:18080/`
- API docs: `http://localhost:18080/docs/`
- MCP: `http://localhost:18080/mcp`
- VNC: `http://localhost:18080/vnc/`

## Pull requests

- Keep changes focused and documented in `README.md` when user-facing.
- Do not commit secrets. Use `.env` locally (see `.env.example`).
- If you change REST endpoints, regenerate OpenAPI clients via `./scripts/generate_client.sh`.
- If you change REST endpoints, ensure generated clients are up to date before pushing: `./scripts/check_generated_clients.sh`.
