# 🐳 Docker para MLOps: Do Dockerfile ao Compose

Este guia foi elaborado para acompanhar o estudo de MLOps do Instituto de Informática (INF/UFG) e do CEIA. Se está a acompanhar esta aula, utilize este material como o seu mapa de navegação pelos conceitos de contentorização.

---

## 📌 1. O Ponto de Partida: Por que estamos aqui? 💻

Já tentou correr um modelo de IA de um colega e ele falhou por erro de "módulo não encontrado" ou versão de biblioteca?

- **O Cenário Comum:** Projetos de ML dependem de versões exatas de `scikit-learn`, `pandas`, `PyTorch` e até drivers específicos de GPU.
- **A Solução com Docker:** Criamos um ambiente imutável. O que vê a funcionar hoje, funcionará exatamente da mesma forma daqui a 10 anos, em qualquer servidor do mundo.

---

## 🎂 2. Entendendo o Docker (Analogia da Cozinha)

Para não esquecer mais como o Docker funciona, imagine que estamos numa cozinha profissional:

1. **Dockerfile (A Receita):** É o documento onde escrevemos os ingredientes (bibliotecas) e o passo a passo da preparação.
2. **Imagem (O Bolo):** É o resultado do "cozimento" (`build`). É um pacote fechado e pronto. Não pode mudar o sabor do bolo depois de pronto, apenas fazer uma receita nova.
3. **Container (A Fatia):** É o que realmente consumimos. Podemos tirar várias fatias (containers) do mesmo bolo (imagem) ao mesmo tempo.

---

## 📂 3. O Que Veremos na Prática

Nesta atividade, vamos observar a construção de uma infraestrutura que une **Inferência + Persistência**:

```
WorkShop_Docker/
├── backend/
│   ├── main.py          # O "cérebro" (API FastAPI que serve o modelo)
│   ├── database.py      # A "ponte" para a base de dados
│   └── requirements.txt # A lista de compras (Dependências Python)
├── Dockerfile           # A receita para o nosso backend
└── docker-compose.yml   # O maestro que coordena a API e o Banco
```

---

## 🚀 4. Acompanhando a Execução

### 🔹 Etapa 1: A Construção da Imagem (Dockerfile)

Nesta fase, transformamos código puro num artefacto pronto para produção.

**Pontos de atenção na "Receita":**

- **Base Leve:** Usamos `python:3.10-slim` para não carregar ficheiros inúteis.
- **Otimização de Camadas:** Instalamos as bibliotecas (`pip install`) antes de copiar o código. Isso economiza tempo em builds futuros.
- **Porta de Saída:** A aplicação comunica com o mundo pela porta `8000`.

**Comandos que serão demonstrados:**

```bash
# Build: Criando o "Bolo" (Imagem)
docker build -t mlops-model-v1 .

# Run: Servindo a "Fatia" (Container)
docker run -p 8080:8000 mlops-model-v1
```

Aceda ao Swagger (documentação da API) em: `http://localhost:8080/docs`

---

### 🔹 Etapa 2: Orquestração (Docker Compose)

Aqui, vemos como múltiplos containers conversam entre si através de ficheiros YAML.

O ficheiro `.yml` é o mapa que o Compose usa para ligar a API à Base de Dados:

1. **Persistência:** Usamos Volumes para que os dados do banco não sejam eliminados se o container parar.
2. **Rede Interna:** O backend localiza a base de dados apenas pelo nome do serviço (`db`).

**Comandos que serão demonstrados:**

```bash
# Sobe todo o sistema (API + Banco) de uma vez
docker-compose up -d

# Mostra o estado de saúde dos serviços
docker-compose ps
```

---

## 📄 5. Guia de Consulta Rápida (Cheat Sheet)

| Categoria | Comando | O que faz? |
|-----------|---------|------------|
| Build | `docker build -t nome .` | Transforma o Dockerfile em imagem. |
| Rodar | `docker run -p 80:80 img` | Inicia um container baseado numa imagem. |
| Status | `docker ps` | Mostra o que está "vivo" no momento. |
| Compose | `docker-compose up -d` | Sobe todos os serviços em segundo plano. |
| Limpeza | `docker system prune` | Remove lixo e liberta espaço em disco. |

---

## 👥 Equipe (Grupo de Estudos MLOps)

- Jamily Vieira Gonçalves
- Pedro Lukas
- Gabriel Vidal
- Matheus

---

> Este material foi criado com o suporte do **Instituto de Informática da Universidade Federal de Goiás (INF/UFG)**.
