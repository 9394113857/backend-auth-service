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

# 6. Expose Flask port (informational only)
EXPOSE 5001

# 7. Run app using Gunicorn
# - sh -c is required to expand $PORT
# - access/error logs are sent to stdout for Render visibility
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --log-level debug --access-logfile - --error-logfile -"]
