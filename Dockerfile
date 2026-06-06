FROM python:3.11-slim

# Instalar ffmpeg e dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências Python
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Diretório temporário de uploads
RUN mkdir -p /tmp/k-videotrim_uploads

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
