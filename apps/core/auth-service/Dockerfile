FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir .

COPY app /app/auth-service/

CMD [ "uvicorn", "auth-service.main:app", "--host", "0.0.0.0", "--port", "8080" ]
