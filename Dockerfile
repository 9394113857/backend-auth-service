# 1. Use lightweight Python image
FROM python:3.11-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy dependency file first (for Docker layer caching)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Expose Flask port (informational only, Render ignores this)
EXPOSE 5001

# 7. DIAGNOSTIC COMMAND (TEMPORARY)
# ------------------------------------------------------------
# Purpose:
# - Print the PORT variable injected by Render
# - Print ALL environment variables
# - Keep the container alive for 5 minutes
#
# Why:
# - Render currently exits the container before logs appear
# - This forces stdout to be visible so we can debug
#
# IMPORTANT:
# - This is NOT the final command
# - We will revert to Gunicorn after diagnosis
# ------------------------------------------------------------
CMD ["sh", "-c", "echo '=== PORT VALUE ===' && echo PORT=$PORT && echo '=== ALL ENV VARS ===' && env && echo '=== CONTAINER HOLD ===' && sleep 300"]
