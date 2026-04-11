# =====================================================
# 🐳 DOCKERFILE – FINAL FIXED (NO METADATA GENERATION)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy EVERYTHING from CI (INCLUDING build_info.json)
COPY . .

# 🚨 IMPORTANT: DO NOT regenerate build_info.json here

CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT"]