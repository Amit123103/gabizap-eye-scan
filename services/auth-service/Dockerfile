FROM python:3.11-slim

WORKDIR /app

COPY ./services/common /app/common
RUN pip install --no-cache-dir /app/common

COPY ./services/auth-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./services/auth-service /app

COPY ./services/auth-service/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
