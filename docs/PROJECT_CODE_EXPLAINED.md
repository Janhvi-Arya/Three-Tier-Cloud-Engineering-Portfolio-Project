# CloudOps Dashboard Code Explained

This file explains the code of the project in simple words.

The goal is not only to tell you what the code does.
The goal is also to help you understand:

- what each file is doing
- why that file is needed
- how all files work together
- how to explain the project to another person

If you are a beginner, read this file slowly from top to bottom.

## 1. Big picture first

This project is a three-tier application.

That means it has three main parts:

1. Frontend or presentation tier
2. Backend or application tier
3. Database or data tier

In this project:

- the frontend is the web page that the user sees
- the backend is the Python API that handles logic
- the database stores service data and login users

The user opens the frontend in the browser.
The frontend talks to the backend API.
The backend talks to PostgreSQL.

So the flow is:

`Browser -> Nginx frontend -> FastAPI backend -> PostgreSQL`

This is already a strong project for a beginner cloud engineer because it shows:

- web application flow
- backend API design
- database usage
- authentication
- role-based access control
- Docker usage
- deployment thinking

## 2. Folder structure in simple words

Important folders:

```text
backend/
  app/
  tests/
frontend/
  static/
docker-compose.yml
README.md
docs/
```

What each part means:

- `backend/app/` contains the real backend code
- `backend/tests/` contains test files
- `frontend/static/` contains the web page files
- `docker-compose.yml` starts the whole project
- `README.md` explains the project at a high level
- `docs/` contains deep explanations like this file

## 3. Backend code overview

The backend is written in Python using FastAPI.

FastAPI is a framework that helps us create APIs quickly.

The backend files are:

- `backend/app/config.py`
- `backend/app/db.py`
- `backend/app/models.py`
- `backend/app/schemas.py`
- `backend/app/repository.py`
- `backend/app/services.py`
- `backend/app/security.py`
- `backend/app/main.py`

Each file has a different job.
This separation is important.
It makes the code easier to read, test, and maintain.

## 4. `config.py`

### What it is

`config.py` reads configuration values.

Examples:

- database URL
- app secret
- admin username
- admin password
- customer username
- customer password

### Why it exists

We should not hardcode important settings all over the project.

If configuration is kept in one place:

- the code becomes cleaner
- changing values becomes easier
- deployment becomes easier
- the project looks more professional

This is also how real cloud projects often work.
They use environment variables for configuration.

### How it works

The file creates a `Settings` object.
That object stores all important configuration values.

When the application starts:

- it reads environment variables
- if some variables are missing, it uses safe defaults for local development

Think of `config.py` as the settings room of the project.

## 5. `db.py`

### What it is

`db.py` handles database connection setup.

### Why it exists

The application needs a clean way to:

- connect to the database
- create sessions
- manage database work safely

If database logic is repeated in many places, the code becomes messy.

### How it works

This file creates:

- a base class for database models
- a database engine
- a session factory
- a helper that opens and closes sessions correctly

A session is like a conversation between your app and the database.
You open the conversation, do your work, then close it.

The file also supports SQLite for tests.
That keeps tests fast and simple.

## 6. `models.py`

### What it is

`models.py` defines the database tables.

This file describes the shape of the data stored in PostgreSQL.

### Why it exists

The backend needs a clear definition for:

- what a service looks like
- what a user looks like
- what role values are allowed
- what service status values are allowed

### Main parts in this file

#### `ServiceStatus`

This is an enum.
It limits status values to:

- `Healthy`
- `Warning`
- `Critical`

This is good because it prevents random values and keeps the data clean.

#### `UserRole`

This enum limits roles to:

- `admin`
- `customer`

This is important for access control.

#### `User`

This table stores login users.

Important fields:

- `username`
- `full_name`
- `role`
- `password_hash`
- `created_at`

The app stores a password hash, not the real password.
That is safer.

#### `TrackedService`

This table stores cloud services shown in the dashboard.

Important fields:

- `name`
- `environment`
- `owner`
- `status`
- `endpoint`
- `notes`
- `created_at`
- `updated_at`

Interview version:

> In `models.py` I defined the database structure using SQLAlchemy and used enums for roles and service health so the data stays clean and predictable.

## 7. `schemas.py`

### What it is

`schemas.py` defines the shapes of API requests and responses.

### Why it exists

The database model and the API model are not always the same thing.

The API may validate input before data reaches the database.

### How it works

This file uses Pydantic models to define:

- login request body
- login response body
- user response
- service create body
- service update body
- service read response
- summary response

Validation protects the backend.

For example:

- very short names are blocked
- invalid role or status values are blocked
- fields can have max length

Simple memory trick:

- `models.py` = how data is stored in the database
- `schemas.py` = how data enters and leaves the API

## 8. `repository.py`

### What it is

`repository.py` handles direct database queries.

### Why it exists

This file keeps raw database work separate from business logic.

That is useful because:

- it makes code easier to test
- it keeps the service layer cleaner
- it follows a good software design pattern

### Main classes

#### `ServiceRepository`

This class handles service table work:

- list services
- get one service
- create a service
- update a service
- delete a service
- calculate summary counts

The summary part is useful because the backend calculates:

- total
- healthy
- warning
- critical

#### `UserRepository`

This class handles user lookups and user creation.

It is used for:

- finding a user by username
- creating default demo users at startup

Interview version:

> I separated direct database access into a repository layer so the route handlers stay small and the business flow is easier to test.

## 9. `services.py`

### What it is

`services.py` contains business logic.

### Why it exists

The service layer is the place for rules like:

- what happens if a service ID does not exist
- when to return a 404 error
- which repository methods to call in what order

### How it works

The `CloudOpsService` class uses `ServiceRepository`.

It provides methods like:

- `list_services`
- `create_service`
- `update_service`
- `delete_service`
- `summary`

This file is the brain for service management.

## 10. `security.py`

### What it is

`security.py` handles password hashing and token creation.

### Why it exists

Authentication is sensitive.
It is better to keep security-related logic in one clear place.

### Main jobs in this file

#### Password hashing

When the app creates the default admin and customer users, it does not store the plain password.

Instead, it:

- creates a random salt
- builds a secure hash
- stores the hash string

#### Password verification

When a user logs in, the app:

- takes the password the user typed
- hashes it in the same way
- compares it with the stored hash

#### Access token creation

After successful login, the backend creates a token.

That token includes:

- username
- role
- expiration time

Then it signs the token with a secret.

This prevents easy tampering.

Important note:

This is a simple custom token approach for a portfolio project.
In bigger production systems, teams often use JWT libraries or cloud identity systems.

## 11. `main.py`

### What it is

`main.py` is the main entry point of the backend.

This file connects everything together.

### Why it exists

This is where the FastAPI app is created.
It defines:

- startup behavior
- dependencies
- authentication rules
- API routes

### Main responsibilities

#### Create the app

The file creates the FastAPI application object.

#### Store app state

It stores:

- engine
- session factory
- settings

#### Start-up behavior

When the app starts:

- database tables are created if they do not exist
- default admin and customer users are seeded

This makes the app easy to demo.

#### Authentication dependency

The `get_current_user` function:

- reads the bearer token
- validates it
- finds the user in the database
- returns the authenticated user

If something is wrong, it returns `401 Unauthorized`.

#### Admin-only dependency

The `require_admin` function checks:

- is the logged-in user an admin

If not, it returns `403 Forbidden`.

Important beginner idea:

- `401` means not logged in or bad token
- `403` means logged in, but not allowed

### Routes in `main.py`

#### `/health`

What:

- checks if the API and database connection are alive

Why:

- health checks are important for Docker and cloud deployment

How:

- runs a small database query
- returns `{ "status": "ok" }`

#### `/api/auth/login`

What:

- logs in admin or customer

Why:

- users need a way to sign in and receive a token

How:

- checks username
- verifies password
- creates access token
- returns token and user info

#### `/api/auth/me`

What:

- returns the current logged-in user

Why:

- frontend needs to know who is logged in
- frontend needs to know the role

#### `/api/services`

What:

- lists services or creates a service

Why:

- customers and admins both need service visibility
- only admins should create new services

How:

- `GET` requires any logged-in user
- `POST` requires admin

#### `/api/services/{id}`

What:

- updates or deletes one service

Why:

- admins need management control

#### `/api/summary`

What:

- returns counts for dashboard cards

Why:

- frontend should not need to count everything itself

Interview version:

> `main.py` is the glue of the backend. It creates the FastAPI app, wires dependencies, seeds default users, and exposes authenticated and role-protected API routes.

## 12. Frontend overview

The frontend uses simple files:

- `index.html`
- `styles.css`
- `app.js`

This is a smart beginner choice because the project stays easy to understand.

## 13. `index.html`

### What it is

This is the structure of the web page.

### Main parts

- login section
- demo credentials
- dashboard section
- summary cards
- admin control panel
- read-only customer message
- services table

Both login view and dashboard view are in one file.
JavaScript chooses which one to show.

## 14. `styles.css`

### What it is

This file controls the look and feel.

### Why it exists

A recruiter-facing project should not look unfinished.

It styles:

- page layout
- cards
- buttons
- forms
- badges
- role labels
- status colors
- responsive behavior

The colors also support meaning:

- green for healthy
- yellow for warning
- red for critical

## 15. `app.js`

### What it is

This file contains the frontend logic.

### Main ideas

#### State

The file stores current app state like:

- access token
- current user

#### `fetchJson`

This helper function sends API requests.

Why it is useful:

- avoids repeating fetch code
- automatically adds the auth token
- handles JSON response
- handles auth errors

#### Login flow

When the user submits the login form:

1. JavaScript sends username and password to `/api/auth/login`
2. the backend returns a token and user info
3. the token is stored in local storage
4. the dashboard view is shown

#### Restore session

If the user refreshes the browser:

- the token is read from local storage
- the frontend calls `/api/auth/me`
- if valid, the user stays logged in

#### Role-based UI

The page changes based on role:

- admin sees the admin control panel
- customer sees a read-only dashboard

Very important:

Even though the frontend hides admin actions for customer users, the backend still enforces security.
Never trust frontend-only security.

## 16. Test files

The test files are:

- `backend/tests/conftest.py`
- `backend/tests/test_api.py`
- `backend/tests/test_service_logic.py`

### Why tests matter

Tests show that your project is not just working by luck.

They show:

- expected behavior
- protected routes
- role restrictions
- CRUD flow

### `conftest.py`

This file sets up shared test helpers:

- test app
- test client
- admin headers
- customer headers
- test database session

### `test_api.py`

This file checks real API behavior:

- health endpoint works
- login works
- protected endpoints require auth
- customer cannot create services
- admin can create, update, and delete services
- missing service gives 404

### `test_service_logic.py`

This file checks the service layer directly.

## 17. End-to-end request flow

Example: admin creates a service

1. admin logs in from frontend
2. frontend sends login request to backend
3. backend verifies password
4. backend returns token
5. frontend stores token
6. admin fills service form
7. frontend sends POST request with bearer token
8. backend checks token
9. backend checks that role is admin
10. backend saves service in PostgreSQL
11. backend returns the new service
12. frontend refreshes the table and summary cards

This is a very nice story to explain in interview because it shows:

- auth
- API
- business rules
- database write
- UI refresh

## 18. Why customer and admin roles are useful

With roles:

- customer can only view status
- admin can manage status

This shows:

- access control thinking
- security thinking
- user separation

For recruiters, this is better than a plain CRUD demo.

## 19. How to read the code as a beginner

If you feel confused, use this reading order:

1. `README.md`
2. `frontend/static/index.html`
3. `backend/app/main.py`
4. `backend/app/models.py`
5. `backend/app/schemas.py`
6. `backend/app/repository.py`
7. `backend/app/services.py`
8. `backend/app/security.py`
9. `frontend/static/app.js`
10. `backend/tests/test_api.py`

## 20. How to talk about this project in interview

You do not need to explain every file.
You only need a clear story.

Here is a simple way to talk about it:

> I built a three-tier CloudOps Dashboard with a static frontend, a FastAPI backend, and PostgreSQL. I added admin and customer login, where customers can view service health and admins can manage services. I used a repository and service layer to keep the backend organized, stored passwords as hashes, protected API routes by role, and containerized the whole application with Docker Compose for local and AWS deployment.

## 21. Common beginner questions

### Why not put everything in one file?

Because large files become hard to manage.

### Why is there both backend auth and frontend role handling?

Because frontend changes what the user sees, but backend enforces what the user is allowed to do.

### Why do we need schemas if we already have models?

Because database structure and API structure are different jobs.

### Why do we use tests?

To prove the important behavior works and stays working after changes.

### Why is the project good for cloud roles?

Because it shows application design plus deployment thinking.

## 22. Final summary

This project is a good learning example because it teaches several important ideas at the same time:

- clean code structure
- API development
- authentication
- role-based access control
- database usage
- frontend-backend communication
- testing
- deployment readiness

If you understand this project well, you will already be able to discuss:

- how a multi-tier app works
- how Docker helps deployment
- how access control works
- how backend and frontend are connected

That is exactly the kind of understanding that helps beginners grow into cloud, DevOps, and backend roles.
