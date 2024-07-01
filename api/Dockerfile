FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y netcat-openbsd && pip install --no-cache-dir -r requirements.txt

COPY src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app
COPY main.py /app
COPY wait-for-it.sh /app
COPY start.sh /app

CMD ["./wait-for-it.sh", "kafka", "--", "sh", "./start.sh"]