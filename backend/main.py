from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import criar_tabela, cadastrar_imovel, listar_imoveis, buscar_imovel_por_id
 
app = FastAPI(title="API de Imóveis — Cadastro e Predição")
 
 
# ── Schema de entrada para cadastro ──────────────────────
class ImovelInput(BaseModel):
    endereco: str
    tamanho_m2: float
    num_quartos: int
 
 
# ── Inicialização ─────────────────────────────────────────
@app.on_event("startup")
def startup():
    """Cria a tabela no banco assim que a API sobe."""
    criar_tabela()
 
 
# ── Endpoints ─────────────────────────────────────────────
 
@app.get("/")
def home():
    return {"status": "API de Imóveis Online e Operacional"}
 
 
@app.post("/imoveis/", status_code=201)
def cadastrar(imovel: ImovelInput):
    """
    Cadastra um novo imóvel no banco de dados.
 
    Exemplo de body:
    {
        "endereco": "Rua das Flores, 123",
        "tamanho_m2": 80,
        "num_quartos": 3
    }
    """
    novo = cadastrar_imovel(imovel.endereco, imovel.tamanho_m2, imovel.num_quartos)
    return {"mensagem": "Imóvel cadastrado com sucesso!", "imovel": novo}
 
 
@app.get("/imoveis/")
def listar():
    """Lista todos os imóveis cadastrados no banco."""
    imoveis = listar_imoveis()
    return {"total": len(imoveis), "imoveis": imoveis}
 
 
@app.get("/imoveis/{imovel_id}")
def buscar(imovel_id: int):
    """Retorna os dados de um imóvel específico pelo ID."""
    imovel = buscar_imovel_por_id(imovel_id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return imovel
 
 
@app.get("/predict/{imovel_id}")
def prever_preco(imovel_id: int):
    """
    Busca um imóvel cadastrado pelo ID e calcula o preço estimado.
    Assim o modelo sempre usa dados reais do banco.
    """
    imovel = buscar_imovel_por_id(imovel_id)
    if not imovel:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
 
    valor_base          = 150_000
    acrescimo_por_m2    = imovel["tamanho_m2"]  * 4_500
    acrescimo_por_quarto = imovel["num_quartos"] * 25_000
    preco_final         = valor_base + acrescimo_por_m2 + acrescimo_por_quarto
 
    return {
        "imovel": {
            "id":          imovel["id"],
            "endereco":    imovel["endereco"],
            "tamanho_m2":  imovel["tamanho_m2"],
            "num_quartos": imovel["num_quartos"],
        },
        "preco_estimado_R$": preco_final
    }
 