FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY appp.py .
COPY templates/ templates/

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=appp.py
ENV FLASK_ENV=production

# Run the application using Gunicorn for production
# Use a simple worker count; adjust based on available CPU
CMD ["python", "appp.py"]
