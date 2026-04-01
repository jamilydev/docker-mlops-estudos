# Define a imagem base enxuta (menor tamanho, ideal para economizar recursos na nuvem)
FROM python:3.10-slim
# Cria e define a pasta de trabalho isolada dentro do container
# junção dos comandos MKDIR E CD
WORKDIR /app
# Copia APENAS o arquivo de dependências primeiro (Estratégia de Cache do Docker)
COPY requirements.txt .
# Instala as bibliotecas da API sem guardar lixo temporário (--no-cache-dir)
RUN pip install --no-cache-dir -r requirements.txt
# Copia o código da API
COPY main.py .
# Sinaliza e documenta qual porta o nosso modelo usará para se comunicar
EXPOSE 8000
# Liga o servidor, liberando acesso externo (--host 0.0.0.0) 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]