"""
Cricbuzz LiveStats – Main Streamlit entry point.
Run with: streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import sys

# Ensure project root is on path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a5f2a;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-left: 5px solid #2e7d32;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🏏 Cricbuzz LiveStats</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-Time Cricket Insights & SQL-Based Analytics</p>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>⚡ Live Match Page</h3>
        <p>Real-time match updates, scorecards, and venue details from the Cricbuzz API.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Top Player Stats</h3>
        <p>Top batting & bowling leaders across formats with clean visualizations.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🔍 SQL Analytics</h3>
        <p>25 ready-to-run SQL practice questions (Beginner → Advanced) on the cricket database.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-card">
        <h3>🛠️ CRUD Operations</h3>
        <p>Full Create / Read / Update / Delete for players and match records.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.subheader("🚀 Getting Started")
st.markdown("""
1. Use the **sidebar** to navigate between pages.
2. For live API data, add your RapidAPI key to a `.env` file (see `.env.example`).
3. Without a key the app runs fully offline using mock data + the local SQLite database.
4. First-time setup: run `python init_db.py` to create the database with sample data.
""")

st.subheader("🛠️ Tech Stack")
st.code("Python • Streamlit • SQLite • pandas • requests • Plotly • REST API (RapidAPI Cricbuzz)", language=None)

st.subheader("📁 Project Structure")
st.code("""
cricbuzz_livestats/
├── app.py                 # Home / landing page
├── pages/
│   ├── 1_Live_Matches.py
│   ├── 2_Player_Stats.py
│   ├── 3_SQL_Analytics.py
│   └── 4_CRUD_Operations.py
├── utils/
│   ├── api_client.py
│   ├── db_connection.py
│   └── sql_queries.py
├── data/cricket.db
├── sql/schema.sql
├── init_db.py
├── requirements.txt
└── README.md
""", language=None)

st.info("👈 Select a page from the sidebar to explore the full dashboard.")
