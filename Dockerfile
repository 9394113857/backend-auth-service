# =====================================================
# 🐳 DOCKERFILE – AUTH SERVICE (FINAL FIXED NO CACHE BUG)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

ARG APP_VERSION=dev
ARG APP_COMMIT=local
ARG APP_BRANCH=local

# Install deps first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full code
COPY . .

# 🔥 FORCE CACHE BREAK HERE (IMPORTANT)
RUN echo "BUILD_ID=${APP_COMMIT}"

# 🔥 ALWAYS regenerate build info AFTER cache break
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

EXPOSE 5000

CMD ["gunicorn", "run:app", "-w", "1", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-"]