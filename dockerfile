# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Expose app port
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
