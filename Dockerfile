# =========================
# 🐳 AUTH SERVICE DOCKERFILE
# =========================

FROM python:3.11-slim

WORKDIR /app

# Build args
ARG APP_VERSION
ARG APP_COMMIT
ARG APP_BRANCH

# Runtime env
ENV APP_VERSION=$APP_VERSION
ENV APP_COMMIT=$APP_COMMIT
ENV APP_BRANCH=$APP_BRANCH

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Copy entrypoint explicitly
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 5000

# Start container
ENTRYPOINT ["/entrypoint.sh"]