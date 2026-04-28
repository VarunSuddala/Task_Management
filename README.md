# Task Management API

A clean FastAPI backend for a task management system with JWT auth, role-based access control, PostgreSQL, Redis caching, and Alembic migrations.

## Included pieces

- Signup, login, and JWT access tokens
- Admin, manager, and user roles
- Task create, read, update, delete, and assign endpoints
- Pagination and filtering for task lists
- Redis cache for task list reads
- SQLAlchemy ORM with PostgreSQL
- Alembic migration setup
- Dockerfile and Docker Compose

## Folder structure

- `src/main.py` wires the FastAPI app, routers, and global exception handlers.
- `src/core/` stores settings.
- `src/db/` stores the SQLAlchemy base, database session, and Redis client.
- `src/auth/` stores password hashing, JWT helpers, and auth dependencies.
- `src/models/` stores ORM models.
- `src/schemas/` stores request and response schemas.
- `src/services/` stores the business logic.
- `src/routers/` stores HTTP routes.
- `src/utils/` stores reusable helpers and exception handlers.
- `alembic/` stores migration configuration and the initial schema migration.

## Run with Docker

From the `backend/` folder:

```bash
cp .env.example .env
docker compose up --build
```

Then open `http://localhost:8000/docs`.

## Local run without Docker

```bash
cd backend
source myenv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn src.main:app --reload
```

## API flow

1. A user signs up at `/auth/signup`.
2. The password is hashed before it is stored in PostgreSQL.
3. Login at `/auth/login` verifies the password and returns a JWT token.
4. Protected endpoints read the token from the `Authorization: Bearer <token>` header.
5. Route dependencies check the user role before allowing the action.

## JWT flow

- Signup stores only a password hash.
- Login verifies the hash and issues a signed access token.
- The token includes the user id in `sub` and the role in `role`.
- `/auth/me` reads the token and returns the current user.

## Redis caching logic

- The task list endpoint builds a cache key from the viewer, page, page size, and filters.
- If Redis already has that key, the API returns the cached list.
- On task create, update, assign, or delete, the app clears task list cache keys.
- This keeps reads fast while avoiding stale task list data.

## Important endpoints

- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/{task_id}`
- `POST /tasks/{task_id}/assign`
- `DELETE /tasks/{task_id}`
- `GET /users` for admin only



