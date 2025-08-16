# UFC Q&A Chatbot with DevSecOps Practices

A FastAPI-based question-answering system about UFC champions and GOAT discussions, demonstrating modern DevSecOps practices and secure containerization.

## Features

- Question-answering API using Hugging Face Transformers
- Context-aware responses about UFC champions (2020-2025)
- Secure multi-stage Docker builds
- Comprehensive test suite with mocking
- CI/CD pipeline with security scanning
- DevSecOps best practices

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-chat-ai-dev-sec-ops.git
cd mcp-chat-ai-dev-sec-ops

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development

# Run the API locally
uvicorn app.chatbot:app --reload

# Run tests
python -m pytest -q
```

### Using Docker

```bash
# Build the container
docker build -t ufc-qa-bot .

# Run the container
docker run -p 8000:8000 ufc-qa-bot
```

## API Usage

```bash
# Example API call
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"text": "Who is considered the UFC GOAT?"}'
```

## Security Features

- Multi-stage Docker builds for minimal attack surface
- Dependency vulnerability scanning (pip-audit)
- Static code analysis (Bandit)
- Code quality checks (flake8)
- Automated security reporting in CI
- No credentials in container
- Minimal base images

## Development Workflow

1. Create feature branch
2. Make changes
3. Run tests locally: `python -m pytest`
4. Run security checks:
   ```bash
   bandit -r app
   pip-audit
   flake8
   ```
5. Create PR to trigger CI pipeline

## Project Structure

```
├── app/
│   ├── chatbot.py         # FastAPI application
│   └── context/           # UFC knowledge base
├── tests/
│   └── test_chat.py      # Test suite
├── .github/
│   └── workflows/         # CI pipeline
├── Dockerfile            # Multi-stage build
├── requirements.txt      # Production dependencies
└── requirements-dev.txt  # Development dependencies
```

## Testing

- Unit tests with pytest
- FastAPI TestClient for API testing
- Mocked transformer pipeline for fast tests
- CI integration via GitHub Actions

## Contributing

1. Fork the repository
2. Create feature branch
3. Follow security guidelines
4. Submit PR with tests

## License

MIT

## Security

Report vulnerabilities via GitHub Security tab or contact maintainers directly.

## Pull requests, CI and branch protection
- The repo includes a GitHub Actions workflow (.github/workflows/ci.yml) named "CI" that runs on push and pull_request.
- When a PR is opened the "CI" job runs tests, linting and security scans (bandit, pip-audit).  
- Configure branch protection on your main branch to require the "CI" status check to pass and to require PR reviews — this will block merging if any checks fail or tests fail.

Quick steps (GitHub web UI)
1. Go to the repository → Settings → Branches → Branch protection rules → Add rule.
2. Set "Branch name pattern" to `main` (or your protected branch).
3. Enable "Require status checks to pass before merging" and select `CI`.
4. (Optional) Enable "Require pull request reviews before merging" and set required approvals.
5. Save changes.

Example using GitHub CLI (replace OWNER and REPO, requires gh auth):
```shell
gh api \
  -X PUT /repos/OWNER/REPO/branches/main/protection \
  -F required_status_checks='{"strict":true,"contexts":["CI"]}' \
  -F enforce_admins=true \
  -F required_pull_request_reviews='{"required_approving_review_count":1}'
```

Result: any PR will trigger the CI workflow and GitHub will block merges to the protected branch until the CI checks and required reviews