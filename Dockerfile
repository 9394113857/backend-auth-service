# =====================================================
# 🐳 DOCKERFILE – FINAL (IMMUTABLE BUILD INFO)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

# 🔥 Build arguments from CI
ARG APP_VERSION
ARG APP_COMMIT

# 🔥 Write build info into file (IMMUTABLE)
RUN echo "{\"version\": \"$APP_VERSION\", \"commit\": \"$APP_COMMIT\"}" > /app/build_info.json

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run app
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]
