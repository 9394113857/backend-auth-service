# =====================================================
# 🐳 DOCKERFILE – AUTH SERVICE (FINAL - RUNTIME BUILD INFO)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

# 🔥 Build args (from CI)
ARG APP_VERSION
ARG APP_COMMIT
ARG APP_BRANCH

# 🔥 Convert to ENV (used at runtime)
ENV APP_VERSION=$APP_VERSION
ENV APP_COMMIT=$APP_COMMIT
ENV APP_BRANCH=$APP_BRANCH

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

# 🚀 Start app via entrypoint
ENTRYPOINT ["/entrypoint.sh"]