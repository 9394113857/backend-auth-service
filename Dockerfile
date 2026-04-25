# =====================================================
# 🐳 DOCKERFILE – AUTH SERVICE (FINAL)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

# Build args from CI
ARG APP_VERSION
ARG APP_COMMIT
ARG APP_BRANCH

# Make available at runtime
ENV APP_VERSION=$APP_VERSION
ENV APP_COMMIT=$APP_COMMIT
ENV APP_BRANCH=$APP_BRANCH

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Entrypoint for runtime build info
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]