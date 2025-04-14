import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.nba_stats import (
    get_player_id,
    get_all_player_stats,
    get_top_players_by_stat,
)
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from src.fantasy_calc import calcular_fantasy_pontos as fantasy_row_calc
import time


# Função para obter imagem do jogador
def get_player_img_url(player_id):
    return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"


# Função para obter a posição do jogador
def get_player_position(player_id):
    time.sleep(0.6)
    info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    df_info = info.get_data_frames()[0]
    return df_info["POSITION"].values[0]


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
            background-color: #2E2E2E;
        }
        h1, h2, h3, .stMarkdown, .stTextInput > label, .stSelectbox > label {
            color: #FFA500;
        }
        .block-container {
            padding: 2rem 2rem 1rem;
            background-color: #2E2E2E;
        }
        div.stButton > button:first-child {
            background-color: #FFA500;
            color: white;
            padding: 0.6em 1.2em;
            border-radius: 8px;
            font-weight: bold;
        }
        .stDataFrame, .stTable {
            background-color: #f5f5f5;
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
            all_stats = get_all_player_stats()

            row1 = all_stats[all_stats["PLAYER_NAME"] == player1_name].iloc[0]
            row2 = all_stats[all_stats["PLAYER_NAME"] == player2_name].iloc[0]

            stats1 = row1.to_dict()
            stats2 = row2.to_dict()

            stats1["Fantasy Points"] = fantasy_row_calc(stats1)
            stats2["Fantasy Points"] = fantasy_row_calc(stats2)

            # Posição dos jogadores
            pos1 = get_player_position(id1)
            pos2 = get_player_position(id2)

            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(
                    get_player_img_url(id1),
                    width=250,
                    caption=f"{player1_name} - {pos1}",
                )
            with col_img2:
                st.image(
                    get_player_img_url(id2),
                    width=250,
                    caption=f"{player2_name} - {pos2}",
                )

            df_comparison = pd.DataFrame(
                [stats1, stats2],
                index=[f"{player1_name} ({pos1})", f"{player2_name} ({pos2})"],
            )
            st.subheader("📋 Estatísticas Gerais + Fantasy Points")
            st.dataframe(df_comparison)

            # Gráfico de barras
            st.subheader("📈 Comparação Visual")
            fig = go.Figure()
            cores = ["#FFA500", "#FF4500"]
            for idx, (player, stats) in enumerate(
                zip(
                    [f"{player1_name} ({pos1})", f"{player2_name} ({pos2})"],
                    [stats1, stats2],
                )
            ):
                fig.add_trace(
                    go.Bar(
                        x=["PTS", "AST", "REB", "STL", "BLK", "Fantasy Points"],
                        y=[
                            stats["PTS"],
                            stats["AST"],
                            stats["REB"],
                            stats["STL"],
                            stats["BLK"],
                            stats["Fantasy Points"],
                        ],
                        name=player,
                        marker_color=cores[idx % len(cores)],
                    )
                )

            fig.update_layout(
                barmode="group",
                title="Comparação de Estatísticas e Fantasy",
                plot_bgcolor="#4F4F4F",
                paper_bgcolor="#4F4F4F",
                font=dict(color="white"),
                legend=dict(bgcolor="#4F4F4F", font=dict(color="white")),
            )
            st.plotly_chart(fig, use_container_width=True)

# Tab 2: Top 25 por Estatística
with tabs[1]:
    st.subheader("📋 Ver Top 25 da Temporada por Estatística")
    all_stats = get_all_player_stats()
    all_stats["Fantasy Points"] = all_stats.apply(fantasy_row_calc, axis=1)

    stat_options = ["PTS", "AST", "REB", "STL", "BLK"]
    stat = st.selectbox("Estatística", stat_options)

    top_players = get_top_players_by_stat(all_stats, stat=stat)
    st.dataframe(top_players)

    fig_bar = go.Figure(
        go.Bar(
            x=top_players[stat][::-1],
            y=top_players["PLAYER_NAME"][::-1],
            orientation="h",
            marker_color="#FFA500",
        )
    )
    fig_bar.update_layout(
        title=f"Top 25 jogadores em {stat}",
        xaxis_title=stat,
        yaxis_title="Jogador",
        height=750,
        plot_bgcolor="#4F4F4F",
        paper_bgcolor="#4F4F4F",
        font=dict(color="white"),
        legend=dict(bgcolor="#4F4F4F", font=dict(color="white")),
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
            marker_color="#FF8C00",
        )
    )
    fig_top_fantasy.update_layout(
        title="Top 25 Jogadores por Pontuação Fantasy",
        xaxis_title="Fantasy Points",
        yaxis_title="Jogador",
        height=750,
        plot_bgcolor="#4F4F4F",
        paper_bgcolor="#4F4F4F",
        font=dict(color="white"),
        legend=dict(bgcolor="#4F4F4F", font=dict(color="white")),
    )
    st.plotly_chart(fig_top_fantasy, use_container_width=True)

# Rodapé
st.markdown("---")
st.markdown(
    "<center>Feito por <a href='https://github.com/mucarii' style='color:#FFA500;'>Murilo Calore</a></center>",
    unsafe_allow_html=True,
)
