FROM python:3.11-slim

WORKDIR /app

COPY ./services/common /app/common
RUN pip install --no-cache-dir /app/common

COPY ./services/iot-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./services/iot-gateway /app

CMD ["python", "main.py"]
