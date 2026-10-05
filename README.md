# FastAPI Study

A learning project for a user API with PostgreSQL, JWT cookies, and login history.

## Setup

Install dependencies: `pip install -r requirements.txt`.
Configure `.env`: `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`,
`DATABASE_PORT`, `DATABASE_NAME`, and a long random `JWT_SECRET_KEY`.
PostgreSQL must be running, and the configured database must already exist.
Start the app: `uvicorn main:app --reload`.
Swagger UI: http://127.0.0.1:8000/docs.
Without database settings, the app uses SQLite in `fastapistudy.db`.

Tables are created at startup. If the existing `login` table is missing the
`email` column, it is added without deleting data. Other schema changes
require separate migrations.

## Endpoints

- POST `/auth/register`: username, email, age, password; creates an account and sets authentication cookies.
- POST `/auth/login`: username, password; logs in and records the login.
- GET `/users/`: lists users; requires authentication.
- GET `/users/{user_id}`: retrieves a user; requires authentication.
- PUT `/users/{user_id}`: replaces all user fields; only your own account.
- DELETE `/users/{user_id}`: deletes your own account.

For PUT and DELETE, send the `X-CSRF-TOKEN` header with the value of the
`csrf_access_token` cookie.
Cookies are configured for local HTTP. For HTTPS deployment, set
`config.JWT_COOKIE_SECURE = True` in `src/core/security.py`.
Passwords are hashed with Argon2 and excluded from API responses.
Existing SHA-256 hashes are upgraded after a successful login.
Without a persistent `JWT_SECRET_KEY`, restarting the app invalidates tokens.

## Tests

Run `python -m pytest -q`.
Tests use a separate temporary SQLite database regardless of the application
connection settings. These tests do not verify PostgreSQL compatibility.
