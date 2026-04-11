# =====================================================
# 🐳 DOCKERFILE – FINAL FIXED
# =====================================================

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything INCLUDING build_info.json from CI
COPY . .

CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT"]