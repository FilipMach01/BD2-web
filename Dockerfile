FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# SECRET_KEY je potřeba jen pro collectstatic (ne pro runtime) – runtime dostane klíč z .env
RUN SECRET_KEY=dummy-build-only DATABASE_URL=sqlite:////tmp/build.db python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "bd_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
