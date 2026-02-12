FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY ./services/common /app/common
RUN pip install --no-cache-dir /app/common

COPY ./services/iris-engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./services/iris-engine /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
