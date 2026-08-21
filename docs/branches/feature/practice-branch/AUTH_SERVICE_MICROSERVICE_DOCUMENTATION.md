# Auth Service Microservice

## Pure Backend Authentication Service — Docker + Managed Database + Independent Server

---

## 1. Overview

This project is a standalone **Authentication Microservice** implemented as a pure backend service using:

* Python
* Flask
* Flask-SQLAlchemy
* Flask-Migrate / Alembic
* Flask-JWT-Extended
* PostgreSQL / Supabase Managed Database
* SQLite for local development
* Docker
* Gunicorn
* Flask-CORS
* Sentry
* Request-ID based logging
* Rotating file logs

The Auth Service is designed as an **independent backend microservice**.

It does not contain:

* Angular UI
* React UI
* HTML frontend application
* Business frontend logic
* Browser authentication screens

The frontend communicates with this service through REST APIs.

---

# 2. High-Level Architecture

```text
                    ┌──────────────────────┐
                    │      Angular App     │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               │ HTTPS / REST API
                               ▼
                    ┌──────────────────────┐
                    │    Auth Microservice  │
                    │                      │
                    │      Flask API       │
                    │                      │
                    │  Register            │
                    │  Login               │
                    │  Profile             │
                    │  Refresh             │
                    │  Logout              │
                    │                      │
                    │  JWT Authentication │
                    │  Logging             │
                    │  Sentry             │
                    └──────────┬───────────┘
                               │
                     SQLAlchemy│
                               ▼
                    ┌──────────────────────┐
                    │   Managed Database   │
                    │                      │
                    │ PostgreSQL / Supabase│
                    │                      │
                    │ users                │
                    │ token_blocklist      │
                    └──────────────────────┘


                    ┌──────────────────────┐
                    │       Sentry         │
                    │ Error Monitoring     │
                    └──────────▲───────────┘
                               │
                               │ Exceptions
                               │
                    ┌──────────┴───────────┐
                    │    Auth Service      │
                    └──────────────────────┘
```

---

# 3. Service Responsibility

The Auth Service is responsible for authentication-related operations.

## Responsibilities

### User Management

* User registration
* Password hashing
* Password verification
* User roles
* Duplicate-user detection

### Authentication

* Login
* Access-token generation
* Refresh-token generation
* JWT validation

### Authorization Foundation

* JWT identity
* User role information
* Protected endpoints

### Token Lifecycle

* Access token expiration
* Refresh token expiration
* Token revocation
* Logout
* JWT blocklist

### Observability

* Request IDs
* Structured application logging
* Rotating log files
* Sentry error monitoring

### Infrastructure

* Docker deployment
* Gunicorn production server
* Managed PostgreSQL database
* Database migrations

---

# 4. Microservice Philosophy

The Auth Service should remain independently deployable.

The architecture should be:

```text
Frontend
   │
   ▼
Auth Service
   │
   ▼
Auth Database
```

The Auth Service owns its authentication data.

Other microservices should not directly modify the Auth Service database.

For example:

```text
Angular
   │
   ├──────────────► Auth Service
   │
   ├──────────────► Product Service
   │
   └──────────────► Order Service
```

Each service should communicate through APIs rather than directly accessing another service's database.

---

# 5. Recommended Project Structure

```text
auth-service/
│
├── app/
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── api/
│   │   └── auth_routes.py
│   │
│   ├── services/
│   │   └── auth_service.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token_blacklist.py
│   │
│   └── errors/
│       └── handlers.py
│
├── migrations/
│
├── logs/
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── build_info.json
├── run.py
└── README.md
```

---

# 6. Layered Architecture

The service follows a basic layered architecture.

```text
HTTP Request
     │
     ▼
API / Route Layer
     │
     ▼
Service Layer
     │
     ▼
Model / Database Layer
     │
     ▼
Managed PostgreSQL
```

---

# 7. API Layer

File:

```text
app/api/auth_routes.py
```

The API layer is responsible for:

* Reading HTTP requests
* Validating request input
* Calling service functions
* Creating JWT tokens
* Returning JSON responses
* HTTP status codes

The route layer should not contain excessive database/business logic.

---

# 8. Service Layer

File:

```text
app/services/auth_service.py
```

The service layer contains business logic such as:

```python
register_user()
```

The purpose of this layer is to keep authentication logic separate from HTTP routing.

---

# 9. Database Layer

The database is accessed through:

```text
Flask-SQLAlchemy
```

Models:

```text
User
TokenBlocklist
```

Production database:

```text
PostgreSQL
```

Recommended production hosting:

```text
Supabase Managed PostgreSQL
```

The application does not need to host PostgreSQL inside the same application container.

---

# 10. User Model

File:

```text
app/models/user.py
```

The `User` model contains:

```text
id
email
password_hash
role
```

Example schema:

```text
users
--------------------------------
id              INTEGER PK
email           VARCHAR(150) UNIQUE
password_hash   VARCHAR(200)
role            VARCHAR(20)
```

---

# 11. Password Security

Passwords must never be stored as plaintext.

The application uses:

```python
generate_password_hash()
```

to create a password hash.

During login:

```python
check_password_hash()
```

is used.

Therefore:

```text
User Password
      │
      ▼
Password Hash
      │
      ▼
Database
```

The actual password is never stored in the database.

---

# 12. User Roles

The current model supports:

```text
user
seller
```

Example:

```json
{
  "email": "user@example.com",
  "role": "user"
}
```

or:

```json
{
  "email": "seller@example.com",
  "role": "seller"
}
```

The role is returned during successful login.

Future authorization can use role-based access control:

```text
JWT
 │
 ├── user_id
 │
 └── role
       │
       ├── user
       └── seller
```

---

# 13. Registration API

Endpoint:

```text
POST /api/v1/auth/angularUser/register
```

Example request:

```json
{
  "email": "user@example.com",
  "password": "MyStrongPassword123",
  "role": "user"
}
```

Successful response:

```json
{
  "message": "User registered successfully",
  "role": "user"
}
```

HTTP status:

```text
201 Created
```

---

# 14. Registration Flow

```text
Client
  │
  │ POST /register
  ▼
Auth Route
  │
  │ Validate email/password
  ▼
register_user()
  │
  │ Create User
  ▼
Hash Password
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
  │
  ▼
Commit
  │
  ▼
201 Created
```

If the email already exists:

```text
IntegrityError
      │
      ▼
db.session.rollback()
      │
      ▼
400 User already exists
```

---

# 15. Login API

Endpoint:

```text
POST /api/v1/auth/angularUser/login
```

Request:

```json
{
  "email": "user@example.com",
  "password": "MyStrongPassword123"
}
```

Successful response:

```json
{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "userId": 1,
  "role": "user"
}
```

---

# 16. Login Flow

```text
Client
  │
  │ email + password
  ▼
Auth Route
  │
  ▼
Find User
  │
  ▼
check_password()
  │
  ├── Invalid
  │      │
  │      ▼
  │    401
  │
  └── Valid
         │
         ▼
create_access_token()
         │
         ▼
create_refresh_token()
         │
         ▼
Return JWTs
```

---

# 17. JWT Authentication

The service uses:

```text
Flask-JWT-Extended
```

The access token contains the user's ID as the JWT identity.

Example:

```python
create_access_token(
    identity=str(user.id)
)
```

The refresh token is also generated with the user ID.

---

# 18. Access Token

The access token is used for protected APIs.

Example:

```text
Authorization: Bearer <access_token>
```

The access token is intentionally short-lived.

Current configuration:

```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
```

This is suitable for testing.

A production system may use approximately:

```text
15 minutes
30 minutes
1 hour
```

depending on the application's security requirements.

---

# 19. Refresh Token

Current configuration:

```python
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
```

The refresh token is used to obtain a new access token.

It should not be used as a normal API authorization token.

---

# 20. Profile API

Endpoint:

```text
GET /api/v1/auth/profile
```

Requires:

```text
Authorization: Bearer <access_token>
```

The route uses:

```python
@jwt_required()
```

The identity is retrieved with:

```python
get_jwt_identity()
```

Response:

```json
{
  "user_id": "1"
}
```

---

# 21. Refresh API

Endpoint:

```text
POST /api/v1/auth/refresh
```

Requires a refresh JWT.

The route uses:

```python
@jwt_required(refresh=True)
```

Flow:

```text
Refresh Token
      │
      ▼
JWT Validation
      │
      ▼
Get User ID
      │
      ▼
Create New Access Token
      │
      ▼
Return Access Token
```

Response:

```json
{
  "access_token": "<new JWT>"
}
```

---

# 22. Logout API

Endpoint:

```text
POST /api/v1/auth/logout
```

The route requires an access token.

The application obtains:

```python
access_jti = get_jwt()["jti"]
```

and stores the JTI in:

```text
token_blocklist
```

If a refresh token is supplied, its JTI is also stored.

---

# 23. Token Blocklist

Model:

```text
TokenBlocklist
```

Database table:

```text
token_blocklist
----------------------------
id      INTEGER PK
jti     VARCHAR(200)
```

The JWT blocklist allows the application to revoke JWTs before their normal expiration.

Flow:

```text
Logout
  │
  ├── Access JTI
  │
  └── Refresh JTI
         │
         ▼
  token_blocklist
```

---

# 24. JWT Revocation Check

The application registers:

```python
@jwt.token_in_blocklist_loader
```

For every protected JWT request, the JTI is checked against the database.

Conceptually:

```text
Incoming JWT
     │
     ▼
Extract JTI
     │
     ▼
Query token_blocklist
     │
     ├── Found
     │     │
     │     ▼
     │   REVOKED
     │
     └── Not found
           │
           ▼
         VALID
```

---

# 25. Health Check

Root endpoint:

```text
GET /
```

The application can return either:

### Browser

An HTML health page containing:

```text
Auth Service
UP
Version
Commit
Branch
Build Time
```

### API Client

JSON:

```json
{
  "status": "auth-service UP",
  "build": {
    "version": "...",
    "commit": "...",
    "branch": "...",
    "build_time_utc": "...",
    "build_time_ist": "..."
  }
}
```

---

# 26. Auth Blueprint Health Check

Endpoint:

```text
GET /api/v1/auth/
```

Response:

```json
{
  "status": "auth-service UP",
  "request_id": "<request-id>"
}
```

---

# 27. Sentry Monitoring

The application integrates:

```text
Sentry
```

through:

```python
sentry_sdk
```

and:

```python
FlaskIntegration()
```

Sentry is used for:

* Exception monitoring
* Production error tracking
* Stack traces
* Request context
* Application failures

---

# 28. Sentry Test Endpoint

Development/testing endpoint:

```text
GET /api/v1/auth/sentry-test
```

The route deliberately performs:

```python
1 / 0
```

which creates:

```text
ZeroDivisionError
```

This is used to verify that Sentry captures backend exceptions.

This endpoint should be removed or disabled in production.

---

# 29. Request ID / Correlation ID

Every request receives an ID.

The application checks:

```text
X-Request-ID
```

If the client does not provide one, the application generates a UUID.

Example:

```text
X-Request-ID: 7f9e9f32-....
```

The same ID is available through:

```python
g.request_id
```

and is returned in the response header.

---

# 30. Request ID Flow

```text
Client
  │
  │ X-Request-ID
  ▼
before_request
  │
  ▼
g.request_id
  │
  ├────────► Route logs
  │
  ├────────► Service logs
  │
  ├────────► Error logs
  │
  └────────► Response Header
```

This allows one request to be traced across the complete backend flow.

---

# 31. Logging

The application writes logs to:

```text
logs/auth.log
```

Logs rotate daily using:

```text
TimedRotatingFileHandler
```

Retention:

```text
30 backup files
```

Example:

```text
2026-08-21 19:00:00 [INFO] [REQ:123] Login success user_id=10
```

---

# 32. Why Request IDs Matter

Suppose a frontend reports:

```text
Login failed
```

and sends:

```text
X-Request-ID: ABC-123
```

The backend log can then be searched for:

```text
REQ:ABC-123
```

This allows engineers to trace:

```text
Request
   ↓
Validation
   ↓
Database
   ↓
Authentication
   ↓
JWT generation
   ↓
Response
```

---

# 33. Global Error Handling

File:

```text
app/errors/handlers.py
```

The service has handlers for:

```text
404
400
500
Exception
```

Standard error responses are JSON.

Example:

```json
{
  "success": false,
  "error": "Resource not found"
}
```

Unhandled exceptions are logged with:

```python
app.logger.exception()
```

and reported to Sentry when Sentry is configured.

---

# 34. Configuration

File:

```text
app/config.py
```

Configuration comes from environment variables.

Important variables:

```text
SECRET_KEY
JWT_SECRET_KEY
DATABASE_URL
SENTRY_DSN
```

Example:

```env
SECRET_KEY=<strong-secret>
JWT_SECRET_KEY=<strong-jwt-secret>
DATABASE_URL=<managed-postgresql-url>
SENTRY_DSN=<sentry-dsn>
```

---

# 35. Environment Separation

The application should support separate environments:

```text
Development
Testing
Staging
Production
```

Example:

```text
.env
.env.example
```

`.env` must never be committed to Git.

---

# 36. Production Secrets

Never use these defaults in production:

```python
SECRET_KEY = "super-secret-key"
JWT_SECRET_KEY = "jwt-secret-key"
```

Production must provide strong random values through environment variables.

Example:

```env
SECRET_KEY=<random-production-secret>
JWT_SECRET_KEY=<random-production-jwt-secret>
```

---

# 37. Database Architecture

The database is intentionally separated from the application server.

Recommended architecture:

```text
                 Internet
                    │
                    ▼
          ┌──────────────────┐
          │ Auth API Server  │
          │ Docker Container │
          └────────┬─────────┘
                   │
                   │ PostgreSQL connection
                   ▼
          ┌──────────────────┐
          │ Managed Database │
          │ Supabase         │
          │ PostgreSQL       │
          └──────────────────┘
```

The application container does not own the production database.

---

# 38. Local Database

For local development:

```text
SQLite
```

Current fallback:

```text
sqlite:///auth.db
```

This makes local development simple.

---

# 39. Production Database

Production should use:

```text
PostgreSQL
```

The connection string is supplied through:

```text
DATABASE_URL
```

Example concept:

```env
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
```

The actual production credentials must never be committed to source control.

---

# 40. Managed Database Principle

The recommended production architecture is:

```text
Application Server
        │
        │ SQL
        ▼
Managed PostgreSQL
```

Instead of:

```text
Application Server
        │
        ▼
PostgreSQL Docker Container
```

A managed database provides database operations independently from the application deployment.

Benefits include:

* Persistent storage
* Backups
* Database monitoring
* Database availability management
* Independent scaling
* Easier application redeployment

---

# 41. Database Migrations

The application uses:

```text
Flask-Migrate
```

which uses:

```text
Alembic
```

Migration files are stored under:

```text
migrations/
```

When a model changes, create a migration.

Example:

```bash
flask db migrate -m "add user role"
```

Then apply it:

```bash
flask db upgrade
```

---

# 42. Migration Principle

Do not manually change production tables whenever possible.

Preferred process:

```text
Change SQLAlchemy Model
        │
        ▼
flask db migrate
        │
        ▼
Review Migration
        │
        ▼
Commit Migration
        │
        ▼
Deploy
        │
        ▼
flask db upgrade
```

---

# 43. Docker Architecture

The Auth Service should be packaged as a Docker image.

```text
Docker Image
     │
     ▼
Python Runtime
     │
     ▼
Flask Application
     │
     ▼
Gunicorn
```

Production:

```text
Managed Platform
       │
       ▼
Docker Container
       │
       ▼
Gunicorn
       │
       ▼
Flask App
```

---

# 44. Why Docker

Docker provides:

* Reproducible runtime
* Consistent Python environment
* Dependency isolation
* Easy deployment
* Easy rollback
* Portable application image

The application should not depend on a developer's local Python installation.

---

# 45. Production Server

The application should use:

```text
Gunicorn
```

instead of Flask's development server.

Development:

```bash
flask run
```

Production:

```bash
gunicorn
```

The Flask development server should not be used as the production server.

---

# 46. Gunicorn Application Target

The current `run.py` exposes:

```python
app = create_app()
```

Therefore the Gunicorn target can be:

```text
run:app
```

Example:

```bash
gunicorn --bind 0.0.0.0:$PORT run:app
```

The exact worker configuration can be adjusted based on deployment platform and workload.

---

# 47. Dockerfile Responsibility

The Dockerfile should:

1. Start from a Python base image.
2. Set the working directory.
3. Install dependencies.
4. Copy application code.
5. Expose the application port.
6. Start Gunicorn.

Conceptually:

```text
Base Python Image
       │
       ▼
Install Dependencies
       │
       ▼
Copy Source
       │
       ▼
Start Gunicorn
```

---

# 48. Docker + Managed DB

The final production setup is:

```text
┌─────────────────────────────────────────────┐
│                 Cloud Server                │
│                                             │
│   ┌─────────────────────────────────────┐   │
│   │        Auth Docker Container        │   │
│   │                                     │   │
│   │  Gunicorn                           │   │
│   │     ↓                               │   │
│   │  Flask                              │   │
│   │     ↓                               │   │
│   │  SQLAlchemy                         │   │
│   └─────────────────┬───────────────────┘   │
│                     │                       │
└─────────────────────┼───────────────────────┘
                      │
                      │ PostgreSQL
                      ▼
            ┌─────────────────────┐
            │ Supabase PostgreSQL │
            │ Managed Database    │
            └─────────────────────┘
```

Sentry remains an external monitoring service:

```text
Auth Container ───────► Sentry
```

---

# 49. CORS

The service uses:

```python
CORS()
```

to support frontend communication.

In production, CORS should ideally be restricted to known frontend origins.

Example concept:

```text
Allowed Origin:
https://frontend.example.com
```

Avoid unrestricted origins in production unless there is a specific requirement.

---

# 50. Complete API List

| Method | Endpoint                            | Authentication | Purpose               |
| ------ | ----------------------------------- | -------------- | --------------------- |
| GET    | `/`                                 | No             | Service health        |
| GET    | `/api/v1/auth/`                     | No             | Auth service health   |
| GET    | `/api/v1/auth/sentry-test`          | No             | Sentry testing        |
| POST   | `/api/v1/auth/angularUser/register` | No             | Register user         |
| POST   | `/api/v1/auth/angularUser/login`    | No             | Login                 |
| GET    | `/api/v1/auth/profile`              | Access JWT     | Get profile identity  |
| POST   | `/api/v1/auth/refresh`              | Refresh JWT    | Generate access token |
| POST   | `/api/v1/auth/logout`               | Access JWT     | Revoke tokens         |

---

# 51. Complete Authentication Lifecycle

```text
                 REGISTER
                    │
                    ▼
              Create User
                    │
                    ▼
              Hash Password
                    │
                    ▼
                Database
                    │
                    ▼
                 LOGIN
                    │
                    ▼
            Verify Password
                    │
                    ▼
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
 Access Token            Refresh Token
        │                       │
        ▼                       ▼
 Protected APIs            /refresh
        │                       │
        │                       ▼
        │                New Access Token
        │
        ▼
      LOGOUT
        │
        ▼
  Blocklist JTIs
        │
        ▼
      Tokens
     Revoked
```

---

# 52. Recommended Production Request Flow

```text
Frontend
   │
   │ HTTPS
   ▼
Load Balancer / Platform
   │
   ▼
Docker Container
   │
   ▼
Gunicorn
   │
   ▼
Flask
   │
   ├── Request ID
   │
   ├── JWT
   │
   ├── Route
   │
   ├── Service
   │
   └── SQLAlchemy
          │
          ▼
   Managed PostgreSQL
```

Errors:

```text
Flask
  │
  ├────────► Logs
  │
  └────────► Sentry
```

---

# 53. Build Information

The service reads:

```text
build_info.json
```

The file can contain:

```json
{
  "version": "1.0.0",
  "commit": "abc123",
  "branch": "main",
  "build_time_utc": "2026-08-21T00:00:00Z",
  "build_time_ist": "2026-08-21T05:30:00+05:30"
}
```

This allows the health endpoint to expose deployment information.

---

# 54. Deployment Model

The recommended deployment is:

```text
Git Repository
      │
      ▼
CI/CD
      │
      ▼
Docker Build
      │
      ▼
Docker Image
      │
      ▼
Production Server / Container Platform
      │
      ▼
Gunicorn
      │
      ▼
Auth Service
      │
      ├────────► Managed PostgreSQL
      │
      └────────► Sentry
```

---

# 55. Independent Server Principle

The Auth Service runs independently from the frontend.

Example:

```text
Frontend:
https://app.example.com

Auth:
https://auth.example.com
```

The frontend calls:

```text
https://auth.example.com/api/v1/auth/angularUser/login
```

The frontend should not need to know anything about the Auth Service's database.

---

# 56. Database Ownership

The Auth Service owns:

```text
users
token_blocklist
```

Other services should not directly manipulate these tables.

For example:

```text
Order Service
      X
      │
      X direct DB access
      │
      ▼
Auth Database
```

Instead:

```text
Order Service
      │
      ▼
Auth API
```

when authentication-related information is required.

---

# 57. Security Recommendations

The current implementation provides a solid foundation, but production hardening is recommended.

## Secrets

Never commit:

```text
.env
DATABASE_URL
SECRET_KEY
JWT_SECRET_KEY
SENTRY_DSN
```

## HTTPS

Production APIs should be served over:

```text
HTTPS
```

## Passwords

Never log passwords.

## JWTs

Never log complete JWT values.

## CORS

Restrict allowed origins.

## Debug Mode

Disable Flask debug mode in production.

## Sentry Test

Remove:

```text
/sentry-test
```

from production.

---

# 58. Recommended JWT Improvements

The current implementation stores only the user ID as the JWT identity.

For future authorization, additional claims may be introduced.

For example:

```text
user_id
role
```

Conceptually:

```json
{
  "sub": "123",
  "role": "seller"
}
```

However, authorization-critical information should be designed carefully because JWT claims can become stale until the token expires.

For sensitive authorization decisions, the server may need to verify current user state.

---

# 59. Refresh Token Security

The current logout implementation accepts a refresh token in the request body:

```json
{
  "refresh_token": "<refresh-token>"
}
```

For stronger production security, refresh-token lifecycle management can be expanded.

Possible future improvements:

```text
Refresh token rotation
Refresh token family tracking
Refresh token reuse detection
Device/session tracking
Server-side session records
```

---

# 60. Token Blocklist Improvements

The current table contains:

```text
id
jti
```

A production implementation may additionally store:

```text
jti
user_id
token_type
expires_at
created_at
revoked_at
```

This makes cleanup and auditing easier.

For example:

```text
token_blocklist
--------------------------------
id
jti
user_id
token_type
expires_at
revoked_at
created_at
```

Expired blacklist records can then be cleaned periodically.

---

# 61. Input Validation

The current registration validation checks:

```text
email exists
password exists
```

Production validation should additionally consider:

```text
Email format
Password minimum length
Password complexity
Maximum input length
Allowed roles
Normalization of email
```

For example, roles should not blindly accept arbitrary values.

Allowed:

```text
user
seller
```

Rejected:

```text
admin
superuser
anything-arbitrary
```

unless those roles are explicitly supported.

---

# 62. Email Normalization

A production authentication system should decide on a consistent email policy.

For example:

```text
User@Example.com
```

could be normalized according to the application's chosen rules.

The important requirement is consistency for:

```text
Registration
Login
Duplicate detection
Password reset
Account lookup
```

---

# 63. Rate Limiting

Authentication endpoints should eventually have rate limiting.

Especially:

```text
/login
/register
/refresh
```

This helps protect against:

```text
Brute-force login
Credential stuffing
Automated registration
Token abuse
```

A future implementation could use Redis-backed rate limiting.

---

# 64. Account Lockout / Abuse Protection

For higher-security environments, consider:

```text
Failed login tracking
Temporary account lockout
IP-based throttling
Device/session monitoring
Suspicious login detection
```

These should be added based on actual application requirements.

---

# 65. Database Connection Stability

The current configuration uses:

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
```

`pool_pre_ping` helps detect stale database connections before use.

`pool_recycle` helps recycle old connections.

This is useful when connecting to managed PostgreSQL services.

---

# 66. Production Database Connectivity

The production container should receive:

```text
DATABASE_URL
```

through the deployment platform's secret/environment configuration.

Do not hard-code:

```text
hostname
username
password
database
```

inside Python source code.

---

# 67. Local Development

Local development can use:

```text
SQLite
```

Run the application:

```bash
venv\Scripts\activate
```

Then:

```bash
set FLASK_APP=run.py
```

and:

```bash
flask run --host=0.0.0.0 --port=5001
```

For development debugging:

```bash
flask run --host=0.0.0.0 --port=5001 --debug
```

Debug mode should not be enabled in production.

---

# 68. Production Execution

Production should use Gunicorn.

Example:

```bash
gunicorn --bind 0.0.0.0:$PORT run:app
```

The deployment platform supplies the production `PORT`.

---

# 69. Docker Runtime

The production runtime should conceptually be:

```text
Docker
  │
  ▼
Gunicorn
  │
  ▼
run:app
  │
  ▼
create_app()
  │
  ├── DB
  ├── JWT
  ├── CORS
  ├── Sentry
  ├── Logging
  ├── Routes
  └── Error Handlers
```

---

# 70. Container Statelessness

The application container should be treated as stateless.

Do not depend on local container filesystem data for persistent business data.

Persistent data belongs in:

```text
Managed PostgreSQL
```

Logs should preferably be shipped to the deployment platform/logging system in addition to local file logging if the hosting platform does not guarantee persistent container storage.

---

# 71. Production Observability

The service has three major observability mechanisms:

```text
1. Request ID
2. Application Logs
3. Sentry
```

Together:

```text
Request ID
    +
Logs
    +
Sentry
    =
Traceable Production Errors
```

---

# 72. Example Production Incident

Suppose login fails unexpectedly.

Frontend sends:

```text
X-Request-ID: ABC-456
```

The backend logs:

```text
[REQ:ABC-456] Login success user_id=10
```

or:

```text
[REQ:ABC-456] Invalid login user@example.com
```

If an unexpected exception occurs:

```text
Unhandled Exception
```

is logged and Sentry can capture the exception.

Engineering can correlate:

```text
Frontend request
      │
      ▼
X-Request-ID
      │
      ├── Backend logs
      │
      └── Error monitoring
```

---

# 73. API Versioning

The service currently uses:

```text
/api/v1/auth
```

This is a good foundation for API versioning.

Future breaking changes can use:

```text
/api/v2/auth
```

instead of breaking existing clients.

---

# 74. Current API Naming

Current Angular-oriented endpoints are:

```text
/angularUser/register
/angularUser/login
```

If the service becomes a general-purpose authentication microservice, a cleaner future naming convention could be:

```text
/api/v1/auth/register
/api/v1/auth/login
/api/v1/auth/profile
/api/v1/auth/refresh
/api/v1/auth/logout
```

The existing endpoints can remain for backward compatibility.

---

# 75. Frontend Integration

The Angular frontend should:

1. Call registration API.
2. Call login API.
3. Store/use authentication tokens according to the application's security model.
4. Send access JWT to protected endpoints.
5. Detect expired access tokens.
6. Call refresh endpoint.
7. Retry the original request where appropriate.
8. Call logout endpoint.
9. Clear client-side authentication state.

Conceptually:

```text
Angular
   │
   ├── Login
   │      │
   │      ▼
   │   Access JWT
   │
   ├── API Request
   │      │
   │      ▼
   │   401 / Expired
   │      │
   │      ▼
   │   Refresh
   │      │
   │      ▼
   │   New Access JWT
   │      │
   │      ▼
   │   Retry Request
   │
   └── Logout
```

---

# 76. Production Components

The complete production environment consists of separate components:

```text
┌─────────────────────────────────────┐
│             Frontend                │
│             Angular                 │
└──────────────────┬──────────────────┘
                   │
                   │ HTTPS
                   ▼
┌─────────────────────────────────────┐
│          Auth API Server             │
│                                     │
│ Docker                              │
│ Gunicorn                            │
│ Flask                               │
│ SQLAlchemy                          │
│ JWT                                 │
│ Logging                             │
│ Sentry                              │
└──────────────────┬──────────────────┘
                   │
                   │ PostgreSQL
                   ▼
┌─────────────────────────────────────┐
│       Managed PostgreSQL             │
│             Supabase                │
└─────────────────────────────────────┘
```

---

# 77. What Is NOT Inside the Auth Service

The Auth Service should not contain:

```text
Angular components
Angular services
HTML pages
CSS
Frontend routing
Product catalog
Orders
Payments
Shopping cart
Seller product management
UI state
```

Those belong to other applications/services.

---

# 78. What Belongs Inside the Auth Service

```text
User registration
User login
Password hashing
Password verification
JWT creation
JWT validation
JWT refresh
Logout
Token revocation
User identity
Authentication roles
Authentication-related database models
Authentication logs
Authentication monitoring
```

---

# 79. Recommended Repository Separation

A larger system could eventually have:

```text
frontend/
    Angular application

auth-service/
    Flask authentication microservice

product-service/
    Product backend

order-service/
    Order backend

payment-service/
    Payment backend
```

Each service can be independently deployed.

---

# 80. Service-to-Service Architecture

A mature architecture could look like:

```text
                         Angular
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        Auth Service   Product Service  Order Service
              │             │             │
              ▼             ▼             ▼
        Auth Database   Product DB      Order DB
```

Each service owns its own database.

---

# 81. Authentication Boundary

The Auth Service is the authority for:

```text
Who is the user?
Is the credential valid?
What identity does the token represent?
Is the token revoked?
What role does the user have?
```

Other services consume authenticated identity rather than implementing duplicate password authentication.

---

# 82. Production Checklist

Before production deployment:

* [ ] Replace default `SECRET_KEY`.
* [ ] Replace default `JWT_SECRET_KEY`.
* [ ] Configure production `DATABASE_URL`.
* [ ] Configure `SENTRY_DSN`.
* [ ] Use PostgreSQL.
* [ ] Run database migrations.
* [ ] Use Gunicorn.
* [ ] Use Docker.
* [ ] Disable Flask debug mode.
* [ ] Restrict CORS.
* [ ] Remove `/sentry-test`.
* [ ] Verify HTTPS.
* [ ] Verify JWT expiration.
* [ ] Verify logout/revocation.
* [ ] Verify database connectivity.
* [ ] Verify Sentry exception capture.
* [ ] Verify request IDs.
* [ ] Verify production logs.
* [ ] Verify health endpoint.
* [ ] Verify deployment build information.
* [ ] Ensure `.env` is not committed.
* [ ] Ensure passwords/tokens are not logged.

---

# 83. Deployment Verification

After deployment, verify:

### Health

```text
GET /
```

Expected:

```text
Auth Service UP
```

### Auth Health

```text
GET /api/v1/auth/
```

Expected:

```json
{
  "status": "auth-service UP"
}
```

### Registration

```text
POST /api/v1/auth/angularUser/register
```

### Login

```text
POST /api/v1/auth/angularUser/login
```

Verify:

```text
access_token
refresh_token
userId
role
```

### Protected API

```text
GET /api/v1/auth/profile
```

with:

```text
Authorization: Bearer <access_token>
```

### Refresh

```text
POST /api/v1/auth/refresh
```

using refresh JWT.

### Logout

```text
POST /api/v1/auth/logout
```

Verify the revoked access token can no longer access protected endpoints.

---

# 84. Final Architecture

The final intended architecture is:

```text
                           CLIENT
                             │
                             │ HTTPS
                             ▼
                  ┌─────────────────────┐
                  │   Angular Frontend  │
                  └──────────┬──────────┘
                             │
                             │ REST API
                             ▼
┌──────────────────────────────────────────────────────┐
│                 AUTH MICROSERVICE                    │
│                                                      │
│                    Docker                           │
│                       │                              │
│                    Gunicorn                         │
│                       │                              │
│                    Flask API                        │
│                       │                              │
│       ┌───────────────┼────────────────┐             │
│       │               │                │             │
│       ▼               ▼                ▼             │
│    Routes          Services          JWT             │
│       │               │                │             │
│       └───────────────┼────────────────┘             │
│                       │                              │
│                   SQLAlchemy                         │
│                       │                              │
│       ┌───────────────┼───────────────┐              │
│       │               │               │              │
│       ▼               ▼               ▼              │
│     Users       Token Blocklist     Migrations       │
│                                                      │
│       ┌──────────────────────┐                       │
│       │ Request ID + Logging │                       │
│       └──────────────────────┘                       │
│                                                      │
│       ┌──────────────────────┐                       │
│       │       Sentry         │                       │
│       └──────────────────────┘                       │
└───────────────────────┬──────────────────────────────┘
                        │
                        │ PostgreSQL
                        ▼
             ┌────────────────────────┐
             │   Managed PostgreSQL   │
             │       Supabase        │
             │                        │
             │   users               │
             │   token_blocklist     │
             └────────────────────────┘
```

---

# 85. Final Design Statement

This project is a **pure backend Authentication Microservice**.

Its production architecture is intentionally separated into:

```text
Frontend
   ≠
Auth Backend
   ≠
Database
```

The Auth Backend is containerized using Docker and runs independently on a production server/container platform using Gunicorn.

The production database is a separately managed PostgreSQL database, such as Supabase PostgreSQL.

The service provides:

```text
Registration
Login
JWT Access Tokens
JWT Refresh Tokens
Protected APIs
Logout
Token Revocation
User Roles
Password Hashing
Database Migrations
Request IDs
Rotating Logs
Sentry Monitoring
Health Checks
Docker Deployment
Independent Backend Hosting
Managed Database Hosting
```

The resulting architecture is therefore:

```text
                 FRONTEND
                    │
                    ▼
             AUTH MICROSERVICE
                    │
             ┌──────┴──────┐
             │             │
             ▼             ▼
       SENTRY/LOGS    MANAGED DATABASE
                         PostgreSQL
```

This separation allows the authentication system to be developed, deployed, monitored, scaled, and maintained independently from the frontend and from other backend microservices.
