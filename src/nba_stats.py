from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import time


def get_player_id(player_name):
    """
    Retorna o ID do jogador a partir do nome.
    """
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict:
        return player_dict[0]["id"]
    else:
        return None


def get_player_career_stats(player_id):
    """
    Retorna as estatísticas de carreira do jogador com base no ID.
    """
    time.sleep(0.6)  # evitar erro de rate limit
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]
    return df


def get_latest_season_stats(df_stats):
    """
    Retorna as estatísticas da temporada mais recente do jogador.
    """
    if df_stats.empty:
        return None
    latest_season = df_stats.iloc[-1]
    return {
        "Temporada": latest_season["SEASON_ID"],
        "Time": latest_season["TEAM_ABBREVIATION"],
        "Jogos": latest_season["GP"],
        "Minutos": latest_season["MIN"],
        "Pontos": latest_season["PTS"],
        "Assistências": latest_season["AST"],
        "Rebotes": latest_season["REB"],
        "Roubos": latest_season["STL"],
        "Tocos": latest_season["BLK"],
    }


def get_all_player_stats():
    """
    Retorna um DataFrame com estatísticas da temporada atual de todos os jogadores.
    """
    time.sleep(0.6)
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2024-25")
    df = stats.get_data_frames()[0]
    return df


def get_top_players_by_stat(df, stat="PTS", top_n=25):
    """
    Retorna os top N jogadores com base em uma estatística.
    """
    df_sorted = df.sort_values(by=stat, ascending=False)
    return df_sorted[["PLAYER_NAME", "TEAM_ABBREVIATION", stat]].head(top_n)


def calcular_fantasy_pontos(stats):
    pontos = stats.get("Pontos", 0)
    rebotes = stats.get("Rebotes", 0)
    assistencias = stats.get("Assistências", 0)
    roubos = stats.get("Roubos", 0)
    tocos = stats.get("Tocos", 0)
    turnovers = stats.get("TOV", 0) if "TOV" in stats else 0
    triplos = stats.get("FG3M", 0) if "FG3M" in stats else 0
    tecnicas = stats.get("TECH_FOUL", 0) if "TECH_FOUL" in stats else 0
    flagrantes = stats.get("FLAGRANT_FOUL", 0) if "FLAGRANT_FOUL" in stats else 0

    fantasy = (
        pontos * 1
        + rebotes * 1.2
        + assistencias * 1.5
        + roubos * 2
        + tocos * 3
        - turnovers * 2
        + triplos * 0.5
        - tecnicas * 2
        - flagrantes * 2
    )

    # Bônus
    bonus = 0
    categorias = [pontos, rebotes, assistencias]
    if sum(x >= 10 for x in categorias) >= 2:
        bonus += 3  # double-double
    if sum(x >= 10 for x in categorias) >= 3:
        bonus += 6  # triple-double
    if pontos >= 40:
        bonus += 2
    if pontos >= 50:
        bonus += 3
    if assistencias >= 15:
        bonus += 2
    if rebotes >= 20:
        bonus += 2

    return round(fantasy + bonus, 2)
