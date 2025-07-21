# syntax=

FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./backend /app/backend
COPY ./cli /app/cli
COPY ./tests /app/tests

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
