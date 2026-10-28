# Small official Python image
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first: Docker caches this layer, so rebuilds are fast
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy our code
COPY . .

EXPOSE 5000

# gunicorn = production web server (Flask's built-in one is for development only)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
