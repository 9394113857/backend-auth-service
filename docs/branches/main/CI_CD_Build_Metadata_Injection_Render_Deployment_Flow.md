# 🚀 DevOps End-to-End Release Flow (Build Metadata Injection)

## Overview

This document explains the complete CI/CD release flow implemented for the Backend Auth Service using GitHub Actions, Docker Hub, Render, Flask, and Build Metadata Injection.

---

# 🚀 COMPLETE FLOW

```text
Developer
    │
    ▼
Git Commit
    │
    ▼
Git Tag (v1.3.59)
    │
    ▼
GitHub Actions CI
    │
    ▼
Generate build_info.json
    │
    ▼
Docker Build
    │
    ▼
COPY build_info.json into Image
    │
    ▼
Push Docker Image
(v1.3.59)
    │
    ▼
Tag Same Image as latest
    │
    ▼
Push latest
    │
    ▼
GitHub Actions CD
    │
    ▼
Render Deploy Hook
    │
    ▼
Render Pulls latest Image
    │
    ▼
Container Starts
    │
    ▼
Flask Reads build_info.json
    │
    ▼
Dynamic Health Page
```

---

# Step 1: Git Tag Creation

Developer creates a release tag:

```bash
git tag v1.3.59

git push origin v1.3.59
```

GitHub receives the tag and triggers the CI workflow.

---

# Step 2: CI Pipeline Starts

GitHub Actions starts the CI workflow.

The metadata step generates:

```text
VERSION=v1.3.59

COMMIT=a677fbc

BRANCH=main

BUILD_TIME_UTC=...

BUILD_TIME_IST=...
```

These values are stored as GitHub Actions environment variables.

---

# Step 3: Generate build_info.json

CI creates:

```json
{
  "version": "v1.3.59",
  "commit": "a677fbc",
  "branch": "main",
  "build_time_utc": "...",
  "build_time_ist": "..."
}
```

File location:

```text
GitHub Runner

├── app/
├── Dockerfile
├── build_info.json
```

---

# Step 4: Docker Build Starts

CI executes:

```bash
docker build -t backend-auth-service:v1.3.59 .
```

Docker starts processing the Dockerfile.

---

# Step 5: Dockerfile Processing

Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]
```

Important line:

```dockerfile
COPY . .
```

This copies all files into the image including:

```text
build_info.json
```

---

# Docker Image Contents

After build:

```text
Docker Image

/app
 ├── app
 ├── run.py
 ├── requirements.txt
 ├── build_info.json
```

The metadata file is now baked into the Docker image.

---

# Step 6: Push Versioned Docker Image

CI pushes:

```text
pythoncodelife/backend-auth-service:v1.3.59
```

to Docker Hub.

---

# Step 7: Update latest Tag

CI executes:

```bash
docker tag pythoncodelife/backend-auth-service:v1.3.59 \
           pythoncodelife/backend-auth-service:latest

docker push pythoncodelife/backend-auth-service:latest
```

Result:

```text
Docker Hub

backend-auth-service

 ├── v1.3.57
 ├── v1.3.58
 ├── v1.3.59
 └── latest
```

latest now points to v1.3.59.

---

# Step 8: CD Pipeline Starts

GitHub Actions CD workflow executes:

```bash
curl -X POST $RENDER_DEPLOY_HOOK
```

---

# What Deploy Hook Does

The Deploy Hook tells Render:

```text
Redeploy service now.
```

It does not build code.

It does not modify images.

It simply triggers a deployment.

---

# Step 9: Render Pulls Latest Docker Image

Render configuration:

```text
docker.io/pythoncodelife/backend-auth-service:latest
```

Render executes:

```bash
docker pull latest
```

Since latest now points to v1.3.59, Render downloads the newest image.

---

# Step 10: Container Startup

Render starts a new container.

Container contents:

```text
Render Container

/app
 ├── app
 ├── run.py
 ├── build_info.json
```

---

# Step 11: Flask Application Startup

Render executes:

```bash
gunicorn run:app
```

Gunicorn starts Flask.

Flask executes:

```python
create_app()
```

from:

```text
app/__init__.py
```

---

# Step 12: User Opens Browser

Request:

```text
https://backend-auth-service-ks6f.onrender.com
```

hits:

```python
@app.get("/")
```

---

# Step 13: Runtime Metadata Read

Flask executes:

```python
def get_build_info():
    with open("build_info.json") as f:
        return json.load(f)
```

File contents:

```json
{
  "version": "v1.3.59",
  "commit": "a677fbc",
  "branch": "main"
}
```

Flask reads the metadata directly from the running container.

---

# Step 14: Dynamic Health Page Generation

Flask injects:

```python
info.get("version")
info.get("commit")
info.get("branch")
```

into HTML.

Generated output:

```text
🚀 Auth Service
🟢 UP

Version: v1.3.59

Commit: a677fbc...

Branch: main

UTC: ...

IST: ...
```

Browser displays the page.

---

# Why Values Change Automatically

Every release creates:

```text
New Tag
    │
    ▼
New build_info.json
    │
    ▼
New Docker Image
    │
    ▼
New Deployment
```

Therefore Flask always reads the metadata embedded in the newest container.

---

# DevOps Concepts Demonstrated

## CI/CD Pipeline

Automated build, test, packaging and deployment process.

---

## Build Metadata Injection

Injecting version, commit, branch and timestamps during CI execution.

---

## Docker Image Versioning

Versioned container releases using Git tags.

Example:

```text
v1.3.57
v1.3.58
v1.3.59
```

---

## latest Tag Synchronization

Keeping latest aligned with the newest production image.

---

## Containerized Deployment

Application packaged and deployed as immutable Docker images.

---

## Runtime Build Information

Application exposes build metadata at runtime.

---

## Release Traceability

Ability to identify:

```text
Version
Commit SHA
Branch
Build Time
Deployment Time
```

for any running environment.

---

# Interview Answer

"During the CI pipeline, build metadata such as version, commit SHA, branch and timestamps are generated dynamically and stored in build_info.json. During Docker build, the metadata file is packaged into the container image. The image is versioned using Git tags and also synchronized with the latest tag. During CD, Render pulls the latest Docker image and deploys a new container. At runtime, the Flask application reads build_info.json and exposes release metadata through a health endpoint, providing deployment traceability and runtime build visibility."
