## Sales Insight Automator

AI-powered sales insight automation system that accepts a sales dataset, derives metrics with pandas, generates an executive summary using Groq Llama models, and emails the summary to a specified recipient. The project is structured as a production-style monorepo with a FastAPI backend, React (Vite + Tailwind) frontend, Docker images, docker-compose stack, and GitHub Actions CI.

### High-level architecture

- **Frontend**: React SPA built with Vite and Tailwind CSS.
  - Single-page upload flow.
  - Sends `multipart/form-data` (file + email) to the backend.
- **Backend**: FastAPI service.
  - `/health` for health checks.
  - `/api/upload` to handle uploads, validation, parsing, AI summary generation, and email delivery.
  - Uses pandas to compute metrics from CSV/XLSX sales data.
  - Uses Groq chat completion API to generate an executive summary.
  - Uses SMTP to send the summary via email.
- **Security and reliability**:
  - File extension and size validation.
  - Email validation and basic input sanitation.
  - In-memory rate limiting per IP (5 requests/min by default).
  - CORS configured to allow the configured frontend origin.
  - Centralized configuration via environment variables.
  - Structured logging for key events.
- **DevOps**:
  - Backend and frontend each have their own Dockerfile.
  - `docker-compose.yml` runs the full stack locally.
  - GitHub Actions CI builds and validates backend and frontend on pull requests.

### Repository layout

- `backend/`
  - `app/main.py`: FastAPI app entrypoint, CORS, `/health`, and router registration.
  - `app/config.py`: Pydantic-based settings (Groq, SMTP, rate limiting, CORS).
  - `app/routes/upload.py`: `/api/upload` endpoint wiring validation, parsing, AI, and email.
  - `app/services/parser.py`: pandas-based CSV/XLSX parsing and sales metric computation.
  - `app/services/ai_service.py`: Groq API integration for executive summary generation.
  - `app/services/email_service.py`: SMTP-based email delivery for the summary.
  - `app/security/validation.py`: file and email validation utilities.
  - `app/security/rate_limit.py`: simple in-memory rate limiting per IP.
  - `app/models/*.py`: Pydantic schemas for request/response and internal metrics.
  - `requirements.txt`: Python dependencies.
  - `Dockerfile`: Production backend image based on `python:3.11-slim` running Uvicorn.
- `frontend/`
  - `src/main.jsx`: React entry.
  - `src/App.jsx`: shell layout and heading.
  - `src/components/UploadForm.jsx`: CSV/XLSX file + email upload workflow with status states.
  - `src/services/api.js`: Axios client for `POST /api/upload`.
  - `src/styles.css`: Tailwind directives plus custom layout styles.
  - `package.json`: React, Vite, Axios, Tailwind, and build scripts.
  - `vite.config.js`: Vite React config.
  - `tailwind.config.js`, `postcss.config.js`: Tailwind + PostCSS setup.
  - `Dockerfile`: Multi-stage Node build and nginx static serving.
- `docker-compose.yml`: Orchestrates backend and frontend together for local runs.
- `.github/workflows/ci.yml`: CI pipeline for backend and frontend.
- `.gitignore`: Ignores build artifacts, node_modules, env files, and IDE state.

### Backend API design

#### `GET /health`

Simple health probe to check that the backend is running:

```json
{
  "status": "healthy"
}
```

#### `POST /api/upload`

Consumes `multipart/form-data`:

- `file`: CSV or XLSX file (max 5 MB).
- `email`: recipient email address for the summary.

Processing steps:

1. Validate file is `.csv` or `.xlsx`.
2. Validate file size does not exceed 5 MB (header and body check).
3. Validate email format and sanitize for unsafe characters.
4. Parse file into a pandas DataFrame.
5. Compute metrics:
   - Total revenue (sum of `Revenue`).
   - Best performing region (by revenue).
   - Best product category (by revenue).
   - Count of cancelled orders (`Status == "cancelled"`).
6. Call Groq chat completion API with metrics and an analyst-style prompt.
7. Send the generated summary to the recipient via SMTP.
8. Return a JSON success response:

```json
{
  "status": "success",
  "message": "Summary generated and emailed"
}
```

Error responses:

- `400` for validation errors (file type, size, email).
- `413` for oversized payloads.
- `429` when the per-IP rate limit is exceeded.
- `500` for unexpected internal errors.

### Security measures

- **Validation**:
  - File extension whitelist (`csv`, `xlsx`) and size limit (5 MB).
  - Email validation via Pydantic `EmailStr`.
  - Basic sanitation on email to avoid control characters and header injection.
- **Rate limiting**:
  - In-memory sliding window limit of 5 requests per minute per IP.
  - IP extraction respects `X-Forwarded-For` when present.
- **CORS**:
  - Allowed origins come from configuration:
    - `http://localhost:5173` by default for local dev.
    - Additional frontend URL via environment (`FRONTEND_URL`).
- **Secrets**:
  - No API keys or SMTP credentials are hardcoded.
  - Environment variables are used for Groq and SMTP configuration.
  - `.env` and `*.env` are ignored by Git.
- **Logging**:
  - Uses Python `logging` with configurable level.
  - Logs:
    - Upload received.
    - File parsed and metrics calculated.
    - AI summary generated.
    - Email sent or failures.

### Environment configuration

Create a `.env` file in the project root (not committed) with values like:

```bash
ENVIRONMENT=development
DEBUG=true

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

SMTP_HOST=smtp.your-provider.com
SMTP_PORT=587
SMTP_USER=your_smtp_user
SMTP_PASSWORD=your_smtp_password
SMTP_FROM_EMAIL=reports@your-domain.com

FRONTEND_URL=http://localhost:3000

RATE_LIMIT_REQUESTS_PER_MINUTE=5
```

The backend `Settings` class reads these via Pydantic environment support. The frontend consumes `VITE_API_BASE_URL` in its own environment when built (docker-compose sets this to `http://backend:8000` inside the network).

### Local development

#### Without Docker

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

The SPA can be reached at `http://localhost:5173`, which calls the backend at `http://localhost:8000`.

#### With Docker and docker-compose

At the repository root:

```bash
docker-compose up --build
```

This will:

- Build and run the FastAPI backend on port `8000`.
- Build and run the React frontend via nginx on port `3000`.

Access the app at `http://localhost:3000`.

### CI/CD pipeline

The GitHub Actions workflow in `.github/workflows/ci.yml` runs on pull requests to `main`:

- **Backend job**:
  - Checks out the repo.
  - Sets up Python 3.11 and installs `backend/requirements.txt`.
  - Imports `app.main` to catch import-level errors.
  - Builds the backend Docker image using the production Dockerfile.
- **Frontend job**:
  - Checks out the repo.
  - Sets up Node 22 and installs dependencies in `frontend`.
  - Runs `npm run build` with `VITE_API_BASE_URL` defined to ensure the SPA builds cleanly.

This mimics a simple production build validation pipeline suitable for branch protection rules.

### Git workflow and branching

Recommended branch structure:

- `main`: production-ready, deployable branch.
- `develop`: integration branch for upcoming features.
- `feature/*`: short-lived feature branches, such as:
  - `feature/upload-endpoint`
  - `feature/frontend-ui`
  - `feature/docker-setup`

Example commit messages aligned with conventional commits:

- `feat: initialize FastAPI backend`
- `feat: implement secure upload pipeline with Groq AI and email`
- `feat: add React frontend with Tailwind styling and upload workflow`
- `chore: add docker-compose stack and root gitignore`
- `ci: add GitHub Actions workflow for backend and frontend builds`
- `docs: add project README with architecture, security, and workflow details`

Suggested workflow:

1. Branch off `develop` for a feature.
2. Implement changes with small, focused commits.
3. Open a pull request into `develop`.
4. Let CI run and ensure it passes.
5. Squash or rebase commits as needed and merge.
6. Periodically fast-forward or merge `develop` into `main` for releases.

### Deployment guidance

This project is designed to map cleanly to:

- **Frontend → Vercel**:
  - Use the `frontend` directory as the project root.
  - Build command: `npm run build`.
  - Output directory: `dist`.
  - Ensure `VITE_API_BASE_URL` in Vercel environment points to the backend URL (for example, your Render service URL).
- **Backend → Render (or similar)**:
  - Use `backend` as the service root.
  - Build command: `pip install -r requirements.txt`.
  - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
  - Configure environment variables for Groq and SMTP as per your `.env`.

For container-based deployments, you can use the existing backend and frontend Dockerfiles and mirror the docker-compose configuration in your orchestration platform.

