import swisseph as swe
import json
import os

# Lista com a ordem dos signos
SIGNOS = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

# Mapeamento dos planetas com seus IDs na Swiss Ephemeris
PLANETAS_ID = {
    "Sol": swe.SUN,
    "Lua": swe.MOON,
    "Mercúrio": swe.MERCURY,
    "Vênus": swe.VENUS,
    "Marte": swe.MARS,
    "Júpiter": swe.JUPITER,
    "Saturno": swe.SATURN,
    "Urano": swe.URANUS,
    "Netuno": swe.NEPTUNE,
    "Plutão": swe.PLUTO
}

# --- CONFIGURAÇÃO DE ORBES (Ajuste aqui quando quiser) ---
ORBE_CONJUNCAO = 8.0
ORBE_OPOSICAO = 8.0

ASPECTOS_CONFIG = {
    "Conjunção": {"angulo": 0, "orbe": ORBE_CONJUNCAO},
    "Sextil": {"angulo": 60, "orbe": 6.0},
    "Quadratura": {"angulo": 90, "orbe": 8.0},
    "Trígono": {"angulo": 120, "orbe": 8.0},
    "Oposição": {"angulo": 180, "orbe": ORBE_OPOSICAO}
}

def converter_graus_para_signo(graus_totais):
    indice_signo = int(graus_totais // 30)
    grau_no_signo = graus_totais % 30
    return SIGNOS[indice_signo], grau_no_signo

def calcular_mapa_base(ano, mes, dia, hora_utc):
    dia_juliano = swe.julday(ano, mes, dia, hora_utc)
    mapa_calculado = {}
    for nome_planeta, id_planeta in PLANETAS_ID.items():
        resultado, _ = swe.calc_ut(dia_juliano, id_planeta)
        graus_totais = resultado[0]
        signo, grau_exato = converter_graus_para_signo(graus_totais)
        mapa_calculado[nome_planeta] = {
            "signo": signo,
            "grau": round(grau_exato, 2),
            "graus_totais": graus_totais
        }
    return mapa_calculado

def calcular_casas_regiomontanus(ano, mes, dia, hora_utc, latitude, longitude):
    dia_juliano = swe.julday(ano, mes, dia, hora_utc)
    cuspides, ascmc = swe.houses(dia_juliano, latitude, longitude, b'R')
    casas_calculadas = {}
    for i in range(1, 13):
        signo, grau_exato = converter_graus_para_signo(cuspides[i])
        casas_calculadas[f"Casa {i}"] = {"signo": signo, "grau": round(grau_exato, 2)}
    signo_asc, grau_asc = converter_graus_para_signo(ascmc[0])
    casas_calculadas["Ascendente"] = {"signo": signo_asc, "grau": round(grau_asc, 2)}
    return casas_calculadas

def interpretar_mapa(mapa_planetas, mapa_casas):
    """Abre o arquivo JSON e extrai os textos correspondentes ao mapa calculado."""
    # Carrega o arquivo de interpretações com segurança
    try:
        with open("interpretacoes.json", "r", encoding="utf-8") as f:
            textos = json.load(f)
    except FileNotFoundError:
        return "Erro: O arquivo 'interpretacoes.json' não foi encontrado."

    relatorio = []
    
    # Busca interpretação para cada planeta calculado
    for planeta, dados in mapa_planetas.items():
        signo = dados["signo"]
        # Puxa o texto se ele existir no JSON, senão coloca um aviso padrão
        texto_planeta = textos.get("planetas", {}).get(planeta, {}).get(signo, "Texto interpretativo em desenvolvimento...")
        relatorio.append(f"🔮 {planeta} em {signo} ({dados['grau']}°):\n↳ {texto_planeta}\n")
        
    return "\n".join(relatorio)

# --- TESTANDO INTEGRADO ---
if __name__ == "__main__":
    # Teste simulando um usuário nascendo agora
    ano, mes, dia = 2026, 5, 30
    hora_utc = 22.0
    lat, lon = -30.03, -51.21  # Porto Alegre
    
    print("🔮 Alinhando 'merlin-morgana-logic' com o banco de dados...")
    
    planetas = calcular_mapa_base(ano, mes, dia, hora_utc)
    casas = calcular_casas_regiomontanus(ano, mes, dia, hora_utc, lat, lon)
    
    # Gera o relatório interpretado em português
    analise_textual = interpretar_mapa(planetas, casas)
    
    print("\n==========================================")
    print("       RELATÓRIO ASTROLÓGICO DIGITAL      ")
    print("==========================================")
    print(analise_textual)
