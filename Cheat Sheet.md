# 📋 Cheat Sheet — Dockerfile & Docker Compose

> Guia de referência rápida para o Grupo de Estudos MLOps — **INF/UFG · CEIA**

---

## 📁 Como usar este material

Esta pasta faz parte do repositório do workshop. Consulte aqui sempre que precisar lembrar a função de um comando ou instrução durante seus projetos de MLOps.

---

## 🐳 Parte 1 — Dockerfile

O **Dockerfile** é o arquivo que define como sua imagem Docker é construída. Cada linha é uma **instrução** que vira uma camada da imagem.

### Estrutura básica

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### 📌 Instruções do Dockerfile

| Instrução | Sintaxe | O que faz |
|-----------|---------|-----------|
| `FROM` | `FROM python:3.10-slim` | Define a imagem base. Ponto de partida obrigatório de todo Dockerfile. |
| `WORKDIR` | `WORKDIR /app` | Define o diretório de trabalho dentro do container. Todos os comandos seguintes rodam a partir daqui. |
| `COPY` | `COPY origem destino` | Copia arquivos do seu computador para dentro da imagem. |
| `RUN` | `RUN pip install -r requirements.txt` | Executa um comando durante o **build** da imagem. Usado para instalar dependências. |
| `EXPOSE` | `EXPOSE 8000` | Documenta qual porta a aplicação usa. Não publica a porta — isso é feito no `docker run`. |
| `CMD` | `CMD ["uvicorn", "main:app"]` | Define o comando padrão executado quando um container sobe. Pode ser substituído no `docker run`. |
| `ENTRYPOINT` | `ENTRYPOINT ["python"]` | Similar ao CMD, mas não pode ser substituído facilmente. Usado quando o container tem um propósito fixo. |
| `ENV` | `ENV APP_ENV=production` | Define variáveis de ambiente disponíveis dentro do container. |
| `ARG` | `ARG VERSAO=1.0` | Variável usada **apenas durante o build**, não fica no container final. |
| `VOLUME` | `VOLUME /data` | Marca um diretório como ponto de montagem para volumes externos. |
| `USER` | `USER appuser` | Define com qual usuário os comandos seguintes são executados. Boa prática de segurança. |
| `LABEL` | `LABEL maintainer="equipe@ufg.br"` | Adiciona metadados à imagem (autor, versão, descrição). |

---

### 💡 Boas práticas do Dockerfile

**1. Use imagens base leves**
```dockerfile
# ✅ Preferido — centenas de MB a menos
FROM python:3.10-slim

# ❌ Evite — carrega pacotes que você não vai usar
FROM python:3.10
```

**2. Instale dependências ANTES de copiar o código**
```dockerfile
# ✅ Correto — aproveita cache de camadas
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .                            # só copia o código por último

# ❌ Errado — qualquer mudança no código invalida o cache do pip
COPY . .
RUN pip install -r requirements.txt
```

> **Por que isso importa?** O Docker guarda cache de cada camada. Se só o código mudou, ele reutiliza a camada do `pip install` e o build fica muito mais rápido.

**3. Use `--no-cache-dir` no pip**
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
# Evita salvar cache do pip dentro da imagem, reduzindo o tamanho final
```

**4. Combine RUNs quando possível**
```dockerfile
# ✅ Uma camada só
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# ❌ Três camadas desnecessárias
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*
```

---

### ⚡ Comandos de build e run

| Comando | O que faz |
|---------|-----------|
| `docker build -t nome-imagem .` | Constrói a imagem usando o Dockerfile no diretório atual. |
| `docker build -t nome:v1.0 .` | Constrói a imagem com uma tag de versão. |
| `docker build --no-cache -t nome .` | Constrói ignorando o cache — útil para forçar reinstalação de dependências. |
| `docker run nome-imagem` | Sobe um container a partir da imagem. |
| `docker run -p 8080:8000 nome` | Sobe o container mapeando porta do host para o container. |
| `docker run -d nome` | Sobe em background (detached). |
| `docker run -e CHAVE=valor nome` | Passa variável de ambiente para o container. |
| `docker run --rm nome` | Remove o container automaticamente ao encerrar. |

---

## 🎼 Parte 2 — Docker Compose

O **Docker Compose** orquestra múltiplos containers a partir de um único arquivo `.yml`. Em vez de rodar vários `docker run` manualmente, você descreve todos os serviços, redes e volumes num só lugar.

### Estrutura básica do `docker-compose.yml`

```yaml
version: "3.9"

services:
  backend:
    build: .
    ports:
      - "8080:8000"
    environment:
      DB_HOST: db
    depends_on:
      - db
    restart: on-failure

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: imoveisdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: senha123
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

### 📌 Chaves do `docker-compose.yml`

#### Nível de serviço (`services`)

| Chave | Exemplo | O que faz |
|-------|---------|-----------|
| `build` | `build: .` | Constrói a imagem usando o Dockerfile do diretório indicado. |
| `image` | `image: postgres:15` | Usa uma imagem pronta do Docker Hub, sem precisar de Dockerfile. |
| `ports` | `- "8080:8000"` | Mapeia porta do host para o container no formato `host:container`. |
| `environment` | `DB_HOST: db` | Define variáveis de ambiente para o container. |
| `depends_on` | `- db` | Define que este serviço só sobe depois que o serviço listado iniciar. |
| `restart` | `on-failure` | Política de reinício: `no`, `always`, `on-failure`, `unless-stopped`. |
| `volumes` | `- pgdata:/data` | Monta um volume ou diretório no container. |
| `networks` | `- minha-rede` | Conecta o serviço a uma rede específica. |
| `env_file` | `env_file: .env` | Carrega variáveis de ambiente de um arquivo `.env`. |
| `command` | `command: python app.py` | Substitui o CMD padrão da imagem. |

#### Nível raiz (fora de `services`)

| Chave | O que faz |
|-------|-----------|
| `version` | Versão da sintaxe do Compose. Use `"3.9"` para projetos novos. |
| `volumes` | Declara volumes nomeados que persistem dados entre reinicializações. |
| `networks` | Declara redes personalizadas para controlar a comunicação entre serviços. |

---

### 📌 Valores de `restart`

| Valor | Comportamento |
|-------|---------------|
| `no` | Nunca reinicia (padrão). |
| `always` | Reinicia sempre, inclusive ao ligar o servidor. |
| `on-failure` | Reinicia apenas se o container encerrar com erro. Útil durante o boot do banco. |
| `unless-stopped` | Reinicia sempre, exceto se você parar manualmente. |

---

### ⚡ Comandos do Docker Compose

#### Subir e parar serviços

| Comando | O que faz |
|---------|-----------|
| `docker-compose up` | Sobe todos os serviços em primeiro plano (mostra os logs). |
| `docker-compose up -d` | Sobe todos os serviços em background. |
| `docker-compose up --build` | Reconstrói as imagens antes de subir (útil após mudanças no código). |
| `docker-compose down` | Para e remove os containers e a rede criada. |
| `docker-compose down -v` | Para, remove containers **e apaga os volumes** — use com cuidado! |
| `docker-compose stop` | Apenas para os containers, sem remover. |
| `docker-compose start` | Reinicia containers que foram parados com `stop`. |
| `docker-compose restart` | Reinicia todos os serviços. |

#### Monitoramento

| Comando | O que faz |
|---------|-----------|
| `docker-compose ps` | Lista o estado de todos os serviços do projeto. |
| `docker-compose logs` | Exibe os logs de todos os serviços. |
| `docker-compose logs -f` | Acompanha os logs em tempo real (follow). |
| `docker-compose logs backend` | Exibe logs apenas do serviço `backend`. |

#### Execução e diagnóstico

| Comando | O que faz |
|---------|-----------|
| `docker-compose exec backend sh` | Abre um terminal dentro do container `backend`. |
| `docker-compose exec db psql -U postgres` | Abre o cliente do PostgreSQL dentro do container `db`. |
| `docker-compose run --rm backend python seed.py` | Roda um comando avulso num novo container e remove ao terminar. |
| `docker-compose config` | Valida e exibe o `docker-compose.yml` processado (com variáveis expandidas). |

---

### 💡 Boas práticas do Docker Compose

**1. Use variáveis de ambiente com `.env`**
```bash
# .env
DB_PASSWORD=senha123
APP_PORT=8080
```
```yaml
# docker-compose.yml
services:
  backend:
    ports:
      - "${APP_PORT}:8000"
    environment:
      DB_PASSWORD: ${DB_PASSWORD}
```
> Nunca suba o `.env` com senhas reais para o repositório. Adicione ao `.gitignore`.

**2. Sempre declare volumes nomeados para bancos de dados**
```yaml
# ✅ Dados persistem após docker-compose down
volumes:
  - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:

# ❌ Dados são perdidos ao remover o container
# (sem volume declarado)
```

**3. Use `depends_on` + `restart: on-failure` juntos**
```yaml
backend:
  depends_on:
    - db           # garante a ordem de inicialização
  restart: on-failure  # reinicia se o banco ainda não estiver pronto
```

**4. Prefira `env_file` para muitas variáveis**
```yaml
services:
  backend:
    env_file:
      - .env       # mais limpo que listar dezenas de variáveis
```

---

## 🔧 Parte 3 — Gerenciamento Geral

### Imagens

| Comando | O que faz |
|---------|-----------|
| `docker images` | Lista todas as imagens locais. |
| `docker rmi nome-imagem` | Remove uma imagem local. |
| `docker pull postgres:15` | Baixa uma imagem do Docker Hub sem rodar. |
| `docker tag img meu-repo/img:v1` | Cria uma nova tag para a imagem (para publicar). |
| `docker push meu-repo/img:v1` | Publica a imagem no Docker Hub. |

### Containers

| Comando | O que faz |
|---------|-----------|
| `docker ps` | Lista containers em execução. |
| `docker ps -a` | Lista todos os containers, incluindo parados. |
| `docker stop <id>` | Para um container em execução. |
| `docker rm <id>` | Remove um container parado. |
| `docker logs -f <id>` | Acompanha os logs de um container em tempo real. |
| `docker exec -it <id> sh` | Abre terminal interativo dentro do container. |
| `docker inspect <id>` | Exibe detalhes técnicos do container (IP, configs, volumes). |

### Limpeza

| Comando | O que faz |
|---------|-----------|
| `docker system prune` | Remove containers parados, redes e imagens não usadas. |
| `docker system prune -a` | Remove tudo acima **e também** imagens sem uso. |
| `docker volume prune` | Remove volumes que não estão sendo usados por nenhum container. |

---

## 🗂️ Resumo visual do fluxo

```
Dockerfile
    │
    │  docker build -t minha-imagem .
    ▼
Imagem (Image)
    │
    │  docker run -p 8080:8000 minha-imagem
    ▼
Container em execução
    │
    └── Conectado via Docker Network a outros containers
            │
            └── Orquestrado pelo Docker Compose (docker-compose.yml)
```

---

## 👥 Equipe

Material produzido pelo Grupo de Estudos MLOps — **INF/UFG · CEIA**

- Jamily Vieira Gonçalves
- Pedro Lukas
- Gabriel Vidal
- Matheus

---

> **Dica final:** sempre que travar num erro, rode `docker-compose logs -f` primeiro. 90% dos problemas aparecem ali.
