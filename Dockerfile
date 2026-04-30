# =====================================================
# 🐳 DOCKERFILE – AUTH SERVICE (FINAL)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

# 📦 Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copy project (includes build_info.json from CI)
COPY . .

# 🚀 Run app
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]
