# build stage
FROM python:3.9-slim AS build

WORKDIR app

COPY requirements.txt .
COPY init_db.sql /docker-entrypoint-initdb.d/

RUN pip install --no-cache-dir -r requirements.txt

COPY app .

FROM python:3.9-slim AS runtime

WORKDIR /app

COPY --from=build /app /app

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]
