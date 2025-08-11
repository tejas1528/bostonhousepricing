FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the code
COPY . .

# Expose port (Render provides $PORT env)
EXPOSE $PORT

# Start Gunicorn
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:${PORT}", "app:app"]
