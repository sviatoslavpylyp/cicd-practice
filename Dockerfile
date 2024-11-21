# build stage
FROM python:3.9-slim AS build

WORKDIR /app

COPY requirements.txt .
COPY init_db.sql /docker-entrypoint-initdb.d/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

# runtime stage
FROM python:3.9-slim AS runtime

WORKDIR /app

# Copy application from build stage
COPY --from=build /app /app

# Install Flask CLI in runtime stage to ensure flask command is available
RUN pip install flask

EXPOSE 5000

# Environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["flask", "run"]
