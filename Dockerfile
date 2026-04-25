# =====================================================
# 🐳 DOCKERFILE – AUTH SERVICE (FINAL WITH COMMENTS) 
# =====================================================

# 🔹 Use lightweight Python base image
FROM python:3.11-slim

# 🔹 Set working directory inside container
WORKDIR /app

# 🔥 Build-time arguments (coming from CI)
# These help track version, commit, branch
ARG APP_VERSION=dev
ARG APP_COMMIT=local
ARG APP_BRANCH=local

# 📦 Copy only requirements first (for better caching)
COPY requirements.txt .

# 📦 Install dependencies (no cache → smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copy full project code into container
COPY . .

# 🧾 Generate build metadata file (used in your health API)
RUN python - <<EOF
import json
from datetime import datetime, timezone, timedelta

ist = timezone(timedelta(hours=5, minutes=30))

data = {
    "version": "${APP_VERSION}",
    "commit": "${APP_COMMIT}",
    "branch": "${APP_BRANCH}",
    "build_time_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "build_time_ist": datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")
}

with open("build_info.json", "w") as f:
    json.dump(data, f, indent=2)
EOF

# 🌐 Expose port (documentation purpose for container tools)
EXPOSE 5000

# 🚀 Run Flask app using Gunicorn (production-ready)
# Fixed port 5000 → Kubernetes compatible
CMD ["gunicorn", "run:app", "-w", "1", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-"]