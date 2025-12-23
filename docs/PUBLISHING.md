# Publishing Generated Clients

This guide explains how to publish the auto-generated API clients to PyPI (Python) and npm (TypeScript).

## Overview

The Airbrowser project generates API clients from the OpenAPI specification:

- **Python client**: `airbrowser-client` on PyPI
- **TypeScript client**: `airbrowser-client` on npm

## Prerequisites

### Python (PyPI)

1. Create a PyPI account at https://pypi.org/account/register/
2. Create an API token at https://pypi.org/manage/account/token/
3. Set up authentication (choose one):

   **Option A: Environment variables (recommended for CI)**
   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-AgEIcH...  # Your API token
   ```

   **Option B: ~/.pypirc file**
   ```ini
   [pypi]
   username = __token__
   password = pypi-AgEIcH...

   [testpypi]
   username = __token__
   password = pypi-AgEIcH...  # Separate token for TestPyPI
   ```

### TypeScript (npm)

1. Create an npm account at https://www.npmjs.com/signup
2. Log in from command line:
   ```bash
   npm login
   ```

## Publishing Workflow

### Step 1: Regenerate Clients (if API changed)

If you've made changes to the API, regenerate the clients first:

```bash
# Start the server if not running
docker compose up -d browser-pool

# Regenerate clients
./scripts/generate_client.sh
```

### Step 2: Update Version

Before publishing, update the version number:

```bash
# Set version via environment variable
VERSION=1.0.1 ./scripts/generate_client.sh
```

Or manually edit:
- Python: `generated-clients/python/pyproject.toml` → `version`
- TypeScript: `generated-clients/typescript/package.json` → `version`

### Step 3: Test Build (Dry Run)

Always do a dry run first to ensure everything builds correctly:

```bash
# Test both
./scripts/publish_clients.sh --dry-run

# Test Python only
./scripts/publish_clients.sh python --dry-run

# Test TypeScript only
./scripts/publish_clients.sh npm --dry-run
```

### Step 4: Publish to Test Repositories (First Time)

For your first publish, use test repositories:

```bash
# Publish Python to TestPyPI
./scripts/publish_clients.sh python --test

# Verify installation works
pip install -i https://test.pypi.org/simple/ airbrowser-client
```

### Step 5: Publish to Production

Once verified, publish to production:

```bash
# Publish Python to PyPI
./scripts/publish_clients.sh python

# Publish TypeScript to npm
./scripts/publish_clients.sh npm

# Or publish both at once
./scripts/publish_clients.sh
```

## Scripts Reference

| Script | Description |
|--------|-------------|
| `./scripts/publish_clients.sh` | Main wrapper script for publishing |
| `./scripts/publish_python.sh` | Python/PyPI specific publishing |
| `./scripts/publish_npm.sh` | TypeScript/npm specific publishing |
| `./scripts/generate_client.sh` | Regenerate clients from OpenAPI spec |

### publish_clients.sh Options

```bash
./scripts/publish_clients.sh [target] [options]

Targets:
  all        Publish both Python and TypeScript (default)
  python     Publish Python client to PyPI
  npm        Publish TypeScript client to npm

Options:
  --dry-run  Build only, don't publish
  --test     Use TestPyPI for Python client
  --help     Show help message
```

## Configuration

### GitHub Repository

The GitHub user and repository are configured in `scripts/generate_client.sh`:

```bash
GITHUB_USER="${GITHUB_USER:-ifokeev}"
GITHUB_REPO="${GITHUB_REPO:-airbrowser-mcp}"
```

To override:
```bash
GITHUB_USER=myuser GITHUB_REPO=myrepo ./scripts/generate_client.sh
```

### Package Metadata

Package metadata is embedded during generation and stored in:

- **Python**: `generated-clients/python/pyproject.toml`
- **TypeScript**: `generated-clients/typescript/package.json`

## Post-Publish Verification

### Python

```bash
# Install from PyPI
pip install airbrowser-client

# Verify
python -c "import airbrowser_client; print(airbrowser_client.__version__)"
```

### TypeScript

```bash
# Install from npm
npm install airbrowser-client

# Verify
node -e "const client = require('airbrowser-client'); console.log(client);"
```

## Troubleshooting

### "Package already exists" Error

You cannot overwrite an existing version. Bump the version number and try again.

### Authentication Failed (PyPI)

- Verify your API token is correct
- Ensure `TWINE_USERNAME=__token__` (literal string, not your username)
- Check token has upload permissions

### Authentication Failed (npm)

```bash
# Re-login
npm logout
npm login

# Verify
npm whoami
```

### Build Errors

```bash
# Python: Check build tools
pip install --upgrade build twine

# TypeScript: Check Node version and reinstall
rm -rf node_modules
npm install
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Publish Clients

on:
  release:
    types: [published]

jobs:
  publish-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: ./scripts/publish_python.sh

  publish-npm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - name: Publish to npm
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: ./scripts/publish_npm.sh
```
