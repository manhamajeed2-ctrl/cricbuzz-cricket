"""
SQL Queries & Analytics – all 25 practice questions.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from utils.db_connection import execute_query, ensure_seeded, get_db_path
from utils.sql_queries import QUERIES

st.set_page_config(page_title="SQL Analytics | Cricbuzz LiveStats", page_icon="🔍", layout="wide")
st.title("🔍 SQL Queries & Analytics")
st.caption("25 practice questions across Beginner, Intermediate and Advanced levels.")

if not ensure_seeded():
    st.error(
        f"Database empty or missing at `{get_db_path()}`.\n\n"
        "Run `python init_db.py` locally, or ensure `data/cricket.db` is committed for Streamlit Cloud."
    )
    st.stop()

levels = ["All", "Beginner", "Intermediate", "Advanced"]
selected_level = st.selectbox("Filter by level", levels)

filtered = QUERIES if selected_level == "All" else [q for q in QUERIES if q["level"] == selected_level]

options = {f"Q{q['id']}: {q['title']} ({q['level']})": q for q in filtered}
choice = st.selectbox("Select a question", list(options.keys()))

q = options[choice]

st.markdown(f"### Question {q['id']} – {q['title']}")
st.info(q["description"])

with st.expander("View SQL", expanded=True):
    st.code(q["sql"].strip(), language="sql")

col1, col2 = st.columns([1, 4])
with col1:
    run = st.button("▶️ Run Query", type="primary")

if run:
    try:
        with st.spinner("Executing..."):
            rows = execute_query(q["sql"])
        if rows:
            df = pd.DataFrame(rows)
            st.success(f"Returned {len(df)} row(s)")
            st.dataframe(df, use_container_width=True, hide_index=True)
            # Simple download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, f"query_{q['id']}_results.csv", "text/csv")
        else:
            st.warning("Query returned no rows.")
    except Exception as e:
        st.error(f"Error executing query: {e}")

st.markdown("---")
st.subheader("✏️ Custom SQL")
custom = st.text_area("Write your own SELECT query (read-only safety)", height=150,
                      placeholder="SELECT * FROM players LIMIT 10;")
if st.button("Run Custom Query"):
    if not custom.strip().lower().startswith("select"):
        st.error("Only SELECT statements are allowed for safety.")
    else:
        try:
            rows = execute_query(custom)
            if rows:
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            else:
                st.info("No rows returned.")
        except Exception as e:
            st.error(str(e))
