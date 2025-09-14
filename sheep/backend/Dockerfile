# Use the official Python image.
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose the port Railway will use
EXPOSE 8000

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
