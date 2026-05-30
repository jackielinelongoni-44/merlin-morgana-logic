import swisseph as swe

# Lista com a ordem dos signos (30 graus para cada)
SIGNOS = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

# Mapeamento dos planetas com seus respectivos IDs na Swiss Ephemeris
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

def converter_graus_para_signo(graus_totais):
    """Transforma a longitude celestial (0-360) em Signo e Grau exato."""
    indice_signo = int(graus_totais // 30)
    grau_no_signo = graus_totais % 30
    nome_signo = SIGNOS[indice_signo]
    return nome_signo, grau_no_signo

def calcular_mapa_base(ano, mes, dia, hora_utc):
    """Calcula a posição de todos os planetas principais para uma data em UTC."""
    dia_juliano = swe.julday(ano, mes, dia, hora_utc)
    mapa_calculado = {}
    
    for nome_planeta, id_planeta in PLANETAS_ID.items():
        resultado, _ = swe.calc_ut(dia_juliano, id_planeta)
        graus_totais = resultado[0]
        signo, grau_exato = converter_graus_para_signo(graus_totais)
        
        mapa_calculado[nome_planeta] = {
            "signo": signo,
            "grau": round(grau_exato, 2)
        }
        
    return mapa_calculado

def calcular_casas_regiomontanus(ano, mes, dia, hora_utc, latitude, longitude):
    """
    Calcula as 12 casas astrológicas e os ângulos principais (Asc/MC)
    utilizando estritamente o sistema Regiomontanus ('R').
    """
    dia_juliano = swe.julday(ano, mes, dia, hora_utc)
    
    # 'R' define o sistema Regiomontanus na biblioteca
    # Retorna duas listas: a primeira com as 12 casas, a segunda com [Asc, MC, etc.]
    cuspides, ascmc = swe.houses(dia_juliano, latitude, longitude, b'R')
    
    casas_calculadas = {}
    
    # Organiza as 12 cúspides das casas
    for i in range(1, 13):
        graus_totais = cuspides[i]
        signo, grau_exato = converter_graus_para_signo(graus_totais)
        casas_calculadas[f"Casa {i}"] = {
            "signo": signo,
            "grau": round(grau_exato, 2)
        }
        
    # Organiza os ângulos principais
    signo_asc, grau_asc = converter_graus_para_signo(ascmc[0])
    signo_mc, grau_mc = converter_graus_para_signo(ascmc[1])
    
    casas_calculadas["Ascendente"] = {"signo": signo_asc, "grau": round(grau_asc, 2)}
    casas_calculadas["Meio do Céu"] = {"signo": signo_mc, "grau": round(grau_mc, 2)}
    
    return casas_calculadas

# --- TESTANDO O MOTOR COMPLETO ---
if __name__ == "__main__":
    # Exemplo: Um nascimento em Porto Alegre - RS
    # Latitude: -30.03, Longitude: -51.21
    ano, mes, dia = 2026, 5, 30
    hora_utc = 22.0  
    lat, lon = -30.03, -51.21
    
    print("🔮 Rodando as engrenagens de 'merlin-morgana-logic'...")
    
    # 1. Calcula Planetas
    planetas = calcular_mapa_base(ano, mes, dia, hora_utc)
    # 2. Calcula Casas (Regiomontanus)
    casas = calcular_casas_regiomontanus(ano, mes, dia, hora_utc, lat, lon)
    
    print(f"\n--- POSIÇÃO DOS ASTROS ---")
    for planeta, dados in planetas.items():
        print(f"🔹 {planeta}: {dados['signo']} a {dados['grau']}°")
        
    print(f"\n--- CÚSPIDES REGIOMONTANUS ---")
    print(f"🌅 Ascendente: {casas['Ascendente']['signo']} a {casas['Ascendente']['grau']}°")
    print(f"👑 Meio do Céu: {casas['Meio do Céu']['signo']} a {casas['Meio do Céu']['grau']}°")
    for i in range(1, 13):
        nome_casa = f"Casa {i}"
        print(f"🏠 {nome_casa}: {casas[nome_casa]['signo']} a {casas[nome_casa]['grau']}°")
