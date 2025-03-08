FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ /app/

# Create uploads directory
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# Set environment variables
ENV API_KEY=""
ENV BASE_URL="http://localhost"

# Expose port 80
EXPOSE 80

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
