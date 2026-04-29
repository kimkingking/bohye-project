# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for mysql-connector)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the application port
EXPOSE 3000

# Define environment variables with defaults
ENV DB_HOST=mysql-service
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_NAME=diet_db

# Command to run the application
CMD ["python", "app.py"]
