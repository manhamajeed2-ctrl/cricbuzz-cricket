"""
Top Player Stats – from local DB + optional API trending.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.db_connection import execute_query
from utils.api_client import get_trending_players

st.set_page_config(page_title="Player Stats | Cricbuzz LiveStats", page_icon="📊", layout="wide")
st.title("📊 Top Player Stats")

tab_bat, tab_bowl, tab_trend = st.tabs(["🏏 Batting Leaders", "🎯 Bowling Leaders", "🔥 Trending (API)"])

with tab_bat:
    fmt = st.selectbox("Format", ["ODI", "Test", "T20I"], key="bat_fmt")
    metric = st.selectbox("Rank by", ["runs", "average", "strike_rate", "centuries"], key="bat_metric")
    limit = st.slider("Show top N", 5, 30, 10, key="bat_n")

    q = f"""
    SELECT p.full_name AS Player, p.country AS Country,
           bs.runs AS Runs, bs.average AS Average, bs.strike_rate AS SR,
           bs.centuries AS Hundreds, bs.fifties AS Fifties, bs.matches AS Matches
    FROM player_batting_stats bs
    JOIN players p ON bs.player_id = p.player_id
    WHERE bs.format = ?
    ORDER BY bs.{metric} DESC
    LIMIT ?
    """
    rows = execute_query(q, (fmt, limit))
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        fig = px.bar(df, x="Player", y=metric.title() if metric != "strike_rate" else "SR",
                     color="Country", title=f"Top {limit} by {metric} ({fmt})")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No batting data found. Run `python init_db.py` first.")

with tab_bowl:
    fmt = st.selectbox("Format", ["ODI", "Test", "T20I"], key="bowl_fmt")
    metric = st.selectbox("Rank by", ["wickets", "bowling_average", "economy_rate"], key="bowl_metric")
    limit = st.slider("Show top N", 5, 30, 10, key="bowl_n")
    order = "ASC" if metric in ("bowling_average", "economy_rate") else "DESC"

    q = f"""
    SELECT p.full_name AS Player, p.country AS Country,
           bw.wickets AS Wickets, bw.bowling_average AS Avg,
           bw.economy_rate AS Economy, bw.matches AS Matches, bw.best_bowling AS Best
    FROM player_bowling_stats bw
    JOIN players p ON bw.player_id = p.player_id
    WHERE bw.format = ?
    ORDER BY bw.{metric} {order}
    LIMIT ?
    """
    rows = execute_query(q, (fmt, limit))
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
        ycol = "Wickets" if metric == "wickets" else ("Avg" if metric == "bowling_average" else "Economy")
        fig = px.bar(df, x="Player", y=ycol, color="Country",
                     title=f"Top {limit} by {metric} ({fmt})")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No bowling data found.")

with tab_trend:
    st.caption("Trending players from Cricbuzz API (requires RAPIDAPI_KEY).")
    if st.button("Refresh Trending"):
        st.rerun()
    players = get_trending_players()
    if players:
        df = pd.DataFrame(players)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("Could not fetch trending players. Check API key or try again later.")
