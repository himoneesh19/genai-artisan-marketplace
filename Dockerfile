# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install cron and curl
RUN apt-get update && apt-get install -y cron curl && rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Copy start.sh script and make it executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Add crontab entry to ping localhost every 10 minutes
RUN echo "*/10 * * * * curl -fsS http://localhost:5000 > /dev/null 2>&1" > /etc/cron.d/ping-cron \
    && chmod 0644 /etc/cron.d/ping-cron \
    && crontab /etc/cron.d/ping-cron

# Expose port 5000 for the Flask app
EXPOSE 5000

# Use start.sh as entrypoint to start cron and Flask app
ENTRYPOINT ["/app/start.sh"]
