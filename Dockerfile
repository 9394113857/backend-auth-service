# =====================================================
# 🐳 DOCKERFILE – AUTH SERVICE (FIXED BUILD INFO)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

# 🔥 Build args
ARG APP_VERSION=dev
ARG APP_COMMIT=local
ARG APP_BRANCH=local

# 🔥 FORCE CACHE BREAK (VERY IMPORTANT)
RUN echo "BUILD_ID=${APP_COMMIT}"

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# 🔥 ALWAYS regenerate build_info.json
RUN rm -f build_info.json && python - <<EOF
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