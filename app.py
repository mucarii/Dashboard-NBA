import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.nba_stats import (
    get_player_id,
    get_player_career_stats,
    get_latest_season_stats,
    get_all_player_stats,
    get_top_players_by_stat,
)
from nba_api.stats.static import players
from src.fantasy_calc import calcular_fantasy_pontos


# Função para obter imagem do jogador
def get_player_img_url(player_id):
    return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"


# Lista de jogadores ativos
player_list = players.get_players()
active_players = [player for player in player_list if player["is_active"]]
player_names = sorted([player["full_name"] for player in active_players])

# Estilo
st.set_page_config(page_title="NBA Player Stats", layout="centered")
st.markdown(
    """
    <style>
        .main {
            background-color: #black;
        }
        h1 {
            color: #1E3A8A;
        }
        .block-container {
            padding: 2rem 2rem 1rem;
        }
        div.stButton > button:first-child {
            background-color: #1E3A8A;
            color: white;
            padding: 0.6em 1.2em;
            border-radius: 8px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🏀 Comparação de Jogadores da NBA")
st.markdown(
    "Selecione dois jogadores para comparar suas estatísticas da temporada mais recente."
)

# Seletor de jogadores
col1, col2 = st.columns(2)
with col1:
    player1_name = st.selectbox(
        "Jogador 1", player_names, index=player_names.index("LeBron James")
    )
with col2:
    player2_name = st.selectbox(
        "Jogador 2", player_names, index=player_names.index("Stephen Curry")
    )

# Tabs para navegação
tabs = st.tabs(["📊 Comparação", "📈 Top 25 Estatísticas", "💎 Top 25 Fantasy"])

# Tab 1: Comparação
with tabs[0]:
    if st.button("Comparar"):
        id1 = get_player_id(player1_name)
        id2 = get_player_id(player2_name)

        if not id1 or not id2:
            st.error("Um dos jogadores não foi encontrado. Tente novamente.")
        else:
            stats1_raw = get_player_career_stats(id1)
            stats2_raw = get_player_career_stats(id2)

            stats1 = get_latest_season_stats(stats1_raw)
            stats2 = get_latest_season_stats(stats2_raw)

            stats1["Fantasy Points"] = calcular_fantasy_pontos(stats1)
            stats2["Fantasy Points"] = calcular_fantasy_pontos(stats2)

            if not stats1 or not stats2:
                st.warning("Não foi possível obter estatísticas para um dos jogadores.")
            else:
                st.image(get_player_img_url(id1), width=200, caption=player1_name)
                st.image(get_player_img_url(id2), width=200, caption=player2_name)

                df_comparison = pd.DataFrame(
                    [stats1, stats2], index=[player1_name, player2_name]
                )
                st.subheader("📋 Estatísticas Gerais + Fantasy Points")
                st.dataframe(df_comparison)

                # Gráfico de barras
                st.subheader("📈 Comparação Visual")
                fig = go.Figure()
                for player, stats in zip(
                    [player1_name, player2_name], [stats1, stats2]
                ):
                    fig.add_trace(
                        go.Bar(
                            x=[
                                "Pontos",
                                "Assistências",
                                "Rebotes",
                                "Roubos",
                                "Tocos",
                                "Fantasy Points",
                            ],
                            y=[
                                stats["Pontos"],
                                stats["Assistências"],
                                stats["Rebotes"],
                                stats["Roubos"],
                                stats["Tocos"],
                                stats["Fantasy Points"],
                            ],
                            name=player,
                        )
                    )
                fig.update_layout(
                    barmode="group", title="Comparação de Estatísticas e Fantasy"
                )
                st.plotly_chart(fig, use_container_width=True)

# Tab 2: Top 25 por Estatística
with tabs[1]:
    st.subheader("📋 Ver Top 25 da Temporada por Estatística")
    all_stats = get_all_player_stats()
    all_stats["Fantasy Points"] = all_stats.apply(calcular_fantasy_pontos, axis=1)

    stat_options = ["PTS", "AST", "REB", "STL", "BLK"]
    stat = st.selectbox("Estatística", stat_options)

    top_players = get_top_players_by_stat(all_stats, stat=stat)
    st.dataframe(top_players)

    fig_bar = go.Figure(
        go.Bar(
            x=top_players[stat][::-1],
            y=top_players["PLAYER_NAME"][::-1],
            orientation="h",
            marker_color="indigo",
        )
    )
    fig_bar.update_layout(
        title=f"Top 25 jogadores em {stat}",
        xaxis_title=stat,
        yaxis_title="Jogador",
        height=750,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Tab 3: Top 25 Fantasy Points
with tabs[2]:
    st.subheader("🏆 Top 25 em Fantasy Points")
    top_fantasy = all_stats.sort_values("Fantasy Points", ascending=False).head(25)
    st.dataframe(top_fantasy[["PLAYER_NAME", "Fantasy Points"]])

    fig_top_fantasy = go.Figure(
        go.Bar(
            x=top_fantasy["Fantasy Points"][::-1],
            y=top_fantasy["PLAYER_NAME"][::-1],
            orientation="h",
            marker_color="darkgreen",
        )
    )
    fig_top_fantasy.update_layout(
        title="Top 25 Jogadores por Pontuação Fantasy",
        xaxis_title="Fantasy Points",
        yaxis_title="Jogador",
        height=750,
    )
    st.plotly_chart(fig_top_fantasy, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown(
    "Feito por [Murilo Calore](https://github.com/mucarii)",
    unsafe_allow_html=True,
)
