# Define a imagem base enxuta (menor tamanho, ideal para economizar recursos na nuvem)
FROM python:3.10-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/*.py .
EXPOSE 8000
# Liga o servidor, liberando acesso externo (--host 0.0.0.0) 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]