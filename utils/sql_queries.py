"""
25 SQL Practice Questions for Cricbuzz LiveStats.
Each entry: title, description, level, sql.
"""

QUERIES = [
    # ========== BEGINNER 1-8 ==========
    {
        "id": 1,
        "level": "Beginner",
        "title": "Indian Players",
        "description": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "sql": """
SELECT full_name, playing_role, batting_style, bowling_style
FROM players
WHERE country = 'India'
ORDER BY full_name;
""",
    },
    {
        "id": 2,
        "level": "Beginner",
        "title": "Recent Matches (Last 30 Days)",
        "description": "Show all cricket matches played in the last 30 days. Include match description, both team names, venue name with city, and match date. Sort by most recent first.",
        "sql": """
SELECT m.match_description,
       t1.team_name AS team1,
       t2.team_name AS team2,
       v.venue_name || ', ' || v.city AS venue,
       m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= date('now', '-30 days')
ORDER BY m.match_date DESC;
""",
    },
    {
        "id": 3,
        "level": "Beginner",
        "title": "Top 10 ODI Run Scorers",
        "description": "List the top 10 highest run scorers in ODI cricket. Show player name, total runs, batting average, and centuries. Highest first.",
        "sql": """
SELECT p.full_name, bs.runs, bs.average, bs.centuries
FROM player_batting_stats bs
JOIN players p ON bs.player_id = p.player_id
WHERE bs.format = 'ODI'
ORDER BY bs.runs DESC
LIMIT 10;
""",
    },
    {
        "id": 4,
        "level": "Beginner",
        "title": "Large Capacity Venues",
        "description": "Display all venues with seating capacity > 50,000. Show name, city, country, capacity. Largest first.",
        "sql": """
SELECT venue_name, city, country, capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;
""",
    },
    {
        "id": 5,
        "level": "Beginner",
        "title": "Team Wins Count",
        "description": "Calculate how many matches each team has won. Show team name and total wins. Most wins first.",
        "sql": """
SELECT t.team_name, COUNT(*) AS total_wins
FROM matches m
JOIN teams t ON m.winner_id = t.team_id
WHERE m.winner_id IS NOT NULL
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;
""",
    },
    {
        "id": 6,
        "level": "Beginner",
        "title": "Players by Role",
        "description": "Count how many players belong to each playing role. Show role and count.",
        "sql": """
SELECT playing_role, COUNT(*) AS player_count
FROM players
WHERE playing_role IS NOT NULL
GROUP BY playing_role
ORDER BY player_count DESC;
""",
    },
    {
        "id": 7,
        "level": "Beginner",
        "title": "Highest Score by Format",
        "description": "Find the highest individual batting score in each format (Test, ODI, T20I).",
        "sql": """
SELECT format, MAX(highest_score) AS highest_score
FROM player_batting_stats
WHERE format IN ('Test', 'ODI', 'T20I')
GROUP BY format
ORDER BY format;
""",
    },
    {
        "id": 8,
        "level": "Beginner",
        "title": "Series Starting in 2024",
        "description": "Show all series that started in 2024. Include name, host country, match type, start date, total matches.",
        "sql": """
SELECT series_name, host_country, match_type, start_date, total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date;
""",
    },
    # ========== INTERMEDIATE 9-16 ==========
    {
        "id": 9,
        "level": "Intermediate",
        "title": "All-rounders 1000+ Runs & 50+ Wickets",
        "description": "Find all-rounder players with >1000 runs AND >50 wickets. Show name, runs, wickets, format.",
        "sql": """
SELECT p.full_name,
       bs.runs AS total_runs,
       bw.wickets AS total_wickets,
       bs.format
FROM players p
JOIN player_batting_stats bs ON p.player_id = bs.player_id
JOIN player_bowling_stats bw ON p.player_id = bw.player_id AND bs.format = bw.format
WHERE p.playing_role = 'All-rounder'
  AND bs.runs > 1000
  AND bw.wickets > 50
ORDER BY bs.runs DESC;
""",
    },
    {
        "id": 10,
        "level": "Intermediate",
        "title": "Last 20 Completed Matches",
        "description": "Details of the last 20 completed matches: description, teams, winner, margin, victory type, venue.",
        "sql": """
SELECT m.match_description,
       t1.team_name AS team1,
       t2.team_name AS team2,
       tw.team_name AS winner,
       m.victory_margin,
       m.victory_type,
       v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams tw ON m.winner_id = tw.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.status = 'completed'
ORDER BY m.match_date DESC
LIMIT 20;
""",
    },
    {
        "id": 11,
        "level": "Intermediate",
        "title": "Multi-format Batting Comparison",
        "description": "Players who played ≥2 formats: runs in Test, ODI, T20I and overall batting average.",
        "sql": """
SELECT p.full_name,
       MAX(CASE WHEN bs.format = 'Test' THEN bs.runs END) AS test_runs,
       MAX(CASE WHEN bs.format = 'ODI' THEN bs.runs END) AS odi_runs,
       MAX(CASE WHEN bs.format = 'T20I' THEN bs.runs END) AS t20i_runs,
       ROUND(SUM(bs.runs * bs.average) / NULLIF(SUM(bs.runs), 0), 2) AS overall_avg
FROM players p
JOIN player_batting_stats bs ON p.player_id = bs.player_id
WHERE bs.format IN ('Test', 'ODI', 'T20I')
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT bs.format) >= 2
ORDER BY overall_avg DESC;
""",
    },
    {
        "id": 12,
        "level": "Intermediate",
        "title": "Home vs Away Performance",
        "description": "Team wins at home vs away (venue country = team country → home).",
        "sql": """
SELECT t.team_name,
       SUM(CASE WHEN v.country = t.country THEN 1 ELSE 0 END) AS home_wins,
       SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) AS away_wins
FROM matches m
JOIN teams t ON m.winner_id = t.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.winner_id IS NOT NULL
GROUP BY t.team_id, t.team_name
ORDER BY home_wins + away_wins DESC;
""",
    },
    {
        "id": 13,
        "level": "Intermediate",
        "title": "100+ Run Partnerships",
        "description": "Consecutive batting positions with combined ≥100 runs in same innings.",
        "sql": """
SELECT p1.full_name AS batsman1,
       p2.full_name AS batsman2,
       (b1.runs + b2.runs) AS partnership_runs,
       b1.innings_number,
       b1.match_id
FROM batting_innings b1
JOIN batting_innings b2
  ON b1.match_id = b2.match_id
 AND b1.innings_number = b2.innings_number
 AND b2.batting_position = b1.batting_position + 1
JOIN players p1 ON b1.player_id = p1.player_id
JOIN players p2 ON b2.player_id = p2.player_id
WHERE (b1.runs + b2.runs) >= 100
ORDER BY partnership_runs DESC
LIMIT 30;
""",
    },
    {
        "id": 14,
        "level": "Intermediate",
        "title": "Bowling at Venues (≥3 matches)",
        "description": "Bowlers with ≥3 matches at same venue, ≥4 overs per match: avg economy, total wickets, matches.",
        "sql": """
SELECT p.full_name,
       v.venue_name,
       ROUND(AVG(bi.economy), 2) AS avg_economy,
       SUM(bi.wickets) AS total_wickets,
       COUNT(DISTINCT bi.match_id) AS matches_at_venue
FROM bowling_innings bi
JOIN players p ON bi.player_id = p.player_id
JOIN matches m ON bi.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE bi.overs >= 4
GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name
HAVING COUNT(DISTINCT bi.match_id) >= 3
ORDER BY avg_economy ASC
LIMIT 25;
""",
    },
    {
        "id": 15,
        "level": "Intermediate",
        "title": "Close Match Performers",
        "description": "Players in close matches (<50 runs or <5 wickets): avg runs, close matches played, wins when batting.",
        "sql": """
WITH close_matches AS (
  SELECT match_id, winner_id
  FROM matches
  WHERE (victory_type = 'runs' AND victory_margin < 50)
     OR (victory_type = 'wickets' AND victory_margin < 5)
)
SELECT p.full_name,
       ROUND(AVG(bi.runs), 1) AS avg_runs,
       COUNT(DISTINCT bi.match_id) AS close_matches,
       SUM(CASE WHEN cm.winner_id IS NOT NULL THEN 1 ELSE 0 END) AS team_wins_in_close
FROM batting_innings bi
JOIN close_matches cm ON bi.match_id = cm.match_id
JOIN players p ON bi.player_id = p.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT bi.match_id) >= 2
ORDER BY avg_runs DESC
LIMIT 20;
""",
    },
    {
        "id": 16,
        "level": "Intermediate",
        "title": "Yearly Batting Trends (since 2020)",
        "description": "Avg runs & strike rate per year for players with ≥5 matches that year.",
        "sql": """
SELECT p.full_name,
       strftime('%Y', m.match_date) AS year,
       ROUND(AVG(bi.runs), 1) AS avg_runs,
       ROUND(AVG(bi.strike_rate), 1) AS avg_sr,
       COUNT(*) AS matches
FROM batting_innings bi
JOIN matches m ON bi.match_id = m.match_id
JOIN players p ON bi.player_id = p.player_id
WHERE m.match_date >= '2020-01-01'
GROUP BY p.player_id, p.full_name, strftime('%Y', m.match_date)
HAVING COUNT(*) >= 5
ORDER BY year DESC, avg_runs DESC
LIMIT 40;
""",
    },
    # ========== ADVANCED 17-25 ==========
    {
        "id": 17,
        "level": "Advanced",
        "title": "Toss Advantage Analysis",
        "description": "% of matches won by toss-winning team, broken down by bat/bowl decision.",
        "sql": """
SELECT toss_decision,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS wins_after_toss,
       ROUND(100.0 * SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) / COUNT(*), 1) AS win_pct
FROM matches
WHERE toss_winner_id IS NOT NULL
  AND winner_id IS NOT NULL
  AND toss_decision IS NOT NULL
GROUP BY toss_decision;
""",
    },
    {
        "id": 18,
        "level": "Advanced",
        "title": "Most Economical Limited-Overs Bowlers",
        "description": "ODI + T20 economy for bowlers with ≥10 matches and ≥2 overs/match avg.",
        "sql": """
SELECT p.full_name,
       bw.format,
       bw.economy_rate,
       bw.wickets,
       bw.matches
FROM player_bowling_stats bw
JOIN players p ON bw.player_id = p.player_id
WHERE bw.format IN ('ODI', 'T20I', 'T20')
  AND bw.matches >= 10
  AND bw.economy_rate > 0
ORDER BY bw.economy_rate ASC
LIMIT 20;
""",
    },
    {
        "id": 19,
        "level": "Advanced",
        "title": "Most Consistent Batsmen (Std Dev)",
        "description": "Avg runs and stddev of runs (players ≥10 balls/innings, since 2022). Lower stddev = more consistent.",
        "sql": """
SELECT p.full_name,
       ROUND(AVG(bi.runs), 1) AS avg_runs,
       ROUND(AVG(bi.runs * bi.runs) - AVG(bi.runs) * AVG(bi.runs), 2) AS variance_approx,
       COUNT(*) AS innings
FROM batting_innings bi
JOIN matches m ON bi.match_id = m.match_id
JOIN players p ON bi.player_id = p.player_id
WHERE bi.balls_faced >= 10
  AND m.match_date >= '2022-01-01'
GROUP BY p.player_id, p.full_name
HAVING COUNT(*) >= 8
ORDER BY variance_approx ASC
LIMIT 20;
""",
    },
    {
        "id": 20,
        "level": "Advanced",
        "title": "Matches & Average by Format",
        "description": "Count of Test/ODI/T20 matches and batting avg per format. Players with ≥20 total matches.",
        "sql": """
SELECT p.full_name,
       SUM(CASE WHEN bs.format = 'Test' THEN bs.matches ELSE 0 END) AS test_matches,
       MAX(CASE WHEN bs.format = 'Test' THEN bs.average END) AS test_avg,
       SUM(CASE WHEN bs.format = 'ODI' THEN bs.matches ELSE 0 END) AS odi_matches,
       MAX(CASE WHEN bs.format = 'ODI' THEN bs.average END) AS odi_avg,
       SUM(CASE WHEN bs.format IN ('T20I', 'T20') THEN bs.matches ELSE 0 END) AS t20_matches,
       MAX(CASE WHEN bs.format IN ('T20I', 'T20') THEN bs.average END) AS t20_avg
FROM players p
JOIN player_batting_stats bs ON p.player_id = bs.player_id
GROUP BY p.player_id, p.full_name
HAVING SUM(bs.matches) >= 20
ORDER BY (test_matches + odi_matches + t20_matches) DESC;
""",
    },
    {
        "id": 21,
        "level": "Advanced",
        "title": "Comprehensive Performance Ranking",
        "description": "Weighted score from batting + bowling + fielding points. Top performers by format.",
        "sql": """
SELECT p.full_name,
       bs.format,
       ROUND(
         (COALESCE(bs.runs, 0) * 0.01) + (COALESCE(bs.average, 0) * 0.5) + (COALESCE(bs.strike_rate, 0) * 0.3)
         + (COALESCE(bw.wickets, 0) * 2)
         + ((50 - COALESCE(bw.bowling_average, 50)) * 0.5)
         + ((6 - COALESCE(bw.economy_rate, 6)) * 2)
         + (COALESCE(f.catches, 0) * 3) + (COALESCE(f.stumpings, 0) * 5)
       , 1) AS performance_score
FROM players p
LEFT JOIN player_batting_stats bs ON p.player_id = bs.player_id
LEFT JOIN player_bowling_stats bw ON p.player_id = bw.player_id AND bs.format = bw.format
LEFT JOIN fielding_stats f ON p.player_id = f.player_id AND bs.format = f.format
WHERE bs.format IS NOT NULL
ORDER BY performance_score DESC
LIMIT 25;
""",
    },
    {
        "id": 22,
        "level": "Advanced",
        "title": "Head-to-Head (last 3 years, ≥5 matches)",
        "description": "Pair of teams with ≥5 matches: total, wins each, win %.",
        "sql": """
WITH h2h AS (
  SELECT
    CASE WHEN team1_id < team2_id THEN team1_id ELSE team2_id END AS team_a,
    CASE WHEN team1_id < team2_id THEN team2_id ELSE team1_id END AS team_b,
    winner_id,
    victory_margin,
    victory_type
  FROM matches
  WHERE match_date >= date('now', '-3 years')
    AND winner_id IS NOT NULL
)
SELECT ta.team_name AS team1,
       tb.team_name AS team2,
       COUNT(*) AS total_matches,
       SUM(CASE WHEN h.winner_id = h.team_a THEN 1 ELSE 0 END) AS team1_wins,
       SUM(CASE WHEN h.winner_id = h.team_b THEN 1 ELSE 0 END) AS team2_wins,
       ROUND(100.0 * SUM(CASE WHEN h.winner_id = h.team_a THEN 1 ELSE 0 END) / COUNT(*), 1) AS team1_win_pct
FROM h2h h
JOIN teams ta ON h.team_a = ta.team_id
JOIN teams tb ON h.team_b = tb.team_id
GROUP BY h.team_a, h.team_b, ta.team_name, tb.team_name
HAVING COUNT(*) >= 5
ORDER BY total_matches DESC;
""",
    },
    {
        "id": 23,
        "level": "Advanced",
        "title": "Recent Form & Momentum",
        "description": "Last performances: categorize form as Excellent / Good / Average / Poor based on avg runs.",
        "sql": """
WITH recent AS (
  SELECT bi.player_id,
         bi.runs,
         bi.strike_rate,
         ROW_NUMBER() OVER (PARTITION BY bi.player_id ORDER BY m.match_date DESC) AS rn
  FROM batting_innings bi
  JOIN matches m ON bi.match_id = m.match_id
)
SELECT p.full_name,
       ROUND(AVG(CASE WHEN rn <= 5 THEN runs END), 1) AS avg_last_5,
       ROUND(AVG(CASE WHEN rn <= 10 THEN runs END), 1) AS avg_last_10,
       ROUND(AVG(CASE WHEN rn <= 10 THEN strike_rate END), 1) AS avg_sr_last_10,
       SUM(CASE WHEN rn <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS fifties_last_10,
       CASE
         WHEN AVG(CASE WHEN rn <= 5 THEN runs END) >= 50 THEN 'Excellent Form'
         WHEN AVG(CASE WHEN rn <= 5 THEN runs END) >= 35 THEN 'Good Form'
         WHEN AVG(CASE WHEN rn <= 5 THEN runs END) >= 20 THEN 'Average Form'
         ELSE 'Poor Form'
       END AS form_category
FROM recent r
JOIN players p ON r.player_id = p.player_id
WHERE rn <= 10
GROUP BY p.player_id, p.full_name
HAVING COUNT(*) >= 5
ORDER BY avg_last_5 DESC
LIMIT 30;
""",
    },
    {
        "id": 24,
        "level": "Advanced",
        "title": "Best Batting Partnerships",
        "description": "Pairs with ≥5 partnerships: avg runs, 50+ count, highest, success rate.",
        "sql": """
WITH partnerships AS (
  SELECT b1.player_id AS p1,
         b2.player_id AS p2,
         (b1.runs + b2.runs) AS runs
  FROM batting_innings b1
  JOIN batting_innings b2
    ON b1.match_id = b2.match_id
   AND b1.innings_number = b2.innings_number
   AND b2.batting_position = b1.batting_position + 1
)
SELECT pl1.full_name AS batsman1,
       pl2.full_name AS batsman2,
       COUNT(*) AS partnerships,
       ROUND(AVG(runs), 1) AS avg_partnership,
       SUM(CASE WHEN runs >= 50 THEN 1 ELSE 0 END) AS fifty_plus,
       MAX(runs) AS highest,
       ROUND(100.0 * SUM(CASE WHEN runs >= 50 THEN 1 ELSE 0 END) / COUNT(*), 1) AS success_rate
FROM partnerships pt
JOIN players pl1 ON pt.p1 = pl1.player_id
JOIN players pl2 ON pt.p2 = pl2.player_id
GROUP BY pt.p1, pt.p2, pl1.full_name, pl2.full_name
HAVING COUNT(*) >= 5
ORDER BY avg_partnership DESC
LIMIT 20;
""",
    },
    {
        "id": 25,
        "level": "Advanced",
        "title": "Career Trajectory (Quarterly)",
        "description": "Quarterly avg runs & SR; categorize Career Ascending / Declining / Stable.",
        "sql": """
WITH quarterly AS (
  SELECT bi.player_id,
         strftime('%Y', m.match_date) || '-Q' || ((CAST(strftime('%m', m.match_date) AS INTEGER) - 1) / 3 + 1) AS quarter,
         AVG(bi.runs) AS avg_runs,
         AVG(bi.strike_rate) AS avg_sr,
         COUNT(*) AS matches
  FROM batting_innings bi
  JOIN matches m ON bi.match_id = m.match_id
  GROUP BY bi.player_id, quarter
  HAVING COUNT(*) >= 3
),
ordered AS (
  SELECT *,
         LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter) AS prev_avg
  FROM quarterly
)
SELECT p.full_name,
       COUNT(*) AS quarters,
       ROUND(AVG(avg_runs), 1) AS career_avg_runs,
       ROUND(AVG(avg_sr), 1) AS career_avg_sr,
       CASE
         WHEN AVG(CASE WHEN prev_avg IS NOT NULL THEN avg_runs - prev_avg END) > 3 THEN 'Career Ascending'
         WHEN AVG(CASE WHEN prev_avg IS NOT NULL THEN avg_runs - prev_avg END) < -3 THEN 'Career Declining'
         ELSE 'Career Stable'
       END AS trajectory
FROM ordered o
JOIN players p ON o.player_id = p.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(*) >= 4
ORDER BY career_avg_runs DESC
LIMIT 25;
""",
    },
]


def get_query_by_id(qid: int) -> dict | None:
    for q in QUERIES:
        if q["id"] == qid:
            return q
    return None


def get_queries_by_level(level: str) -> list:
    return [q for q in QUERIES if q["level"].lower() == level.lower()]
