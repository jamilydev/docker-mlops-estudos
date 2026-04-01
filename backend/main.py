from fastapi import FastAPI

app = FastAPI(title="API de Predição Imobiliária")

@app.get("/")
def home():
    return {"status": "Modelo de Precificação Online e Operacional"}

@app.get("/predict/")
def prever_preco(tamanho_m2: float, num_quartos: int):
    valor_base = 150000
    acrescimo_por_m2 = tamanho_m2 * 4500
    acrescimo_por_quarto = num_quartos * 25000
    
    preco_final = valor_base + acrescimo_por_m2 + acrescimo_por_quarto
    
    return {
        "dados_recebidos": {
            "metros_quadrados": tamanho_m2,
            "quantidade_quartos": num_quartos
        },
        "preco_estimado_R$": preco_final
    }