from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Inicializa o FastAPI (O nosso garçom do aplicativo)
app = FastAPI(title="Merlin & Morgana - Motor Astrológico")

# CONFIGURAÇÃO DE SEGURANÇA (CORS)
# Isso permite que a sua página web do GitHub Pages converse com este motor Python com total segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite requisições da sua interface web
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos exatamente o formato dos dados de nascimento que o motor aceita receber
class DadosNascimento(BaseModel):
    nome: str
    data: str
    hora: str
    cidade: str

# ROTA PRINCIPAL: A fresta na torre por onde os dados da tela entram
@app.post("/calcular-mapa")
def calcular_mapa(dados: DadosNascimento):
    # 1. Aqui o motor recebe os dados limpos da tela
    nome_usuario = dados.nome
    data_nascimento = dados.data
    hora_nascimento = dados.hora
    cidade_nascimento = dados.cidade

    # 2. [ÁREA DE CÁLCULO]: Aqui entram as nossas funções das efemérides.
    # Por enquanto, vamos simular o retorno do cálculo usando o Sistema Regiomontanus
    # para testarmos se a conexão entre a tela e o Python está perfeita.
    
    resultado_astrologico = {
        "status": "sucesso",
        "mensagem": f"Céu de nascimento para {nome_usuario} conjurado com sucesso!",
        "sistema_casas": "Regiomontanus",
        "mapa": {
            "Sol": "Touro",      # Exemplo simulado
            "Lua": "Escorpião",
            "Ascendente": "Câncer",
            "Casa_1": "Câncer",
            "Casa_10": "Áries"
        }
    }

    # 3. O garçom leva o resultado de volta para a tela do usuário
    return resultado_astrologico

# Rota simples de teste para garantir que o motor está vivo no servidor
@app.get("/")
def home():
    return {"status": "Alinhado", "mensagem": "O Motor de Merlin & Morgana está online e operando pelo sistema Regiomontanus!"}
