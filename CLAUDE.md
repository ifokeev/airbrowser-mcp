# CLAUDE.md - Important Project Information

## Critical Rules

### Package Management
**Always use `uv` instead of `pip` for Python package management:**
- Install packages: `uv pip install <package>`
- Run Python scripts: `uv run python3 <script>` (ensures correct environment)
- Run tools: `uvx <tool>` (e.g., `uvx ruff check src/`)
- Install from requirements: `uv pip install -r requirements.txt`

### Git Commits
**Use Conventional Commits format:** https://www.conventionalcommits.org/

Format: `<type>(<scope>): <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, semicolons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or fixing tests
- `chore`: Build process, dependencies, or tooling
- `ci`: CI/CD configuration

Examples:
- `feat(api): add browser screenshot endpoint`
- `fix(launcher): handle missing Chrome binary`
- `docs: update installation instructions`
- `chore(deps): upgrade seleniumbase to 4.32.0`

**Create separate logical commits with scope.** Do not bundle unrelated changes into one commit:
- Good: 3 commits for `feat(mcp)`, `docs`, `refactor(tests)`
- Bad: 1 commit with "feat(mcp): add feature and update docs and refactor tests"

**Do NOT add AI attribution to commits.** Never include:
- "🤖 Generated with Claude Code"
- "Co-Authored-By: Claude..."
- Any other AI/Claude attribution text

### Token Efficiency
**⚠️ MINIMIZE OUTPUT TO REDUCE TOKEN USAGE**

When running commands with verbose output (tests, builds, logs):
- Always pipe to `tail -n` to show only the final result/summary
- Example: `./scripts/run_tests.sh 2>&1 | tail -10`
- Never stream full test logs, build logs, or large file contents

### AGENTS.md
**AGENTS.md is for OpenAI Codex CLI, not project documentation.** Do not reference it as documentation in README or other files.

### Documentation
**⚠️ NEVER ADD DYNAMIC/MANUAL INFORMATION TO DOCS THAT WILL BECOME STALE**

When writing documentation, avoid:
- Hardcoded lists of files (use `ls` or `find` commands instead)
- Version history tables (tracked by git tags and package registries)
- Lists of test files (use `pytest --collect-only`)
- Lists of endpoints (reference Swagger docs at `/docs/`)

Instead, provide commands that dynamically discover information.

### Generated Clients Directory
**⚠️ NEVER MANUALLY EDIT FILES IN `generated-clients/` DIRECTORY OR TypeScript client files**

The `generated-clients/` directory contains auto-generated client libraries from the OpenAPI specification. 

**🔴 IMPORTANT: WHENEVER THE REST API CHANGES, YOU MUST REGENERATE THE CLIENTS**

**If REST API is modified (new endpoints, changed parameters, etc.):**
1. Modify the source API in `/src/airbrowser/server/api.py`
2. Restart the server: `docker compose restart browser-pool`
3. **ALWAYS regenerate the clients**: `./scripts/generate_client.sh`
4. For Python: Reinstall the client: `uv pip install -e generated-clients/python --force-reinstall`
5. For TypeScript: The client is generated into `generated-clients/typescript/`
6. Update tests and code to use the new client methods (never use raw HTTP calls)

**Python generated client import name**
- The generated Python client package name is `airbrowser_client` (see `scripts/generate_client.sh`).

### API Structure
- The API uses `/api/v1` prefix for all endpoints
- Swagger documentation is available at `http://localhost:8000/docs/`
- OpenAPI spec is available at `http://localhost:8000/api/v1/swagger.json`

### Testing
- Run tests: `./scripts/run_tests.sh` (skips slow/external tests by default)
- Fast re-runs: `./scripts/run_tests.sh -r` (reuses running containers)
- All tests: `./scripts/run_tests.sh -m ''` (includes slow/external site tests)
- Rebuild: `./scripts/run_tests.sh --build` (force rebuild containers)
- **Run specific tests by name**: `./scripts/run_tests.sh -r -k "test_name"` (e.g., `-k "test_list_tabs"`)
- **Run tests from specific file**: `./scripts/run_tests.sh -r -k "test_tabs"` (matches test_tabs.py)
- **Run specific test class**: `./scripts/run_tests.sh -r -k "TestListTabs"`
- See `docs/TESTING.md` for detailed testing guide
- The generated client automatically includes the `/api/v1` prefix

### Common Commands
```bash
# Restart the API server after changes
docker compose restart browser-pool

# Regenerate Python and TypeScript clients from OpenAPI spec
./scripts/generate_client.sh

# Install/reinstall the Python client
uv pip install -e generated-clients/python --force-reinstall

# Run fast tests (skips slow/external by default)
./scripts/run_tests.sh

# Fast re-runs (reuse containers)
./scripts/run_tests.sh -r

# Run specific tests
./scripts/run_tests.sh -k "test_health"

# Run ALL tests including slow/external
./scripts/run_tests.sh -m ''

# Force rebuild containers
./scripts/run_tests.sh --build

# Lint and format code
./scripts/lint.sh --fix --format

# Publish clients to PyPI/npm
./scripts/publish_clients.sh --dry-run  # Test first
./scripts/publish_clients.sh            # Publish
```

### Project Structure
```
airbrowser-mcp/
├── src/airbrowser/server/       # API server implementation
│   ├── app.py                   # Flask app factory
│   ├── models.py                # Data models
│   ├── routes/                  # API route handlers
│   ├── schemas/                 # OpenAPI schemas
│   ├── services/                # Business logic
│   ├── browser/                 # Browser control (launcher, commands)
│   ├── mcp/                     # MCP integration
│   └── vision/                  # Vision model integration
├── generated-clients/           # AUTO-GENERATED - DO NOT EDIT
│   ├── python/                  # Python client (PyPI: airbrowser-client)
│   └── typescript/              # TypeScript client (npm: airbrowser-client)
├── scripts/                     # Utility scripts
│   ├── generate_client.sh       # Regenerate clients from OpenAPI
│   ├── run_tests.sh             # Run test suite
│   ├── lint.sh                  # Lint and format code
│   └── publish_*.sh             # Publish clients to PyPI/npm
├── tests/                       # Test files
└── docs/                        # Documentation
```

### Development Workflow
1. Make API changes in `src/airbrowser/server/api.py`
2. Restart server: `docker compose restart browser-pool`
3. Regenerate clients: `./scripts/generate_client.sh`
4. Test Python client: `python tests/test_generated_client_complete.py`
5. TypeScript client will be automatically available in steam-auto-signup package

### TypeScript Client Usage
```typescript
import { BrowserApi, Configuration } from 'airbrowser-client';
import type { BrowserConfig, NavigateRequest } from 'airbrowser-client';

const configuration = new Configuration({
  basePath: 'http://localhost:8000/api/v1',
});

const browserApi = new BrowserApi(configuration);

// Create browser (UC + CDP mode enabled by default)
const browserConfig: BrowserConfig = { window_size: [1920, 1080] };
const response = await browserApi.createBrowser(browserConfig);

// Navigate
const browserId = response.data.data.browser_id;
const navigateRequest: NavigateRequest = { url: 'https://example.com', timeout: 60 };
await browserApi.navigateBrowser(browserId, navigateRequest);
```

### Important Notes
- The generated client uses Pydantic for validation
- All request bodies use the `payload` parameter name
- **IMPORTANT**: The client configuration must use `host="http://localhost:8000/api/v1"` (including /api/v1)
- When setting configuration.host, it replaces the entire base path, not just the domain

### CDP Mode Limitations
- **After activating CDP mode, `execute_script` stops working** - this is a known SeleniumBase limitation
- ChatGPT and similar protected sites require CDP mode but limit JavaScript execution
- Use typing, clicking, and screenshots instead of script execution after CDP activation
- See `docs/CDP_MODE_NOTES.md` for detailed information

### MCP Tools Architecture
**MCP tools are auto-generated from `BrowserOperations` class methods.**

- Source: `src/airbrowser/server/services/browser_operations.py`
- Every public method in `BrowserOperations` becomes an MCP tool
- Enhanced descriptions: `src/airbrowser/server/mcp/tool_descriptions.py` (optional overrides)
- Registration: `src/airbrowser/server/mcp/integration.py` auto-registers all methods

**To add a new MCP tool:**
1. Add a public method to `BrowserOperations` class
2. Add docstring (becomes default tool description)
3. Optionally add enhanced description to `tool_descriptions.py`
4. Regenerate docs: `./scripts/generate_docs.sh`

### Static Documentation
**Docs are auto-generated from source code to avoid staleness.**

```bash
# Regenerate docs (requires running server)
./scripts/generate_docs.sh
```

- Output: `landing/docs/index.html`
- Sources: OpenAPI spec + BrowserOperations + tool_descriptions.py
- Regenerate after API or MCP tool changes
