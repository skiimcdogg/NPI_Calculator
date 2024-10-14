FROM python:3.9.13-slim

RUN apt-get update && apt-get install -y \
    python3-tk \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    libsqlite3-dev \
    libreadline-dev \
    libtk8.6 libnss3 libx11-6 libxext6 libxrender1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]