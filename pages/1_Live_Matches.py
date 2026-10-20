"""
Live Matches page – real-time / recent / upcoming from Cricbuzz API (or mock).
"""

import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.api_client import (
    get_live_matches,
    get_recent_matches,
    get_upcoming_matches,
    get_match_scorecard,
)

st.set_page_config(page_title="Live Matches | Cricbuzz LiveStats", page_icon="⚡", layout="wide")
st.title("⚡ Live Matches")
st.caption("Data from Cricbuzz Cricket API (RapidAPI). Falls back to mock data if no API key is set.")

tab_live, tab_recent, tab_upcoming = st.tabs(["🔴 Live", "✅ Recent", "📅 Upcoming"])


def render_match_card(m: dict):
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            st.markdown(f"**{m.get('team1', 'Team 1')} vs {m.get('team2', 'Team 2')}**")
            st.caption(f"{m.get('series', '')} · {m.get('description', '')} · {m.get('format', '')}")
        with c2:
            st.markdown(f"**{m.get('team1_score') or '—'}**")
            st.caption(m.get("team1", ""))
        with c3:
            st.markdown(f"**{m.get('team2_score') or '—'}**")
            st.caption(m.get("team2", ""))
        st.markdown(f"📍 {m.get('venue', '')}, {m.get('city', '')}")
        if m.get("status"):
            st.info(m["status"])
        mid = m.get("match_id")
        if mid and st.button("View Scorecard", key=f"sc_{mid}"):
            sc = get_match_scorecard(mid)
            if sc:
                st.json(sc)
            else:
                st.warning("Scorecard not available.")


with tab_live:
    with st.spinner("Fetching live matches..."):
        matches = get_live_matches()
    if not matches:
        st.warning("No live matches right now (or API unavailable).")
    else:
        st.success(f"Found {len(matches)} live match(es)")
        for m in matches:
            render_match_card(m)

with tab_recent:
    with st.spinner("Fetching recent matches..."):
        matches = get_recent_matches()
    if not matches:
        st.warning("No recent matches found.")
    else:
        for m in matches:
            render_match_card(m)

with tab_upcoming:
    with st.spinner("Fetching upcoming matches..."):
        matches = get_upcoming_matches()
    if not matches:
        st.warning("No upcoming matches found.")
    else:
        for m in matches:
            render_match_card(m)
