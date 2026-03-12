# CloudOps Dashboard

CloudOps Dashboard is a beginner-friendly **three-tier cloud engineering portfolio project**. It gives you a practical way to showcase containerization, service separation, reverse proxying, persistent storage, health checks, **role-based access control**, and AWS-ready deployment thinking without turning the project into an enterprise-sized system.

The application helps teams track cloud services, environments, owners, and operational health through a clean dashboard:

- **Presentation tier:** static frontend served by `nginx`
- **Application tier:** Python `FastAPI` API
- **Data tier:** PostgreSQL

## Why This Project Matters

Recruiters hiring for cloud engineer and junior DevOps roles often want to see more than scripts. They want evidence that you can work across the application and infrastructure boundary. This project demonstrates:

- building and containerizing a Python API
- connecting application services to a managed data tier
- exposing an app through a reverse proxy
- using environment variables for configuration
- creating health-aware multi-container deployments
- writing a clear deployment runbook for AWS EC2

## Features

- Role-based login for `admin` and `customer`
- Cloud service tracking with environment, owner, endpoint, and operational notes
- Summary cards for total, healthy, warning, and critical services
- Admin-only service creation, update, and deletion
- Customer read-only dashboard for service visibility
- Persistent PostgreSQL storage through Docker volumes
- Health checks for database and API containers
- Simple REST API that is easy to explain in interviews

## Architecture

```text
                ┌────────────────────────────┐
                │        Recruiter UI        │
                │      Browser on :8080      │
                └─────────────┬──────────────┘
                              │
                              ▼
                ┌────────────────────────────┐
                │   Frontend / Presentation  │
                │    nginx + static assets   │
                │    proxies /api requests   │
                └─────────────┬──────────────┘
                              │
                              ▼
                ┌────────────────────────────┐
                │ Application / Business     │
                │ Python FastAPI on :8000    │
                │ routes + service layer     │
                └─────────────┬──────────────┘
                              │
                              ▼
                ┌────────────────────────────┐
                │       Data / Storage       │
                │      PostgreSQL 16         │
                │   persisted by volume      │
                └────────────────────────────┘
```

## Project Structure

```text
.
├── backend
│   ├── app
│   ├── tests
│   ├── Dockerfile
│   └── requirements.txt
├── docs
├── frontend
│   ├── static
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
└── README.md
```

## Deep-Dive Docs

If you want long beginner-friendly explanations, read these files:

- `docs/PROJECT_CODE_EXPLAINED.md`
- `docs/DOCKER_AND_COMPOSE_EXPLAINED.md`
- `docs/AWS_DEPLOYMENT_STEP_BY_STEP.md`

## API Overview

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health endpoint for the API |
| `POST` | `/api/auth/login` | Login as admin or customer |
| `GET` | `/api/auth/me` | Return the current authenticated user |
| `GET` | `/api/services` | List tracked services for authenticated users |
| `POST` | `/api/services` | Create a tracked service for admins |
| `PUT` | `/api/services/{id}` | Update status, notes, or service details for admins |
| `DELETE` | `/api/services/{id}` | Remove a tracked service for admins |
| `GET` | `/api/summary` | Return dashboard summary counts for authenticated users |

Tracked statuses:

- `Healthy`
- `Warning`
- `Critical`

## Run Locally With Docker Compose

### 1. Prepare environment variables

```bash
cp .env.example .env
```

### 2. Start the stack

```bash
docker compose up --build
```

### 3. Open the app

- Frontend: `http://localhost:8080`
- API docs: `http://localhost:8000/docs`
- API health: `http://localhost:8000/health`

### 4. Demo login credentials

- Admin login: `admin` / `AdminPass123!`
- Customer login: `customer` / `CustomerPass123!`

Change these defaults in `.env` before you deploy anywhere public.

### 5. Stop the stack

```bash
docker compose down
```

To remove containers and keep database data:

```bash
docker compose down
```

To remove containers **and** wipe persisted PostgreSQL data:

```bash
docker compose down -v
```

## Run Backend Tests

If you want to run the tests outside Docker:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Manual Demo Flow

Use this exact sequence during a recruiter demo:

1. Open the dashboard and explain the three-tier architecture.
2. Log in as `customer` and show the read-only visibility view.
3. Log out and sign in as `admin`.
4. Add a service such as `API Gateway` in `Production`.
5. Show that it appears immediately in the list and updates the summary cards.
6. Change the service from `Healthy` to `Warning`.
7. Explain that the frontend talks to `nginx`, which proxies API traffic to FastAPI, which then enforces role-based access.
8. Restart the stack and show that PostgreSQL data persists.

## AWS EC2 Deployment Walkthrough

This project is intentionally designed to be easy to deploy on a single Linux VM, which is a strong beginner cloud engineer story.

### Recommended setup

- EC2 instance: Ubuntu 24.04 LTS
- Instance type: `t3.small` or higher
- Security group:
  - allow `22` from your IP
  - allow `80` from the internet
  - optionally allow `8080` during testing only

### Deployment steps

1. Launch an EC2 instance.
2. SSH into the instance.
3. Install Docker and Docker Compose plugin.
4. Copy the project to the VM using `git clone` or `scp`.
5. Create the environment file:

```bash
cp .env.example .env
```

6. Update `.env` with a stronger database password and a unique `APP_SECRET`.
7. Build and start the services:

```bash
docker compose up --build -d
```

8. Validate the deployment:

```bash
docker compose ps
curl http://localhost:8080
curl http://localhost:8000/health
```

9. Point a domain name to the EC2 public IP if needed.
10. As a later improvement, place `nginx` behind an AWS Application Load Balancer or add TLS with Let's Encrypt.

## What This Demonstrates

- Docker-based application packaging
- Multi-container application design
- Reverse proxy configuration with `nginx`
- Role-based authentication and access control
- Persistent storage with PostgreSQL volumes
- Health checks and service readiness
- Environment-driven configuration
- Basic deployment readiness on AWS EC2

## Troubleshooting

### Port `8080` or `8000` is already in use

Stop the conflicting process or change the published ports in `docker-compose.yml`.

### The API container fails to start

Check whether `.env` exists, whether `DATABASE_URL` matches the PostgreSQL credentials, and whether `APP_SECRET` is set.

### Frontend loads but API calls fail

Confirm the API container is healthy:

```bash
docker compose ps
docker compose logs api
```

### Database data did not persist

Do not use `docker compose down -v` unless you want to delete the Postgres volume.

## Resume / LinkedIn Bullets

You can adapt these directly:

- Built a three-tier CloudOps Dashboard using `FastAPI`, `PostgreSQL`, `nginx`, and Docker Compose to demonstrate service separation and deployment readiness.
- Implemented role-based login with separate admin and customer experiences to demonstrate secure access patterns in a containerized Python stack.
- Containerized a Python application stack with health checks, persistent storage, reverse proxy routing, and protected API endpoints for local and VM-based deployment.
- Authored an AWS EC2 deployment runbook for a multi-container application, highlighting environment configuration and operational validation.

## Next Improvements

If you want to extend this project later, good recruiter-relevant upgrades are:

- add Terraform for EC2 provisioning
- add CI/CD with GitHub Actions
- add metrics with Prometheus and Grafana
- deploy behind an ALB with TLS
