FROM python:3.11-slim

WORKDIR /app

COPY ./services/common /app/common
RUN pip install --no-cache-dir /app/common

COPY ./services/matcher/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./services/matcher /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006"]
