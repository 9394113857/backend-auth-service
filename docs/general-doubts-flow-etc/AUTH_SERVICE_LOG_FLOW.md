# 🔐 Auth Service – Registration & Login Flow (Log Analysis)

This document explains the **exact sequence of API calls** observed while testing the **Auth Service** locally using an Angular frontend.

It decodes Flask logs into a **clear developer-readable flow**, covering:
- Seller registration & login
- Customer registration & login
- CORS preflight behavior
- HTTP status codes and outcomes

---

## 🚀 Service Startup

```text
flask run --port 5001

•	Auth Service started successfully
•	Running on http://127.0.0.1:5001
•	Debug mode: OFF (production-like behavior)

•	Auth Service started successfully
•	Running on http://127.0.0.1:5001
•	Debug mode: OFF (production-like behavior)
________________________________________
🧠 High-Level Flow Summary
1.	Seller registers
2.	Seller attempts login (wrong password → fail)
3.	Seller logs in successfully
4.	Customer registers
5.	Customer attempts login (wrong password → fail)
6.	Customer logs in successfully
All OPTIONS requests are CORS preflight checks triggered by the browser (Angular).
________________________________________
📊 Full Request–Response Log Breakdown

| S.No | HTTP Method | Endpoint                            | User Role | Action         | Result  | Status Code | Notes                                  |
| ---- | ----------- | ----------------------------------- | --------- | -------------- | ------- | ----------- | -------------------------------------- |
| 1    | —           | —                                   | —         | Service start  | Running | —           | Flask Auth Service booted on port 5001 |
| 2    | OPTIONS     | `/api/v1/auth/angularUser/register` | Seller    | CORS preflight | Allowed | 200         | Browser permission check               |
| 3    | POST        | `/api/v1/auth/angularUser/register` | Seller    | Register       | Success | 201         | Seller created (id=1)                  |
| 4    | OPTIONS     | `/api/v1/auth/angularUser/login`    | Seller    | CORS preflight | Allowed | 200         | Preflight before login                 |
| 5    | POST        | `/api/v1/auth/angularUser/login`    | Seller    | Login          | Failed  | 401         | Invalid credentials                    |
| 6    | OPTIONS     | `/api/v1/auth/angularUser/login`    | Seller    | CORS preflight | Allowed | 200         | Retry login                            |
| 7    | POST        | `/api/v1/auth/angularUser/login`    | Seller    | Login          | Success | 200         | JWT issued                             |
| 8    | OPTIONS     | `/api/v1/auth/angularUser/register` | Customer  | CORS preflight | Allowed | 200         | Preflight for register                 |
| 9    | POST        | `/api/v1/auth/angularUser/register` | Customer  | Register       | Success | 201         | Customer created (id=2)                |
| 10   | OPTIONS     | `/api/v1/auth/angularUser/login`    | Customer  | CORS preflight | Allowed | 200         | Preflight for login                    |
| 11   | POST        | `/api/v1/auth/angularUser/login`    | Customer  | Login          | Failed  | 401         | Invalid credentials                    |
| 12   | OPTIONS     | `/api/v1/auth/angularUser/login`    | Customer  | CORS preflight | Allowed | 200         | Retry login                            |
| 13   | POST        | `/api/v1/auth/angularUser/login`    | Customer  | Login          | Success | 200         | JWT issued                             |

🔐 API Behavior Explained
🔹 Registration Endpoint
POST /api/v1/auth/angularUser/register

•	Creates a new user
•	Hashes password
•	Stores role (seller or user)
•	Returns 201 Created
________________________________________
🔹 Login Endpoint

POST /api/v1/auth/angularUser/login

•	Validates email
•	Verifies hashed password
•	Issues JWT on success
•	Returns:
o	200 OK → Login success
o	401 Unauthorized → Wrong credentials
________________________________________
🌐 Why OPTIONS Requests Appear
Browsers enforce CORS security.
Before every POST request:

OPTIONS /login
OPTIONS /register

✔ Normal
✔ Expected
✔ Required for frontend-backend communication

✅ Final Validation
•	✔ Auth service is stable
•	✔ Registration works
•	✔ Login works
•	✔ JWT generation works
•	✔ Angular ↔ Flask integration works
•	✔ No errors or inconsistencies detected
________________________________________
📌 Notes for Future Developers
•	Always ignore OPTIONS logs during debugging
•	Focus on POST responses for business logic
•	Never log raw passwords
•	JWT should be sent in Authorization header for protected routes
________________________________________
📄 Document Purpose
This file serves as API flow documentation and debug reference for authentication testing.


---

If you want next, I can:
- Create **logout flow documentation**
- Add **JWT lifecycle diagram**
- Merge this into a **main README**
- Create **API contract documentation**

Just say 👍

