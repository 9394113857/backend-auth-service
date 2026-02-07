# 1. Use lightweight Python image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy dependency file first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project files
COPY . .

# 6. Expose Flask port (informational for Docker only)
EXPOSE 5001

# 7. Run app using Gunicorn (Render + Docker safe)
# NOTE:
# - Render injects PORT at runtime
# - Exec-form CMD does NOT expand env vars
# - So we use 'sh -c' to expand $PORT correctly
CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:$PORT run:app"]
