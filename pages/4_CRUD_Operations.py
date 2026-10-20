"""
CRUD Operations for players (and simple match view).
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.db_connection import execute_query, execute_write

st.set_page_config(page_title="CRUD | Cricbuzz LiveStats", page_icon="🛠️", layout="wide")
st.title("🛠️ CRUD Operations")
st.caption("Create, Read, Update, Delete player records.")

tab_read, tab_create, tab_update, tab_delete = st.tabs(
    ["📖 Read / List", "➕ Create", "✏️ Update", "🗑️ Delete"]
)

# ---------- READ ----------
with tab_read:
    st.subheader("All Players")
    search = st.text_input("Search by name or country")
    if search:
        rows = execute_query(
            """SELECT player_id, full_name, country, playing_role, batting_style, bowling_style
               FROM players
               WHERE full_name LIKE ? OR country LIKE ?
               ORDER BY full_name""",
            (f"%{search}%", f"%{search}%"),
        )
    else:
        rows = execute_query(
            """SELECT player_id, full_name, country, playing_role, batting_style, bowling_style
               FROM players ORDER BY player_id"""
        )
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.caption(f"Total: {len(rows)} players")
    else:
        st.info("No players found. Run `python init_db.py` first.")

# ---------- CREATE ----------
with tab_create:
    st.subheader("Add New Player")
    with st.form("create_player"):
        full_name = st.text_input("Full Name *")
        country = st.text_input("Country *")
        role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        bat_style = st.text_input("Batting Style", value="Right-handed")
        bowl_style = st.text_input("Bowling Style")
        dob = st.date_input("Date of Birth", value=None)
        submitted = st.form_submit_button("Create Player")
        if submitted:
            if not full_name or not country:
                st.error("Name and Country are required.")
            else:
                try:
                    # Get next id
                    max_id = execute_query("SELECT COALESCE(MAX(player_id), 0) + 1 AS nid FROM players")
                    nid = max_id[0]["nid"]
                    execute_write(
                        """INSERT INTO players (player_id, full_name, country, playing_role, batting_style, bowling_style, date_of_birth)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (nid, full_name, country, role, bat_style or None, bowl_style or None,
                         dob.isoformat() if dob else None),
                    )
                    st.success(f"Player '{full_name}' created with ID {nid}")
                except Exception as e:
                    st.error(str(e))

# ---------- UPDATE ----------
with tab_update:
    st.subheader("Update Player")
    players = execute_query("SELECT player_id, full_name FROM players ORDER BY full_name")
    if not players:
        st.warning("No players in database.")
    else:
        options = {f"{p['full_name']} (ID {p['player_id']})": p["player_id"] for p in players}
        selected = st.selectbox("Select player", list(options.keys()))
        pid = options[selected]
        current = execute_query("SELECT * FROM players WHERE player_id = ?", (pid,))[0]

        with st.form("update_player"):
            full_name = st.text_input("Full Name", value=current["full_name"])
            country = st.text_input("Country", value=current["country"])
            role = st.selectbox(
                "Playing Role",
                ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"],
                index=["Batsman", "Bowler", "All-rounder", "Wicket-keeper"].index(
                    current["playing_role"] or "Batsman"
                ),
            )
            bat_style = st.text_input("Batting Style", value=current["batting_style"] or "")
            bowl_style = st.text_input("Bowling Style", value=current["bowling_style"] or "")
            submitted = st.form_submit_button("Update Player")
            if submitted:
                try:
                    execute_write(
                        """UPDATE players
                           SET full_name=?, country=?, playing_role=?, batting_style=?, bowling_style=?
                           WHERE player_id=?""",
                        (full_name, country, role, bat_style or None, bowl_style or None, pid),
                    )
                    st.success(f"Player ID {pid} updated successfully.")
                except Exception as e:
                    st.error(str(e))

# ---------- DELETE ----------
with tab_delete:
    st.subheader("Delete Player")
    st.warning("This permanently removes the player record (stats may remain orphaned).")
    players = execute_query("SELECT player_id, full_name, country FROM players ORDER BY full_name")
    if players:
        options = {f"{p['full_name']} – {p['country']} (ID {p['player_id']})": p["player_id"] for p in players}
        selected = st.selectbox("Select player to delete", list(options.keys()), key="del_sel")
        pid = options[selected]
        if st.button("🗑️ Confirm Delete", type="primary"):
            try:
                execute_write("DELETE FROM players WHERE player_id = ?", (pid,))
                st.success(f"Player ID {pid} deleted.")
                st.rerun()
            except Exception as e:
                st.error(str(e))
    else:
        st.info("No players to delete.")
