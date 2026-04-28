#!/bin/sh
# =====================================================
# 🚀 ENTRYPOINT SCRIPT – AUTH SERVICE
# =====================================================

# 👉 This script runs when the container starts

# =====================================================
# 🧾 GENERATE BUILD INFO (RUNTIME METADATA)
# =====================================================
# We create build_info.json so the app can display:
# version, commit, branch, and timestamps

python <<EOF
import json
from datetime import datetime, timezone, timedelta
import os

# IST timezone setup
ist = timezone(timedelta(hours=5, minutes=30))

# Build metadata (from Docker build args → ENV)
data = {
    "version": os.getenv("APP_VERSION", "unknown"),   # app version
    "commit": os.getenv("APP_COMMIT", "unknown"),     # git commit SHA
    "branch": os.getenv("APP_BRANCH", "unknown"),     # git branch name
    "build_time_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "build_time_ist": datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")
}

# Write metadata file
with open("build_info.json", "w") as f:
    json.dump(data, f, indent=2)
EOF


# =====================================================
# 🐳 START APPLICATION (GUNICORN) 
# =====================================================
# run:app → from run.py (Flask app factory)
# -w 1    → number of workers (can scale later)
# -b      → bind to all interfaces on port 5000

exec gunicorn run:app \
  -w 1 \
  -b 0.0.0.0:5000 \
  --access-logfile - \
  --error-logfile -