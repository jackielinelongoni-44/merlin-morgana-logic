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

# Definição dos Aspectos Maiores: (Ângulo exato, Orbe padrão sugerida)
ASPECTOS_CONFIG = {
    "Conjunção": {"angulo": 0, "orbe": 8},
    "Sextil": {"angulo": 60, "orbe": 6},
    "Quadratura": {"angulo": 90, "orbe": 8},
    "Trígono": {"angulo": 120, "orbe": 8},
    "Oposição": {"angulo": 180, "orbe": 8}
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
            "grau": round(grau_exato, 2),
            "graus_totais": graus_totais  # Guardamos o valor bruto (0-360) para calcular aspectos
        }
        
    return mapa_calculado

def calcular_casas_regiomontanus(ano, mes, dia, hora_utc, latitude, longitude):
    """Calcula as 12 casas astrológicas utilizando o sistema Regiomontanus ('R')."""
    dia_juliano = swe.julday(ano, mes, dia, hora_utc)
    cuspides, ascmc = swe.houses(dia_juliano, latitude, longitude, b'R')
    
    casas_calculadas = {}
    for i in range(1, 13):
        signo, grau_exato = converter_graus_para_signo(cuspides[i])
        casas_calculadas[f"Casa {i}"] = {"signo": signo, "grau": round(grau_exato, 2)}
        
    signo_asc, grau_asc = converter_graus_para_signo(ascmc[0])
    signo_mc, grau_mc = converter_graus_para_signo(ascmc[1])
    
    casas_calculadas["Ascendente"] = {"signo": signo_asc, "grau": round(grau_asc, 2)}
    casas_calculadas["Meio do Céu"] = {"signo": signo_mc, "grau": round(grau_mc, 2)}
    
    return casas_calculadas

def detectar_aspectos(planetas_calculados):
    """Varre todos os planetas em pares e identifica os aspectos ativos."""
    aspectos_encontrados = []
    nomes_planetas = list(planetas_calculados.keys())
    
    # Cruzamento duplo (Garante que não calculamos Sol-Lua e depois Lua-Sol repetido)
    for i in range(len(nomes_planetas)):
        for j in range(i + 1, len(nomes_planetas)):
            p1 = nomes_planetas[i]
            p2 = nomes_planetas[j]
            
            g1 = planetas_calculados[p1]["graus_totais"]
            g2 = planetas_calculados[p2]["graus_totais"]
            
            # Calcula a menor distância geométrica no círculo de 360°
            diff = abs(g1 - g2)
            distancia = diff if diff <= 180 else 360 - diff
            
            # Testa a distância contra cada configuração de aspecto
            for nome_asp, config in ASPECTOS_CONFIG.items():
                if abs(distancia - config["angulo"]) <= config["orbe"]:
                    orbe_exata = abs(distancia - config["angulo"])
                    aspectos_encontrados.append({
                        "p1": p1,
                        "p2": p2,
                        "aspecto": nome_asp,
                        "orbe": round(orbe_exata, 2)
                    })
                    
    return aspectos_encontrados

# --- TESTANDO O MOTOR COMPLETO ---
if __name__ == "__main__":
    # Exemplo: Teste em tempo real
    ano, mes, dia = 2026, 5, 30
    hora_utc = 22.0  
    lat, lon = -30.03, -51.21  # Porto Alegre
    
    print("🔮 Rodando as engrenagens de 'merlin-morgana-logic'...")
    
    planetas = calcular_mapa_base(ano, mes, dia, hora_utc)
    casas = calcular_casas_regiomontanus(ano, mes, dia, hora_utc, lat, lon)
    aspectos = detectar_aspectos(planetas)
    
    print(f"\n--- POSIÇÃO DOS ASTROS ---")
    for planeta, dados in planetas.items():
        print(f"🔹 {planeta}: {dados['signo']} a {dados['grau']}°")
        
    print(f"\n--- ASPECTOS ENCONTRADOS ---")
    for asp in aspectos:
        print(f"⚡ {asp['p1']} em {asp['aspecto']} com {asp['p2']} (Orbe: {asp['orbe']}°)")
