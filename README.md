# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A comprehensive cricket analytics dashboard that integrates **live data from the Cricbuzz API** (via RapidAPI) with a **SQLite database** and a multi-page **Streamlit** web application.

## Features

| Page | Description |
|------|-------------|
| **Home** | Project overview, tech stack, structure |
| **Live Matches** | Live / Recent / Upcoming matches + scorecards |
| **Player Stats** | Top batting & bowling leaders with charts + trending players |
| **SQL Analytics** | All **25 SQL practice questions** (Beginner → Advanced) + custom query runner |
| **CRUD Operations** | Create / Read / Update / Delete player records |

## Tech Stack

- **Python 3.10+**
- **Streamlit** – interactive multi-page dashboard
- **SQLite** – lightweight SQL database (easy to switch to PostgreSQL/MySQL)
- **pandas** + **Plotly** – data handling & visualization
- **requests** + **python-dotenv** – REST API client
- **Cricbuzz Cricket API** (RapidAPI)

## Project Structure

```
cricbuzz_livestats/
├── app.py                      # Landing / Home page
├── pages/
│   ├── 1_Live_Matches.py
│   ├── 2_Player_Stats.py
│   ├── 3_SQL_Analytics.py
│   └── 4_CRUD_Operations.py
├── utils/
│   ├── api_client.py           # RapidAPI wrapper + mock fallback
│   ├── db_connection.py        # SQLite helpers
│   └── sql_queries.py          # All 25 SQL questions
├── sql/
│   └── schema.sql
├── data/
│   └── cricket.db              # Created by init_db.py
├── init_db.py                  # Schema + sample data seeder
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start (Local)

### 1. Clone / Download & Enter Directory

```bash
cd cricbuzz_livestats
```

### 2. Create Virtual Environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
python init_db.py
```

This creates `data/cricket.db` with schema + realistic sample data for all 25 SQL questions.

### 5. (Optional) Add RapidAPI Key for Live Data

1. Sign up at [RapidAPI – Cricbuzz Cricket](https://rapidapi.com/cricketapilive/api/cricbuzz-cricket/)
2. Subscribe to a free/basic plan and copy your key
3. Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and set:
RAPIDAPI_KEY=your_actual_key_here
```

Without a key the app still works fully using **mock live data** + the local database.

### 6. Run the Dashboard

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## SQL Practice Questions

All 25 questions from the project brief are implemented and runnable from the **SQL Analytics** page:

- **Beginner (1–8)** – SELECT, WHERE, GROUP BY, ORDER BY
- **Intermediate (9–16)** – JOINs, subqueries, aggregates
- **Advanced (17–25)** – Window functions, CTEs, rankings, form analysis

You can also write custom `SELECT` queries on the same page.

## Database Schema (summary)

- `teams`, `venues`, `series`, `players`
- `matches` (with toss, winner, margin)
- `player_batting_stats`, `player_bowling_stats`, `fielding_stats`
- `batting_innings`, `bowling_innings` (ball-by-ball style aggregates for advanced queries)

## Notes & Guidelines Followed

- PEP 8 style
- Proper exception handling for API & DB
- API key kept out of code (`.env`)
- Modular design (`utils/`)
- Works offline (mock + SQLite)
- CRUD via form-based UI

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `No module named 'utils'` | Run from project root: `streamlit run app.py` |
| Empty tables | Run `python init_db.py` again |
| API returns nothing | Check `RAPIDAPI_KEY` in `.env` or use mock mode |
| Port already in use | `streamlit run app.py --server.port 8502` |

## License

Educational / project use. Cricket data © respective owners. API usage subject to RapidAPI terms.

---

**Skills practiced:** Python • SQL • Streamlit • JSON • REST API • Database design • Data analytics
