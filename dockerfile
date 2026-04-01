# Define a imagem base enxuta (menor tamanho, ideal para economizar recursos na nuvem)
FROM python:3.10-slim

WORKDIR /app
# Copia o arquivo de dependências para o diretório de trabalho no container
COPY backend/requirements.txt .
# Instala as dependências do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copia os arquivos Python do diretório backend para o diretório de trabalho no container
COPY backend/*.py .
# Expõe a porta 8000 para acesso externo (a porta padrão do FastAPI)
EXPOSE 8000
# Liga o servidor, liberando acesso externo (--host 0.0.0.0) 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]