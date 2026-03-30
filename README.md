Task Management API (Jira Lite)
===============================

A FastAPI-based backend for a Jira-like task management system.

Current implementation includes:
- User registration
- Project creation
- Basic project listing placeholder
- Database models for users, projects, and issues

Tech Stack
----------
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic

Project Structure
-----------------
backend/
|- src/
|  |- main.py
|  |- core/
|  |  |- db.py
|  |- models/
|  |  |- users_model.py
|  |  |- project_model.py
|  |  |- issue_model.py
|  |- schemas/
|  |  |- user_schema.py
|  |  |- project_schema.py
|  |  |- issue_schema.py
|  |- routers/
|  |  |- user_router.py
|  |  |- project_router.py
|  |  |- issue_router.py
|  |- services/
|  |  |- user_service.py
|  |  |- project_service.py
|- myenv/
|- README.md

Database Configuration
----------------------
Database URL is currently hardcoded in `src/core/db.py`:

`postgresql://postgres:varun@localhost/jira-lite`

Make sure:
1. PostgreSQL is running.
2. Database `jira-lite` exists.
3. Username/password in URL are valid for your machine.

Quick Start
-----------
1. Go to project root:

	 `cd backend`

2. Activate virtual environment:

	 `source myenv/bin/activate`

3. Run server from `src` folder:

	 `cd src`

	 `uvicorn main:app --reload`

4. Open docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

API Endpoints
-------------

Base URL: `http://127.0.0.1:8000`

Health
------
- `GET /`

Response:
```json
{
	"message": "Jira Lite API is running!"
}
```

Users
-----
- `POST /users/register`

Request body:
```json
{
	"username": "varun",
	"email": "varun@example.com",
	"password": "yourpassword",
	"role": "member",
	"is_active": true
}
```

- `POST /users/login` (placeholder)
- `GET /users/me` (placeholder)

Projects
--------
- `GET /project/list` (placeholder)
- `POST /project/create`

Request body:
```json
{
	"key": "JIRA",
	"name": "Jira Lite",
	"description": "Task management backend",
	"owner_id": 1
}
```

Important:
- `owner_id` must exist in `users` table.
- If owner does not exist, API returns `404 Owner user not found`.

Core Data Models
----------------

User
- id (PK)
- username (unique)
- email (unique)
- password
- role
- is_active
- created_at
- updated_at

Project
- id (PK)
- key (unique, max 10)
- name
- description
- owner_id (FK -> users.id)
- status
- created_at
- updated_at

Issue
- id (PK)
- title
- description
- type
- status
- priority
- project_id (FK -> projects.id)
- reporter_id (FK -> users.id)
- assignee_id (FK -> users.id)
- created_at
- updated_at

Current Limitations
-------------------
- Passwords are stored as plain text (must be hashed before production use).
- Login and current-user endpoints are placeholders.
- Issue router and issue schema are not implemented yet.
- Project list endpoint is a placeholder.
- No authentication/authorization yet.

Suggested Next Improvements
---------------------------
1. Add password hashing (bcrypt/passlib).
2. Implement JWT-based auth for login and protected routes.
3. Complete issue schema/router/service.
4. Add response models for all endpoints.
5. Move DB URL to environment variables using `.env`.
6. Add Alembic migrations.


