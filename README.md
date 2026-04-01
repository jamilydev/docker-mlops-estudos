#🐳 Docker para MLOps: Do Dockerfile ao Compose

Este guia foi elaborado para acompanhar o estudo de MLOps do Instituto de Informática (INF/UFG) e do CEIA. Se você está acompanhando esta aula, utilize este material como o seu mapa de navegação pelos conceitos de containerização.
---
##📌 1. O Ponto de Partida: Por que estamos aqui? 💻

Você já tentou rodar um modelo de IA de um colega e ele falhou por erro de "módulo não encontrado" ou versão de biblioteca?

O Cenário Comum: Projetos de ML dependem de versões exatas de scikit-learn, pandas, PyTorch e até drivers específicos de GPU.

A Solução com Docker: Criamos um ambiente imutável. O que você vê rodando hoje, rodará exatamente da mesma forma daqui a 10 anos, em qualquer servidor do mundo.
---
##🎂 2. Entendendo o Docker (Analogia da Cozinha)

Para não esquecer mais como o Docker funciona, imagine que estamos em uma cozinha profissional:

Dockerfile (A Receita): É o documento onde escrevemos os ingredientes (bibliotecas) e o passo a passo da preparação.

Imagem (O Bolo): É o resultado do "cozimento" (build). É um pacote fechado e pronto. Você não pode mudar o sabor do bolo depois de pronto, apenas fazer uma receita nova.

Container (A Fatia): É o que realmente consumimos. Podemos tirar várias fatias (containers) do mesmo bolo (imagem) ao mesmo tempo.

##📂 3. O Que Veremos na Prática

Nesta atividade, vamos observar a construção de uma infraestrutura que une Inferência + Persistência:
```
WorkShop_Docker/
├── backend/
│   ├── main.py          # O "cérebro" (API FastAPI que serve o modelo)
│   ├── database.py      # A "ponte" para o banco de dados
│   └── requirements.txt # A lista de compras (Dependências Python)
├── Dockerfile           # A receita para o nosso backend
└── docker-compose.yml   # O maestro que coordena a API e o Banco
```

🚀 4. Acompanhando a Execução

🔹 Etapa 1: A Construção da Imagem (Dockerfile)

Nesta fase, transformamos código puro em um artefato pronto para produção.

Pontos de atenção na "Receita":

Base Leve: Usamos python:3.10-slim para não carregar arquivos inúteis.

Otimização de Camadas: Instalamos as bibliotecas (pip install) antes de copiar o código. Isso faz com que, se mudarmos apenas uma linha do código, o Docker não precise reinstalar tudo de novo.

Porta de Saída: A aplicação se comunica com o mundo pela porta 8000.

Comandos que serão demonstrados:

# Build: Criando o "Bolo" (Imagem)
```bash
docker build -t mlops-model-v1 .
```
# Run: Servindo a "Fatia" (Container)
```bash
docker run -p 8080:8000 mlops-model-v1
```

Acesse o Swagger (documentação da API) em: http://localhost:8080/docs

🔹 Etapa 2: Orquestração (Docker Compose)

Aqui, vemos como múltiplos containers conversam entre si.

No mundo real de MLOps, o modelo não vive sozinho. Ele precisa de um banco para salvar logs de predição. O Compose resolve isso:

Persistência: Usamos Volumes para que, se o banco de dados cair, os dados não sejam deletados.

Rede Interna: O backend sabe onde o banco de dados está apenas chamando-o pelo nome (db).

Comandos que serão demonstrados:

# Sobe todo o sistema (API + Banco) de uma vez
docker-compose up -d

# Mostra o status de saúde dos serviços
docker-compose ps




👥 Equipe (Grupo de Estudos MLOps)

Jamily Vieira Gonçalves

Pedro Lukas

Gabriel Vidal

Matheus

Este material foi criado com o suporte do Instituto de Informática da Universidade Federal de Goiás (INF/UFG).
