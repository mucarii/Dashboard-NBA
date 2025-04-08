def calcular_fantasy_pontos(stats):
    try:
        pontos = stats.get("PTS", 0)
        rebotes = stats.get("REB", 0)
        assistencias = stats.get("AST", 0)
        roubos = stats.get("STL", 0)
        tocos = stats.get("BLK", 0)
        turnovers = stats.get("TO", 0)
        triplos = stats.get("FG3M", 0)
        tech_fouls = stats.get(
            "TECH_FOULS", 0
        )  # Pode ser diferente dependendo do dataset
        flagrant_fouls = stats.get("FLAGRANT_FOULS", 0)  # Idem

        # Pontuação base
        fantasy_points = (
            pontos * 1
            + rebotes * 1.2
            + assistencias * 1.5
            + roubos * 2
            + tocos * 3
            - turnovers * 2
            + triplos * 0.5
            - tech_fouls * 2
            - flagrant_fouls * 2
        )

        # Bônus
        bonus = 0
        stats_triplo = 0
        for stat in [pontos, rebotes, assistencias, roubos, tocos]:
            if stat >= 10:
                stats_triplo += 1

        if stats_triplo >= 3:
            bonus += 6  # Triple-double
        elif stats_triplo >= 2:
            bonus += 3  # Double-double

        if pontos >= 40:
            bonus += 2
        if pontos >= 50:
            bonus += 3
        if assistencias >= 15:
            bonus += 2
        if rebotes >= 20:
            bonus += 2

        return round(fantasy_points + bonus, 2)

    except Exception as e:
        print(f"Erro ao calcular fantasy: {e}")
        return 0
