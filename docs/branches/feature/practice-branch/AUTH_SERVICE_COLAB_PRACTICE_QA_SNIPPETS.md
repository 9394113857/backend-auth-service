# Auth Service — Google Colab Practice Questions, Answers & Small Code Snippets

This document is designed for **Google Colab practice**.

The examples are intentionally small and focus on concepts used in the Auth Service:

* `try / except`
* `IntegrityError`
* `rollback()`
* `commit()`
* SQLAlchemy
* User creation
* Duplicate data
* Password hashing
* Queries
* JWT basics
* Request IDs
* Logging
* Flask API basics

---

# 1. IntegrityError — Basic

## Question

What happens if we insert duplicate data into a database column having a unique constraint?

## Answer

The database can raise an `IntegrityError`.

We catch it and rollback the transaction.

## Small Snippet

```python
try:
    db.session.add(user)
    db.session.commit()

except IntegrityError:
    db.session.rollback()
```

---

# 2. Why rollback()?

## Question

Why do we use `rollback()` after an `IntegrityError`?

## Answer

Because the database transaction has failed.

`rollback()` returns the session to a clean state so another database operation can be performed.

## Small Snippet

```python
try:
    db.session.commit()

except IntegrityError:
    db.session.rollback()
```

---

# 3. Duplicate Email

## Question

How would you handle duplicate user registration?

## Answer

Make email unique in the database and catch `IntegrityError`.

## Model

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )
```

## Registration

```python
try:
    db.session.add(user)
    db.session.commit()

except IntegrityError:
    db.session.rollback()
    print("User already exists")
```

---

# 4. commit() vs rollback()

## Question

What is the difference between `commit()` and `rollback()`?

## Answer

`commit()` saves the transaction.

`rollback()` cancels the failed/uncommitted transaction.

```python
db.session.add(user)

db.session.commit()
```

If something fails:

```python
db.session.rollback()
```

---

# 5. try / except

## Question

Why use `try / except` around database operations?

## Answer

To catch expected database exceptions and handle them safely.

```python
try:
    db.session.commit()

except IntegrityError:
    db.session.rollback()
    print("Database error")
```

---

# 6. Create a User

## Question

How do you create a SQLAlchemy user object?

## Answer

Create an instance of the model.

```python
user = User(
    email="test@example.com",
    role="user"
)
```

Then:

```python
db.session.add(user)
db.session.commit()
```

---

# 7. Complete Small Registration

## Question

Write a simple registration function.

## Answer

```python
def register(email):
    try:
        user = User(email=email)

        db.session.add(user)
        db.session.commit()

        return "Created"

    except IntegrityError:
        db.session.rollback()
        return "Already exists"
```

---

# 8. Return HTTP Status

## Question

How can the service return a response and HTTP status?

## Answer

Return a tuple.

```python
return {
    "message": "Created"
}, 201
```

For duplicate:

```python
return {
    "message": "Already exists"
}, 400
```

---

# 9. Password Hashing

## Question

Should we store the user's password directly?

## Answer

No. Store a password hash.

```python
from werkzeug.security import generate_password_hash

password_hash = generate_password_hash("secret123")
```

---

# 10. Password Verification

## Question

How do you verify a password?

## Answer

Use `check_password_hash()`.

```python
from werkzeug.security import check_password_hash

ok = check_password_hash(
    password_hash,
    "secret123"
)
```

---

# 11. Small User Model

## Question

Create a simple user model.

## Answer

```python
class User(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(150),
        unique=True
    )
```

---

# 12. Query a User

## Question

How do you find a user by email?

## Answer

```python
user = User.query.filter_by(
    email=email
).first()
```

---

# 13. What does first() do?

## Question

What does `.first()` do?

## Answer

It returns the first matching record or `None` if no record exists.

```python
user = User.query.filter_by(
    email="a@example.com"
).first()
```

---

# 14. User Not Found

## Question

How do you check whether a user exists?

## Answer

```python
user = User.query.filter_by(
    email=email
).first()

if not user:
    print("User not found")
```

---

# 15. Duplicate Check Before Insert

## Question

Can we check for an existing email before inserting?

## Answer

Yes.

```python
user = User.query.filter_by(
    email=email
).first()

if user:
    return "Already exists"
```

However, the database's unique constraint should still remain because application-level checks alone are not enough under concurrent requests.

---

# 16. Duplicate Check + IntegrityError

## Question

What is the safer pattern?

## Answer

Use an application check for a friendly response, but also keep the database unique constraint and catch `IntegrityError`.

```python
user = User.query.filter_by(
    email=email
).first()

if user:
    return "Already exists"

try:
    db.session.add(User(email=email))
    db.session.commit()

except IntegrityError:
    db.session.rollback()
    return "Already exists"
```

---

# 17. Why Database Constraint Matters

## Question

Why not only check if the email exists?

## Answer

Because two requests can arrive at almost the same time.

```text
Request A → email not found
Request B → email not found

Request A → insert
Request B → insert
```

The database unique constraint is the final protection.

---

# 18. Multiple Database Operations

## Question

What happens if one of several database operations fails?

## Answer

The transaction can be rolled back.

```python
try:
    db.session.add(user)
    db.session.add(token)

    db.session.commit()

except IntegrityError:
    db.session.rollback()
```

---

# 19. Logging After Commit

## Question

Why log after `commit()`?

## Answer

Because the database operation has successfully completed.

```python
db.session.add(user)
db.session.commit()

current_app.logger.info(
    f"User created id={user.id}"
)
```

---

# 20. Request ID

## Question

Why use `g.request_id`?

## Answer

It helps trace logs belonging to the same HTTP request.

```python
current_app.logger.info(
    f"[REQ:{g.request_id}] User created"
)
```

---

# 21. `current_app`

## Question

Why use `current_app.logger` instead of a global Flask `app`?

## Answer

`current_app` gives access to the currently active Flask application inside application context.

```python
current_app.logger.info(
    "User created"
)
```

---

# 22. Complete Auth-Service Style Function

## Question

Write a small version of the registration logic from the project.

## Answer

```python
def register_user(email, password, role="user"):

    try:
        user = User(
            email=email,
            role=role
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return {
            "message": "Created",
            "role": user.role
        }, 201

    except IntegrityError:
        db.session.rollback()

        return {
            "message": "Already exists"
        }, 400
```

---

# 23. What If commit() Fails?

## Question

What should happen if `commit()` raises `IntegrityError`?

## Answer

Rollback the session.

```python
try:
    db.session.commit()

except IntegrityError:
    db.session.rollback()
```

---

# 24. What If We Forget rollback()?

## Question

What can happen if we don't rollback after a failed transaction?

## Answer

The SQLAlchemy session can remain in a failed transaction state, causing later database operations to fail until the session is rolled back.

Remember:

```text
Error
 ↓
rollback()
 ↓
Session usable again
```

---

# 25. JWT — Small Practice

## Question

How do you create an access token?

## Answer

```python
access_token = create_access_token(
    identity=str(user.id)
)
```

---

# 26. JWT Identity

## Question

How do you get the user ID from the JWT?

## Answer

```python
user_id = get_jwt_identity()
```

---

# 27. Protected Route

## Question

How do you protect a Flask route with JWT?

## Answer

```python
@jwt_required()
def profile():
    return {
        "user_id": get_jwt_identity()
    }
```

---

# 28. Refresh Token

## Question

How do you require a refresh token?

## Answer

```python
@jwt_required(refresh=True)
def refresh():
    ...
```

---

# 29. JWT JTI

## Question

How do you get the JTI?

## Answer

```python
jti = get_jwt()["jti"]
```

---

# 30. Blocklist

## Question

How do you store a revoked JWT?

## Answer

```python
jti = get_jwt()["jti"]

db.session.add(
    TokenBlocklist(jti=jti)
)

db.session.commit()
```

---

# 31. Blocklist Check

## Question

How can you check whether a JTI was revoked?

## Answer

```python
token = TokenBlocklist.query.filter_by(
    jti=jti
).first()

revoked = token is not None
```

---

# 32. Simple API

## Question

Write a tiny Flask API.

## Answer

```python
@app.get("/hello")
def hello():
    return {
        "message": "Hello"
    }
```

---

# 33. GET vs POST

## Question

When would you use GET and POST?

## Answer

```text
GET
→ Retrieve data

POST
→ Create/send data
```

Example:

```python
@app.get("/users")
def users():
    ...
```

```python
@app.post("/users")
def create_user():
    ...
```

---

# 34. Read JSON

## Question

How do you read JSON from a Flask request?

## Answer

```python
data = request.get_json() or {}
```

Then:

```python
email = data.get("email")
```

---

# 35. Validate Input

## Question

How do you check required fields?

## Answer

```python
if not email or not password:
    return {
        "message": "Required"
    }, 400
```

---

# 36. HTTP 201

## Question

Why use status `201` after registration?

## Answer

Because a new user resource was created.

```python
return {
    "message": "Created"
}, 201
```

---

# 37. HTTP 400

## Question

When would you return 400?

## Answer

For an invalid client request.

Example:

```python
if not email:
    return {
        "message": "Email required"
    }, 400
```

---

# 38. HTTP 401

## Question

When would you return 401?

## Answer

When authentication fails.

```python
return {
    "message": "Invalid credentials"
}, 401
```

---

# 39. Colab Python Practice — Exception

## Question

Write a simple exception example.

## Answer

```python
try:
    number = 10 / 0

except ZeroDivisionError:
    print("Cannot divide by zero")
```

---

# 40. Colab Practice — Custom Duplicate Simulation

## Question

Practice the same idea as `IntegrityError` without a database.

## Answer

```python
users = {"a@example.com"}

email = "a@example.com"

try:
    if email in users:
        raise ValueError("Duplicate")

except ValueError:
    print("User already exists")
```

This is only a Python practice exercise.

---

# 41. Colab Practice — Transaction Thinking

## Question

Explain this flow.

```python
try:
    add_user()
    save_user()
    commit()

except Exception:
    rollback()
```

## Answer

The operations are treated as one logical transaction.

If a failure occurs, rollback prevents a partially completed transaction from being left behind.

---

# 42. Interview Coding Question

## Question

Write a function that safely inserts a user and handles duplicate email.

## Answer

```python
def add_user(email):

    try:
        user = User(email=email)

        db.session.add(user)
        db.session.commit()

        return "Created"

    except IntegrityError:
        db.session.rollback()

        return "Duplicate"
```

---

# 43. Interview Coding Question

## Question

Write a function to find a user.

## Answer

```python
def find_user(email):

    return User.query.filter_by(
        email=email
    ).first()
```

---

# 44. Interview Coding Question

## Question

Write a simple login check.

## Answer

```python
user = User.query.filter_by(
    email=email
).first()

if user and user.check_password(password):
    print("Login successful")
else:
    print("Invalid login")
```

---

# 45. Interview Coding Question

## Question

Create access and refresh tokens.

## Answer

```python
access = create_access_token(
    identity=str(user.id)
)

refresh = create_refresh_token(
    identity=str(user.id)
)
```

---

# 46. Interview Coding Question

## Question

Write a logout blocklist operation.

## Answer

```python
jti = get_jwt()["jti"]

db.session.add(
    TokenBlocklist(jti=jti)
)

db.session.commit()
```

---

# 47. Interview Coding Question

## Question

How do you handle a database error safely?

## Answer

```python
try:
    db.session.commit()

except IntegrityError:
    db.session.rollback()
```

---

# 48. Most Important IntegrityError Questions

For your interview, practice these especially:

### Question 1

What is `IntegrityError`?

**Answer:** A database constraint/integrity violation.

### Question 2

Why can duplicate registration cause it?

**Answer:** Because `email` is marked `unique=True`.

### Question 3

What should you do after catching it?

**Answer:** Call `db.session.rollback()`.

### Question 4

Why is rollback necessary?

**Answer:** The SQLAlchemy transaction/session needs to be returned to a usable state.

### Question 5

Should you remove the database unique constraint and only check in Python?

**Answer:** No. Application checks are useful, but the database constraint provides the final protection against concurrent duplicate inserts.

### Question 6

What status does your service return?

**Answer:**

```text
400
```

with:

```json
{
  "message": "User already exists"
}
```

---

# 49. The Core Pattern to Memorize

For database operations, remember:

```python
try:
    db.session.add(object)
    db.session.commit()

except IntegrityError:
    db.session.rollback()
```

Think:

```text
ADD
 ↓
COMMIT
 ↓
SUCCESS

ERROR
 ↓
ROLLBACK
```

---

# 50. Final Practice Order

Practice these in this order:

```text
1. try / except
2. commit()
3. rollback()
4. IntegrityError
5. unique=True
6. SQLAlchemy model
7. SQLAlchemy query
8. password hashing
9. login validation
10. JWT access token
11. JWT refresh token
12. JWT identity
13. JWT JTI
14. token blocklist
15. Flask Blueprint
16. before_request
17. after_request
18. request ID
19. logging
20. Sentry
21. Flask-Migrate
22. PostgreSQL
23. Docker
24. Gunicorn
25. Microservice architecture
```

## One Key Interview Explanation

If the interviewer asks:

> "Explain the `IntegrityError` handling in your registration code."

Answer:

> "The email column has a unique constraint. During registration I add the user and commit the transaction. If the database detects a duplicate email, SQLAlchemy raises `IntegrityError`. I catch that exception, call `db.session.rollback()` to reset the failed transaction, log the event with the request ID, and return a `400` response saying that the user already exists."

Small code:

```python
try:
    db.session.add(user)
    db.session.commit()

except IntegrityError:
    db.session.rollback()

    return {
        "message": "User already exists"
    }, 400
```

This is the **main pattern from your current Auth Service that you should be able to explain confidently in an interview.**
