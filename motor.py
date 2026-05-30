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

# --- TESTANDO O MOTOR ---
if __name__ == "__main__":
    # Exemplo de teste com o momento atual (Maio de 2026)
    ano, mes, dia = 2026, 5, 30
    hora_utc = 22.0  # Ajustado para Tempo Universal
    
    print("🔮 Rodando as engrenagens de 'merlin-morgana-logic'...")
    meu_mapa = calcular_mapa_base(ano, mes, dia, hora_utc)
    
    print(f"\n--- POSIÇÃO DOS ASTROS ({dia}/{mes}/{ano}) ---")
    for planeta, dados in meu_mapa.items():
        print(f"🔹 {planeta}: {dados['signo']} a {dados['grau']}°")
