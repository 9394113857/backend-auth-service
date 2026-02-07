# =========================================================
# FINAL PRODUCTION DOCKERFILE (RENDER + DOCKER SAFE)
# =========================================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (informational only)
EXPOSE 5001

# Start app using Gunicorn
# - sh -c required to expand $PORT
# - logs go to stdout for Render
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]
