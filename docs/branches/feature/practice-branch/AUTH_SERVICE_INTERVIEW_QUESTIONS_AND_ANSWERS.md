# Auth Service Microservice — Interview Questions, Answers & Practice

## 1. Project Introduction

### Q1. Explain your project.

**Answer:**

My project is a standalone Flask-based Authentication Microservice.

It provides:

* User registration
* Login
* JWT access and refresh tokens
* Protected APIs
* Logout and token revocation
* Role management
* Password hashing
* PostgreSQL database support
* Database migrations
* Request-ID logging
* Sentry monitoring
* Docker-based deployment

The frontend communicates with the Auth Service through REST APIs, while the production database is hosted separately as a managed PostgreSQL database.

---

# 2. Flask Concepts

### Q2. Why did you use Flask?

**Answer:**

Flask is lightweight and flexible. It is suitable for building REST APIs and microservices without unnecessary framework overhead.

---

### Q3. What is a Flask Blueprint?

**Answer:**

A Blueprint helps organize routes into separate modules.

Simple example:

```python
auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/profile")
def profile():
    return {"message": "profile"}
```

Then it is registered with the application.

```python
app.register_blueprint(auth_bp)
```

---

### Q4. What is an application factory?

**Answer:**

`create_app()` creates and configures the Flask application.

```python
def create_app():
    app = Flask(__name__)
    return app
```

It makes the application easier to test and configure for different environments.

---

# 3. SQLAlchemy

### Q5. Why did you use SQLAlchemy?

**Answer:**

SQLAlchemy provides ORM functionality, so I can work with database tables using Python models instead of writing SQL for every operation.

---

### Q6. What is a model?

**Answer:**

A model represents a database table.

Example:

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
```

The `User` class represents the `users` table.

---

### Q7. What does `primary_key=True` mean?

**Answer:**

It identifies a column uniquely for each database record.

For example:

```python
id = db.Column(db.Integer, primary_key=True)
```

---

### Q8. What does `unique=True` mean?

**Answer:**

It prevents duplicate values.

In my project:

```python
email = db.Column(
    db.String(150),
    unique=True
)
```

So two users cannot normally have the same email.

---

# 4. Password Security

### Q9. Do you store the user's password?

**Answer:**

No.

I store a password hash.

```python
user.set_password(password)
```

Internally:

```python
generate_password_hash(password)
```

During login:

```python
check_password_hash(hash, password)
```

---

### Q10. Why hash passwords?

**Answer:**

If the database is compromised, plaintext passwords would immediately be exposed. Password hashing provides a much safer storage mechanism.

---

### Q11. What is the difference between hashing and encryption?

**Answer:**

Hashing is generally one-way.

```text
Password → Hash
```

You don't decrypt the hash to get the original password.

Encryption is reversible with a key:

```text
Data → Encryption → Decryption → Data
```

---

# 5. JWT

### Q12. What is JWT?

**Answer:**

JWT stands for JSON Web Token. It is used to represent authenticated user information between the client and server.

---

### Q13. Why did you use JWT?

**Answer:**

JWT works well for REST APIs because the server can validate the token sent with requests.

Example:

```text
Authorization: Bearer <token>
```

---

### Q14. What is an access token?

**Answer:**

The access token is a short-lived token used to access protected APIs.

In my configuration:

```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
```

---

### Q15. What is a refresh token?

**Answer:**

A refresh token is longer-lived and is used to obtain a new access token after the access token expires.

My configuration uses:

```python
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
```

---

### Q16. Why have two tokens?

**Answer:**

The access token can be short-lived for security, while the refresh token provides a way to obtain a new access token without forcing the user to log in again.

---

### Q17. What does `@jwt_required()` do?

**Answer:**

It protects an endpoint and requires a valid JWT.

```python
@jwt_required()
def profile():
    ...
```

---

### Q18. What does `@jwt_required(refresh=True)` mean?

**Answer:**

It specifically requires a refresh token.

```python
@jwt_required(refresh=True)
def refresh():
    ...
```

---

### Q19. What is `get_jwt_identity()`?

**Answer:**

It retrieves the identity stored inside the JWT.

In my project, the identity is the user ID.

```python
user_id = get_jwt_identity()
```

---

# 6. Token Revocation

### Q20. JWTs are stateless, so how do you implement logout?

**Answer:**

I use a JWT blocklist.

When the user logs out, I get the JWT's JTI and save it in the `token_blocklist` table.

```python
jti = get_jwt()["jti"]

db.session.add(
    TokenBlocklist(jti=jti)
)
```

Later, every protected request checks whether that JTI is revoked.

---

### Q21. What is JTI?

**Answer:**

JTI means JWT ID. It uniquely identifies a JWT.

Simple concept:

```text
JWT
 ↓
JTI
 ↓
Blocklist
```

---

### Q22. Why do you need a blocklist?

**Answer:**

Normally, a JWT remains valid until it expires. The blocklist allows the server to revoke it earlier, such as during logout.

---

# 7. Database Transactions

### Q23. Why do you use `db.session.commit()`?

**Answer:**

It commits the database transaction and permanently saves the changes.

```python
db.session.add(user)
db.session.commit()
```

---

### Q24. Why do you use rollback?

**Answer:**

If a database operation fails, rollback returns the current transaction to a clean state.

```python
except IntegrityError:
    db.session.rollback()
```

---

### Q25. What is `IntegrityError`?

**Answer:**

It is a database integrity violation.

For example, registering an email that already exists when the email column is unique.

---

# 8. Service Layer

### Q26. Why did you create `auth_service.py`?

**Answer:**

I separated business logic from the API routes.

The route handles HTTP:

```text
Request → Route → Response
```

The service handles business logic:

```text
Register User → Hash Password → Save User
```

This makes the code easier to maintain and test.

---

### Q27. Why shouldn't everything be written inside the route?

**Answer:**

Large routes become difficult to maintain and test.

Separating:

```text
API Layer
Service Layer
Database Layer
```

keeps responsibilities clear.

---

# 9. Request ID

### Q28. Why did you implement request IDs?

**Answer:**

A request ID helps trace one request through the application logs.

Example:

```text
REQ:ABC123
```

I can search the logs for `ABC123` and follow the complete request.

---

### Q29. Where do you store the request ID?

**Answer:**

I store it in Flask's request context:

```python
g.request_id = request_id
```

---

### Q30. What is Flask `g`?

**Answer:**

`g` is a Flask context object used to store data during the current request.

For example:

```python
g.request_id = "ABC123"
```

---

# 10. Middleware / Request Lifecycle

### Q31. What is `before_request`?

**Answer:**

It runs before the request reaches the route.

My application uses it to create the request ID.

```python
@app.before_request
def assign_request_id():
    g.request_id = str(uuid.uuid4())
```

---

### Q32. What is `after_request`?

**Answer:**

It runs after the route creates a response.

I use it to return the request ID in the response header.

```python
@app.after_request
def attach_request_id(response):
    response.headers["X-Request-ID"] = g.request_id
    return response
```

---

# 11. Error Handling

### Q33. Why do you have global error handlers?

**Answer:**

They provide consistent API error responses and prevent internal exceptions from returning uncontrolled responses.

Example:

```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

### Q34. What does `app.logger.exception()` do?

**Answer:**

It logs the exception with traceback information, which is useful for debugging production problems.

---

# 12. Sentry

### Q35. Why did you use Sentry?

**Answer:**

Sentry provides production error monitoring.

If an unexpected exception occurs, Sentry can capture information about the error and its traceback.

---

### Q36. How did you test Sentry?

**Answer:**

I created a test endpoint that intentionally raises an exception.

Simple example:

```python
@app.get("/sentry-test")
def test():
    return 1 / 0
```

This should only be available during testing, not production.

---

# 13. Logging

### Q37. Why use rotating logs?

**Answer:**

Without rotation, log files can grow continuously. `TimedRotatingFileHandler` creates new log files periodically and keeps a configured number of backups.

---

### Q38. What information do your logs contain?

**Answer:**

They contain:

```text
Timestamp
Log level
Request ID
Message
```

Example:

```text
INFO [REQ:ABC123] Login success user_id=10
```

---

# 14. CORS

### Q39. What is CORS?

**Answer:**

CORS controls which browser origins are allowed to make requests to the backend.

It is important because my Angular frontend and backend can be hosted on different domains.

---

### Q40. Should CORS be open to everyone in production?

**Answer:**

Preferably no. Production should allow only trusted frontend origins.

---

# 15. Flask-Migrate

### Q41. Why use Flask-Migrate?

**Answer:**

It manages database schema changes using Alembic.

For example, if I add a `role` column, I can generate and apply a migration.

```bash
flask db migrate -m "add role"
flask db upgrade
```

---

### Q42. What is Alembic?

**Answer:**

Alembic is the database migration tool used underneath Flask-Migrate.

---

# 16. Docker

### Q43. Why Dockerize the Auth Service?

**Answer:**

Docker gives me a consistent runtime environment and makes deployment easier.

The application runs the same packaged environment across development and production.

---

### Q44. Why use Gunicorn?

**Answer:**

Flask's development server is not intended for production. Gunicorn is a production WSGI server designed to run Flask applications.

Example:

```bash
gunicorn run:app
```

---

### Q45. What does `run:app` mean?

**Answer:**

It means:

```text
run.py
  ↓
app variable
```

So Gunicorn loads the `app` object from `run.py`.

---

# 17. Managed Database

### Q46. Why use a managed PostgreSQL database?

**Answer:**

The database is separated from the application server. A managed database provider handles important infrastructure concerns such as database availability, backups, and maintenance.

---

### Q47. Why not put PostgreSQL inside the same application container?

**Answer:**

Application containers should ideally be stateless and independently deployable. A managed database provides persistent storage independently from application containers.

---

### Q48. What happens if the Docker container is recreated?

**Answer:**

The application container can be recreated without losing database data because the production data is stored in the managed PostgreSQL database.

---

# 18. Environment Variables

### Q49. Why use environment variables?

**Answer:**

Secrets and environment-specific configuration should not be hard-coded.

Examples:

```text
DATABASE_URL
SECRET_KEY
JWT_SECRET_KEY
SENTRY_DSN
```

---

### Q50. Why shouldn't `.env` be committed?

**Answer:**

It may contain database credentials and security secrets. It should be added to `.gitignore`.

---

# 19. Microservices

### Q51. Why is this a microservice?

**Answer:**

Authentication is isolated into an independently deployable backend service with its own API and database ownership.

---

### Q52. Does the frontend directly access the Auth database?

**Answer:**

No.

The frontend communicates with the Auth API.

```text
Frontend
   ↓
Auth API
   ↓
Database
```

---

### Q53. Should another microservice directly access the Auth database?

**Answer:**

Preferably no. The Auth Service should own its database and expose APIs for authentication-related operations.

---

# 20. HTTP Status Codes

### Q54. Why return 201 during registration?

**Answer:**

`201 Created` indicates that a new resource was successfully created.

---

### Q55. Why return 401 during invalid login?

**Answer:**

`401 Unauthorized` indicates that authentication failed.

Example:

```json
{
  "message": "Invalid email or password"
}
```

---

### Q56. What is the difference between 401 and 403?

**Answer:**

Simple rule:

```text
401 → Authentication is missing/invalid

403 → Authentication exists, but access is forbidden
```

---

# 21. Scenario Questions

### Q57. User logs in successfully. What happens?

**Answer:**

```text
Email/password
     ↓
Find User
     ↓
Check Password
     ↓
Create Access Token
     ↓
Create Refresh Token
     ↓
Return Tokens
```

---

### Q58. Access token expires. What happens?

**Answer:**

The frontend can use the refresh token to request a new access token.

```text
Access Token Expired
        ↓
Refresh Token
        ↓
New Access Token
```

---

### Q59. User logs out. What happens?

**Answer:**

The JWT JTI is added to the token blocklist. Future requests using that revoked token are rejected.

---

### Q60. Database registration fails. What happens?

**Answer:**

The transaction is rolled back.

```python
db.session.rollback()
```

Then an appropriate error response is returned.

---

### Q61. Two users register with the same email. What happens?

**Answer:**

The database's unique constraint prevents the duplicate. SQLAlchemy raises `IntegrityError`, and the transaction is rolled back.

---

### Q62. Sentry is not configured. What happens?

**Answer:**

The code checks whether `SENTRY_DSN` exists. Without a DSN, Sentry initialization is skipped.

---

# 22. Important Concepts to Study

For an interview based on this project, focus strongly on these concepts:

## Must Know

```text
Flask
REST API
HTTP methods
HTTP status codes
Blueprints
Application Factory
SQLAlchemy ORM
Database transactions
JWT
Access Token
Refresh Token
JTI
JWT Revocation
Password Hashing
CORS
Environment Variables
Docker
Gunicorn
PostgreSQL
Database Migrations
Logging
Request IDs
Sentry
Microservices
```

---

# 23. Small Syntax Snippets to Practice

## Flask Route

```python
@app.get("/hello")
def hello():
    return {"message": "hello"}
```

## POST Request

```python
@app.post("/login")
def login():
    data = request.get_json()
    return data
```

## SQLAlchemy Query

```python
user = User.query.filter_by(email=email).first()
```

## Add Record

```python
db.session.add(user)
db.session.commit()
```

## Rollback

```python
db.session.rollback()
```

## Password Hash

```python
user.set_password(password)
```

## Password Check

```python
user.check_password(password)
```

## JWT Creation

```python
token = create_access_token(
    identity=str(user.id)
)
```

## Protected Route

```python
@jwt_required()
def profile():
    return {"ok": True}
```

## JWT Identity

```python
user_id = get_jwt_identity()
```

## JWT JTI

```python
jti = get_jwt()["jti"]
```

## Request ID

```python
g.request_id = str(uuid.uuid4())
```

## Logging

```python
current_app.logger.info("Login successful")
```

## Error Logging

```python
current_app.logger.exception("Something failed")
```

---

# 24. Interview Practice — Rapid Fire

Try answering these without looking at the answers:

1. What is Flask?
2. What is a Blueprint?
3. What is an application factory?
4. What is REST?
5. What is SQLAlchemy?
6. What is ORM?
7. What is a primary key?
8. What is a unique constraint?
9. Why hash passwords?
10. Hashing vs encryption?
11. What is JWT?
12. Access token vs refresh token?
13. What is JTI?
14. How does JWT logout work in your project?
15. What is a JWT blocklist?
16. What does `jwt_required()` do?
17. What does `get_jwt_identity()` do?
18. What is a database transaction?
19. Why use rollback?
20. What is `IntegrityError`?
21. What is Flask-Migrate?
22. What is Alembic?
23. Why Docker?
24. Why Gunicorn?
25. Why managed PostgreSQL?
26. Why environment variables?
27. What is CORS?
28. What is Sentry?
29. Why request IDs?
30. What is `before_request`?
31. What is `after_request`?
32. What is a microservice?
33. Why separate database ownership?
34. What is 401?
35. What is 403?
36. What is 404?
37. What is 500?
38. What happens during login?
39. What happens when access token expires?
40. What happens during logout?

---

# 25. One-Minute Project Explanation

If the interviewer says:

> "Explain your project in one minute."

Use this structure:

```text
I developed a standalone Flask Authentication Microservice.

It provides user registration, login, JWT-based authentication,
refresh tokens, protected APIs and logout with JWT revocation.

I used Flask with SQLAlchemy for the API and database layer,
Flask-Migrate for database migrations, and PostgreSQL as the
production database.

The application is Dockerized and runs with Gunicorn in production.
The database is hosted separately as a managed PostgreSQL service.

For observability, I implemented request IDs, rotating logs and
Sentry error monitoring.

The main goal was to keep authentication independently deployable
from the frontend and other backend services.
```

---

# 26. Best Interview Strategy

Do not try to memorize every line of the project.

Understand this flow very clearly:

```text
REQUEST
   ↓
FLASK ROUTE
   ↓
VALIDATION
   ↓
SERVICE LOGIC
   ↓
SQLALCHEMY
   ↓
POSTGRESQL
   ↓
RESPONSE
```

And for authentication:

```text
LOGIN
  ↓
PASSWORD CHECK
  ↓
ACCESS TOKEN
  +
REFRESH TOKEN
  ↓
PROTECTED API
  ↓
TOKEN VALIDATION
  ↓
USER ID
```

And for logout:

```text
LOGOUT
  ↓
GET JTI
  ↓
BLOCKLIST
  ↓
TOKEN REVOKED
```

And for deployment:

```text
CODE
 ↓
DOCKER
 ↓
GUNICORN
 ↓
FLASK
 ↓
MANAGED POSTGRESQL
```

If you can explain these four flows confidently, you will be able to answer a large percentage of interview questions based on this project.
