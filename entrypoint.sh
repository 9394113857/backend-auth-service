#!/bin/sh

# 🔥 Generate build info at runtime (NO CACHE ISSUE)
python <<EOF
import json
from datetime import datetime, timezone, timedelta
import os

ist = timezone(timedelta(hours=5, minutes=30))

data = {
    "version": os.getenv("APP_VERSION", "unknown"),
    "commit": os.getenv("APP_COMMIT", "unknown"),
    "branch": os.getenv("APP_BRANCH", "unknown"),
    "build_time_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "build_time_ist": datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")
}

with open("build_info.json", "w") as f:
    json.dump(data, f, indent=2)
EOF

# 🚀 Start Gunicorn
exec gunicorn run:app -w 1 -b 0.0.0.0:5000 --access-logfile - --error-logfile -