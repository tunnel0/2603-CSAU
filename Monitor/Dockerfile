# Use official Python lightweight image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Give execution rights to the start script
RUN chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]
