# Install Dependencies
FROM python:3.11-slim as builder

# Set ENV variables for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /app

# Install system dependencies for psycopg2 (Postgres driver)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    gettext \
    && rm -rf var/lib/apt/lists/*

# Copy only requirements.txt to use Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final Image
FROM python:3.11-slim

WORKDIR /app

# Copy previously installed packeges from builder
COPY --from=builder /install /usr/local

# Install runtime libraries for Postgres
RUN apt-get update && apt-get install -y \
    gettext \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy everithing else
COPY . .

# Expose Django port
EXPOSE 8000

# Start command using dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]