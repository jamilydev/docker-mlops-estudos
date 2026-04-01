import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Variáveis de ambiente definidas no docker-compose.yml
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "imoveisdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "senha123")


def get_connection():
    """Abre uma conexão com o PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


def criar_tabela():
    """
    Cria a tabela de imóveis se ainda não existir.
    Chamada automaticamente quando a API inicializa.
    """
    sql = """
        CREATE TABLE IF NOT EXISTS imoveis (
            id            SERIAL PRIMARY KEY,
            endereco      TEXT        NOT NULL,
            tamanho_m2    FLOAT       NOT NULL,
            num_quartos   INTEGER     NOT NULL,
            cadastrado_em TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
        );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def cadastrar_imovel(endereco: str, tamanho_m2: float, num_quartos: int):
    """Insere um novo imóvel no banco e retorna o registro criado."""
    sql = """
        INSERT INTO imoveis (endereco, tamanho_m2, num_quartos)
        VALUES (%s, %s, %s)
        RETURNING id, endereco, tamanho_m2, num_quartos, cadastrado_em;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (endereco, tamanho_m2, num_quartos))
            imovel = cur.fetchone()
        conn.commit()
    return imovel


def listar_imoveis():
    """Retorna todos os imóveis cadastrados, do mais recente ao mais antigo."""
    sql = """
        SELECT id, endereco, tamanho_m2, num_quartos, cadastrado_em
        FROM imoveis
        ORDER BY cadastrado_em DESC;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()


def buscar_imovel_por_id(imovel_id: int):
    """Retorna um imóvel específico pelo seu ID."""
    sql = """
        SELECT id, endereco, tamanho_m2, num_quartos, cadastrado_em
        FROM imoveis
        WHERE id = %s;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (imovel_id,))
            return cur.fetchone()
