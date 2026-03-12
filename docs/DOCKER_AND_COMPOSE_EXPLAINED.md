# Docker And Docker Compose Explained For This Project

This file explains:

- what Docker is
- why this project uses Docker
- how the Dockerfiles work
- how `docker-compose.yml` works
- how to explain all of this in simple words

The goal is to help you understand the container side of the project clearly.

## 1. Very simple meaning of Docker

Docker helps us package an application with what it needs to run.

Think of Docker like a box.

Inside that box, we keep:

- the code
- the runtime
- the dependencies
- the startup command

That box is called a container.

Without Docker, a project may work on one machine but fail on another machine.
Docker helps reduce that problem.

## 2. Why Docker is useful in this project

This project has multiple parts:

- frontend
- backend
- database

Each part has different needs.

For example:

- backend needs Python packages
- frontend needs Nginx
- database needs PostgreSQL

Docker helps us run each part in its own clean environment.
This is a good cloud engineering pattern.

## 3. What Docker Compose does

Docker Compose helps run multiple containers together.

In this project, Compose starts:

- `frontend`
- `api`
- `db`

Without Compose, you would need many long Docker commands.
With Compose, one file describes everything.

## 4. Project containers

### Frontend container

What:

- serves the web page

Why:

- users need a browser-based interface

How:

- Nginx serves static files
- Nginx also proxies `/api` requests to the backend

### API container

What:

- runs FastAPI

Why:

- backend logic should be separate from frontend and database

How:

- Python runs `uvicorn`
- FastAPI handles routes and auth

### Database container

What:

- runs PostgreSQL

Why:

- app data and users need persistent storage

How:

- Postgres stores tables and records
- a Docker volume keeps data safe across container restarts

## 5. Backend Dockerfile explained

File:

`backend/Dockerfile`

### `FROM python:3.12-slim`

What:

- starts from a Python image

Why:

- backend needs Python to run

Why `slim`:

- smaller image
- less extra stuff

### `WORKDIR /app`

What:

- sets the working folder inside the container

Why:

- commands should run from one known location

### `ENV PYTHONDONTWRITEBYTECODE=1`

What:

- tells Python not to create `.pyc` files

Why:

- keeps the container cleaner

### `ENV PYTHONUNBUFFERED=1`

What:

- tells Python to show logs immediately

Why:

- very helpful for Docker logs

### `COPY requirements.txt .`

What:

- copies dependency file into the container

Why:

- Docker must know what Python packages to install

### `RUN pip install --no-cache-dir -r requirements.txt`

What:

- installs Python dependencies

Why:

- FastAPI, SQLAlchemy, psycopg, pytest and others are needed

Why `--no-cache-dir`:

- avoids keeping unnecessary pip cache
- makes image smaller

### `COPY app ./app`

What:

- copies the backend source code

Why:

- now the container has the real app code

### `EXPOSE 8000`

What:

- documents that the container uses port 8000

### `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`

What:

- starts the FastAPI app

Why host `0.0.0.0`:

- because the server must listen on all interfaces inside the container

## 6. Frontend Dockerfile explained

File:

`frontend/Dockerfile`

### `FROM nginx:1.27-alpine`

What:

- starts from an Nginx image

Why:

- frontend is a static site
- Nginx is very good at serving static files

### `COPY nginx.conf /etc/nginx/conf.d/default.conf`

What:

- replaces the default Nginx config

Why:

- we want custom behavior
- especially proxying `/api` to the backend

### `COPY static /usr/share/nginx/html`

What:

- copies HTML, CSS, and JS files into the default web folder

Why:

- Nginx serves files from there

### `EXPOSE 80`

What:

- documents the HTTP port

## 7. `frontend/nginx.conf` explained

This file is small but important.

### What it does

- serves the frontend files
- forwards API requests to the backend
- forwards the health request

### Why it matters

It lets the user access:

- the page
- the API through the same frontend entry point

This is called a reverse proxy pattern.

That is a useful cloud and DevOps idea.

## 8. `docker-compose.yml` explained

This is the file that starts the full application.

Think of it as the conductor of the project.

It tells Docker:

- which services exist
- which ports to use
- which env vars to load
- what order services depend on
- which volume stores database data

## 9. Compose service: `db`

### What it is

The PostgreSQL service.

### Important parts

#### `image: postgres:16-alpine`

Uses the official PostgreSQL image.

#### `env_file: .env`

Reads environment variables from `.env`.

#### `environment`

Sets database name, user, and password.

#### `volumes`

Uses `db-data:/var/lib/postgresql/data`

Why:

- this keeps data even if the container stops or restarts

#### `healthcheck`

Uses `pg_isready`

Why:

- database must be ready to accept connections

## 10. Compose service: `api`

### What it is

The FastAPI backend service.

### Important parts

#### `build: ./backend`

Builds the image from `backend/Dockerfile`.

#### `env_file: .env`

Loads variables like:

- `DATABASE_URL`
- `APP_SECRET`
- admin and customer credentials

#### `depends_on`

The API waits for the database health check.

Why:

- backend should not start talking to Postgres before Postgres is ready

#### `ports: "8000:8000"`

Why:

- you can open FastAPI docs from your machine

#### `healthcheck`

The API checks its own `/health` endpoint.

Why:

- Docker can know whether the backend is healthy

## 11. Compose service: `frontend`

### What it is

The Nginx frontend service.

### Important parts

#### `build: ./frontend`

Builds the frontend image from its Dockerfile.

#### `depends_on`

Waits for the API to become healthy.

Why:

- if frontend starts before backend is ready, API requests may fail during startup

#### `ports: "8080:80"`

Why:

- you open `http://localhost:8080`

## 12. Compose volume explained

At the bottom:

```yaml
volumes:
  db-data:
```

This is a named Docker volume.

Why it exists:

- to keep PostgreSQL data outside the life of a single container

If you restart containers:

- your data stays

If you remove the volume:

- your data goes away

That is why `docker compose down -v` is more destructive than `docker compose down`.

## 13. `.env` and `.env.example`

These files store configuration values.

Important values:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `APP_SECRET`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `CUSTOMER_USERNAME`
- `CUSTOMER_PASSWORD`

Why this matters:

- config should be easy to change without editing code

This is a very important real-world practice.

## 14. What happens when you run `docker compose up --build`

Step by step:

1. Docker reads `docker-compose.yml`
2. Docker builds backend image
3. Docker builds frontend image
4. Docker pulls PostgreSQL image if needed
5. Docker creates network
6. Docker creates volume for database
7. Docker starts database
8. Docker waits for DB health check
9. Docker starts API
10. Docker waits for API health check
11. Docker starts frontend

This is useful because it shows that startup order matters.

## 15. Why health checks are important

Many beginners think:

> If the container is running, the app is ready.

That is not always true.

A container can be running but still not ready.

Examples:

- database still starting
- API server started but cannot connect to DB yet
- app has internal error

Health checks give a better answer.

## 16. Why reverse proxy matters

Nginx in front of the backend is a good design choice.

Why:

- static files are served efficiently
- API calls can go through one public entry point
- backend can stay behind frontend proxy
- this pattern is common in real deployment

## 17. Why separate containers are better than one big container

A beginner may ask:

> Why not put frontend, backend, and database in one container?

Because separate containers are cleaner.

Each container should ideally have one main responsibility.

This gives benefits:

- easier debugging
- easier scaling
- easier replacement
- cleaner architecture

## 18. How to explain Docker part in interview

You can say:

> I used Docker to package the frontend and backend separately, and Docker Compose to orchestrate the frontend, API, and PostgreSQL database together. I also added health checks and a persistent volume so the stack behaves more like a real deployment.

## 19. Common beginner doubts

### Is Docker the same as a virtual machine?

No.
They are similar in idea because both isolate environments, but Docker containers are lighter.

### Why do we still need Docker Compose?

Because one project has many containers.
Compose makes it easier to manage them together.

### Why do we expose ports?

So your local machine can reach services inside containers.

### Why do we need both Dockerfile and docker-compose.yml?

Because they solve different problems.

- Dockerfile = how to build one image
- Compose = how to run many services together

## 20. Final summary

The Docker side of this project is strong because it shows more than just "I can run a container."

It shows:

- separate frontend and backend containers
- a database container
- environment-based config
- health checks
- reverse proxy
- persistent storage
- multi-service orchestration

These are exactly the kinds of ideas that help a beginner move toward cloud engineering work.
