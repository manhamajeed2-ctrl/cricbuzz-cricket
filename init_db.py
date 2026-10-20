"""
Initialize the cricket database with schema and realistic sample data
sufficient to run all 25 SQL practice questions.
"""

import sqlite3
from pathlib import Path
from datetime import date, timedelta
import random

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "data" / "cricket.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"


def init_database(force: bool = False):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists() and not force:
        print(f"Database already exists at {DB_PATH}. Use force=True to recreate.")
        return

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")

    # Apply schema
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    # ---------- TEAMS ----------
    teams = [
        (1, "India", "India", "international"),
        (2, "Australia", "Australia", "international"),
        (3, "England", "England", "international"),
        (4, "Pakistan", "Pakistan", "international"),
        (5, "South Africa", "South Africa", "international"),
        (6, "New Zealand", "New Zealand", "international"),
        (7, "West Indies", "West Indies", "international"),
        (8, "Sri Lanka", "Sri Lanka", "international"),
        (9, "Bangladesh", "Bangladesh", "international"),
        (10, "Afghanistan", "Afghanistan", "international"),
        (11, "Mumbai Indians", "India", "league"),
        (12, "Chennai Super Kings", "India", "league"),
    ]
    conn.executemany(
        "INSERT INTO teams (team_id, team_name, country, team_type) VALUES (?, ?, ?, ?)",
        teams,
    )

    # ---------- VENUES ----------
    venues = [
        (1, "Narendra Modi Stadium", "Ahmedabad", "India", 132000),
        (2, "Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
        (3, "Eden Gardens", "Kolkata", "India", 68000),
        (4, "Lord's", "London", "England", 30000),
        (5, "Wankhede Stadium", "Mumbai", "India", 33108),
        (6, "Sydney Cricket Ground", "Sydney", "Australia", 48000),
        (7, "The Oval", "London", "England", 25500),
        (8, "Newlands", "Cape Town", "South Africa", 25000),
        (9, "Gaddafi Stadium", "Lahore", "Pakistan", 27000),
        (10, "R. Premadasa Stadium", "Colombo", "Sri Lanka", 35000),
        (11, "Eden Park", "Auckland", "New Zealand", 50000),
        (12, "Kensington Oval", "Bridgetown", "West Indies", 28000),
        (13, "M. Chinnaswamy Stadium", "Bengaluru", "India", 40000),
        (14, "Adelaide Oval", "Adelaide", "Australia", 53500),
        (15, "Trent Bridge", "Nottingham", "England", 17500),
    ]
    conn.executemany(
        "INSERT INTO venues (venue_id, venue_name, city, country, capacity) VALUES (?, ?, ?, ?, ?)",
        venues,
    )

    # ---------- SERIES ----------
    series = [
        (1, "ICC Cricket World Cup 2023", "India", "ODI", "2023-10-05", "2023-11-19", 48),
        (2, "Border-Gavaskar Trophy 2024-25", "Australia", "Test", "2024-11-22", "2025-01-07", 5),
        (3, "India vs England ODI Series 2025", "India", "ODI", "2025-01-22", "2025-02-12", 3),
        (4, "T20 World Cup 2024", "West Indies", "T20I", "2024-06-01", "2024-06-29", 55),
        (5, "Pakistan vs Australia Test Series 2024", "Pakistan", "Test", "2024-03-12", "2024-03-26", 2),
        (6, "IPL 2024", "India", "T20", "2024-03-22", "2024-05-26", 74),
        (7, "India vs South Africa T20I Series 2024", "South Africa", "T20I", "2024-11-08", "2024-11-15", 4),
        (8, "Asia Cup 2023", "Sri Lanka", "ODI", "2023-08-30", "2023-09-17", 13),
        (9, "England vs Australia Ashes 2023", "England", "Test", "2023-06-16", "2023-07-31", 5),
        (10, "New Zealand vs India Test Series 2024", "India", "Test", "2024-10-16", "2024-11-05", 3),
    ]
    conn.executemany(
        """INSERT INTO series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        series,
    )

    # ---------- PLAYERS ----------
    players = [
        # India
        (1, "Virat Kohli", "India", "Batsman", "Right-handed", "Right-arm medium", "1988-11-05"),
        (2, "Rohit Sharma", "India", "Batsman", "Right-handed", "Right-arm offbreak", "1987-04-30"),
        (3, "Jasprit Bumrah", "India", "Bowler", "Right-handed", "Right-arm fast", "1993-12-06"),
        (4, "Ravindra Jadeja", "India", "All-rounder", "Left-handed", "Left-arm orthodox", "1988-12-06"),
        (5, "KL Rahul", "India", "Wicket-keeper", "Right-handed", None, "1992-04-18"),
        (6, "Hardik Pandya", "India", "All-rounder", "Right-handed", "Right-arm medium-fast", "1993-10-11"),
        (7, "Mohammed Shami", "India", "Bowler", "Right-handed", "Right-arm fast", "1990-09-03"),
        (8, "Suryakumar Yadav", "India", "Batsman", "Right-handed", "Right-arm medium", "1990-09-14"),
        (9, "Rishabh Pant", "India", "Wicket-keeper", "Left-handed", None, "1997-10-04"),
        (10, "Kuldeep Yadav", "India", "Bowler", "Left-handed", "Left-arm wrist-spin", "1994-12-14"),
        # Australia
        (11, "Steve Smith", "Australia", "Batsman", "Right-handed", "Right-arm legbreak", "1989-06-02"),
        (12, "David Warner", "Australia", "Batsman", "Left-handed", "Right-arm legbreak", "1986-10-27"),
        (13, "Pat Cummins", "Australia", "Bowler", "Right-handed", "Right-arm fast", "1993-05-08"),
        (14, "Mitchell Starc", "Australia", "Bowler", "Left-handed", "Left-arm fast", "1990-01-30"),
        (15, "Glenn Maxwell", "Australia", "All-rounder", "Right-handed", "Right-arm offbreak", "1988-10-14"),
        (16, "Travis Head", "Australia", "Batsman", "Left-handed", "Right-arm offbreak", "1993-12-29"),
        (17, "Josh Hazlewood", "Australia", "Bowler", "Left-handed", "Right-arm fast-medium", "1991-01-08"),
        (18, "Alex Carey", "Australia", "Wicket-keeper", "Left-handed", None, "1991-08-27"),
        # England
        (19, "Joe Root", "England", "Batsman", "Right-handed", "Right-arm offbreak", "1990-12-30"),
        (20, "Ben Stokes", "England", "All-rounder", "Left-handed", "Right-arm fast-medium", "1991-06-04"),
        (21, "Jos Buttler", "England", "Wicket-keeper", "Right-handed", None, "1990-09-08"),
        (22, "James Anderson", "England", "Bowler", "Left-handed", "Right-arm fast-medium", "1982-07-30"),
        (23, "Harry Brook", "England", "Batsman", "Right-handed", "Right-arm medium", "1999-02-22"),
        (24, "Jofra Archer", "England", "Bowler", "Right-handed", "Right-arm fast", "1995-04-01"),
        # Pakistan
        (25, "Babar Azam", "Pakistan", "Batsman", "Right-handed", "Right-arm offbreak", "1994-10-15"),
        (26, "Shaheen Afridi", "Pakistan", "Bowler", "Left-handed", "Left-arm fast", "2000-04-06"),
        (27, "Mohammad Rizwan", "Pakistan", "Wicket-keeper", "Right-handed", None, "1992-06-01"),
        (28, "Shadab Khan", "Pakistan", "All-rounder", "Right-handed", "Right-arm legbreak", "1998-10-04"),
        # South Africa
        (29, "Quinton de Kock", "South Africa", "Wicket-keeper", "Left-handed", None, "1992-12-17"),
        (30, "Kagiso Rabada", "South Africa", "Bowler", "Left-handed", "Right-arm fast", "1995-05-25"),
        (31, "Aiden Markram", "South Africa", "Batsman", "Right-handed", "Right-arm offbreak", "1994-10-04"),
        (32, "Heinrich Klaasen", "South Africa", "Wicket-keeper", "Right-handed", None, "1991-07-30"),
        # New Zealand
        (33, "Kane Williamson", "New Zealand", "Batsman", "Right-handed", "Right-arm offbreak", "1990-08-08"),
        (34, "Trent Boult", "New Zealand", "Bowler", "Right-handed", "Left-arm fast-medium", "1989-07-22"),
        (35, "Devon Conway", "New Zealand", "Batsman", "Left-handed", "Right-arm medium", "1991-07-08"),
        # Others
        (36, "Shakib Al Hasan", "Bangladesh", "All-rounder", "Left-handed", "Left-arm orthodox", "1987-03-24"),
        (37, "Rashid Khan", "Afghanistan", "Bowler", "Right-handed", "Right-arm legbreak", "1998-09-20"),
        (38, "Nicholas Pooran", "West Indies", "Wicket-keeper", "Left-handed", None, "1995-10-02"),
        (39, "Wanindu Hasaranga", "Sri Lanka", "All-rounder", "Right-handed", "Right-arm legbreak", "1997-07-29"),
        (40, "Shoaib Malik", "Pakistan", "All-rounder", "Right-handed", "Right-arm offbreak", "1982-02-01"),
    ]
    conn.executemany(
        """INSERT INTO players (player_id, full_name, country, playing_role, batting_style, bowling_style, date_of_birth)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        players,
    )

    # ---------- BATTING STATS ----------
    batting_stats = [
        # player_id, format, matches, innings, runs, highest, avg, sr, 100s, 50s, 4s, 6s
        (1, "ODI", 295, 281, 13848, 183, 58.07, 93.6, 50, 72, 1294, 151),
        (1, "Test", 113, 191, 8848, 254, 49.15, 55.6, 29, 30, 986, 26),
        (1, "T20I", 125, 117, 4188, 122, 48.7, 137.0, 1, 38, 369, 124),
        (2, "ODI", 265, 257, 10709, 264, 48.9, 90.0, 31, 55, 995, 331),
        (2, "Test", 62, 106, 4301, 212, 44.3, 55.0, 12, 17, 482, 88),
        (2, "T20I", 159, 151, 4237, 121, 32.1, 140.9, 5, 32, 383, 205),
        (4, "ODI", 197, 132, 2756, 87, 32.4, 85.0, 0, 13, 199, 54),
        (4, "Test", 73, 108, 3216, 175, 36.9, 56.0, 4, 20, 320, 64),
        (4, "T20I", 74, 48, 515, 46, 21.5, 127.0, 0, 0, 36, 17),
        (5, "ODI", 78, 73, 2888, 112, 45.1, 88.0, 7, 18, 230, 52),
        (5, "Test", 55, 95, 3257, 199, 34.3, 55.0, 8, 18, 390, 25),
        (5, "T20I", 72, 68, 2265, 110, 37.8, 139.0, 2, 22, 191, 99),
        (6, "ODI", 92, 68, 1769, 92, 33.4, 113.0, 0, 11, 132, 66),
        (6, "T20I", 104, 85, 1812, 71, 26.6, 142.0, 0, 9, 129, 96),
        (8, "ODI", 37, 35, 744, 117, 24.0, 105.0, 1, 4, 76, 19),
        (8, "T20I", 60, 58, 2141, 117, 46.5, 171.0, 4, 17, 194, 123),
        (9, "ODI", 30, 26, 865, 125, 36.0, 106.0, 1, 5, 88, 26),
        (9, "Test", 33, 56, 2271, 159, 42.1, 73.0, 5, 11, 247, 56),
        (11, "ODI", 156, 142, 5431, 164, 43.1, 87.0, 12, 31, 495, 52),
        (11, "Test", 109, 195, 9685, 239, 56.9, 54.0, 32, 41, 1072, 54),
        (11, "T20I", 67, 56, 1208, 90, 28.1, 125.0, 0, 7, 100, 40),
        (12, "ODI", 161, 159, 6932, 179, 45.3, 97.0, 22, 33, 733, 130),
        (12, "Test", 112, 205, 8786, 335, 44.6, 70.0, 26, 37, 1036, 69),
        (12, "T20I", 110, 110, 3277, 100, 33.4, 142.0, 1, 28, 335, 122),
        (15, "ODI", 138, 127, 3895, 108, 33.6, 125.0, 4, 23, 368, 150),
        (15, "T20I", 111, 101, 2495, 145, 29.0, 154.0, 5, 12, 208, 141),
        (16, "ODI", 72, 70, 2675, 152, 43.1, 101.0, 6, 16, 295, 58),
        (16, "Test", 52, 87, 3749, 175, 46.3, 63.0, 9, 17, 445, 28),
        (16, "T20I", 65, 63, 1659, 91, 32.5, 148.0, 0, 12, 158, 72),
        (19, "ODI", 171, 160, 6522, 133, 49.4, 86.0, 16, 39, 560, 46),
        (19, "Test", 140, 257, 11968, 254, 50.9, 55.0, 31, 62, 1280, 28),
        (19, "T20I", 32, 30, 893, 90, 35.7, 126.0, 0, 5, 71, 29),
        (20, "ODI", 112, 95, 3279, 102, 39.0, 95.0, 3, 24, 266, 96),
        (20, "Test", 105, 190, 6501, 258, 36.1, 58.0, 13, 31, 758, 116),
        (20, "T20I", 43, 36, 700, 52, 23.3, 132.0, 0, 2, 48, 32),
        (21, "ODI", 181, 154, 5022, 162, 40.5, 118.0, 11, 26, 414, 173),
        (21, "T20I", 112, 103, 3260, 101, 35.4, 144.0, 1, 26, 282, 144),
        (25, "ODI", 128, 125, 5729, 158, 56.7, 89.0, 19, 31, 520, 60),
        (25, "Test", 54, 98, 3898, 196, 45.3, 53.0, 9, 26, 430, 18),
        (25, "T20I", 120, 113, 4145, 122, 41.0, 129.0, 3, 36, 430, 74),
        (27, "ODI", 85, 78, 2931, 131, 43.1, 90.0, 4, 20, 255, 42),
        (27, "T20I", 100, 90, 3146, 104, 48.4, 127.0, 1, 28, 250, 82),
        (29, "ODI", 155, 150, 5943, 178, 44.0, 95.0, 17, 29, 620, 110),
        (29, "T20I", 80, 79, 2277, 79, 32.5, 135.0, 0, 15, 205, 87),
        (33, "ODI", 161, 153, 6554, 148, 47.8, 81.0, 13, 42, 580, 55),
        (33, "Test", 100, 176, 8743, 251, 54.3, 51.0, 32, 34, 950, 20),
        (33, "T20I", 87, 85, 2464, 95, 33.3, 123.0, 0, 17, 220, 52),
        (36, "ODI", 247, 234, 7570, 134, 37.4, 82.0, 9, 56, 690, 85),
        (36, "Test", 66, 121, 4609, 217, 39.1, 58.0, 5, 31, 520, 35),
        (36, "T20I", 117, 109, 2382, 84, 23.1, 122.0, 0, 12, 190, 68),
        # Extra all-rounders for Q9
        (28, "ODI", 70, 55, 1205, 86, 28.7, 95.0, 0, 7, 90, 30),
        (28, "T20I", 90, 70, 1100, 52, 22.0, 130.0, 0, 3, 80, 45),
        (39, "ODI", 55, 45, 980, 80, 25.8, 92.0, 0, 5, 70, 20),
        (39, "T20I", 70, 55, 850, 71, 21.3, 135.0, 0, 4, 60, 35),
    ]
    conn.executemany(
        """INSERT INTO player_batting_stats
           (player_id, format, matches, innings, runs, highest_score, average, strike_rate, centuries, fifties, fours, sixes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        batting_stats,
    )

    # ---------- BOWLING STATS ----------
    bowling_stats = [
        # player_id, format, matches, innings, wickets, avg, econ, sr, best, 5w
        (3, "ODI", 89, 88, 149, 23.5, 4.6, 30.5, "6/19", 2),
        (3, "Test", 36, 69, 159, 20.7, 2.7, 45.8, "6/27", 10),
        (3, "T20I", 70, 69, 89, 18.6, 6.6, 16.9, "3/14", 0),
        (4, "ODI", 197, 189, 220, 36.1, 4.9, 44.3, "5/36", 2),
        (4, "Test", 73, 133, 294, 24.6, 2.5, 59.5, "7/48", 13),
        (4, "T20I", 74, 71, 54, 29.9, 7.5, 23.9, "3/15", 0),
        (7, "ODI", 95, 94, 195, 24.0, 5.5, 26.2, "5/69", 5),
        (7, "Test", 64, 122, 229, 27.7, 3.0, 54.6, "6/56", 6),
        (10, "ODI", 110, 107, 170, 27.0, 5.0, 32.3, "6/25", 2),
        (10, "T20I", 40, 39, 66, 14.2, 6.8, 12.5, "5/24", 1),
        (13, "ODI", 88, 87, 143, 27.8, 5.2, 32.0, "5/70", 1),
        (13, "Test", 62, 116, 269, 22.3, 2.9, 46.5, "6/23", 12),
        (13, "T20I", 55, 54, 62, 23.0, 7.5, 18.4, "3/15", 0),
        (14, "ODI", 121, 120, 236, 23.2, 5.1, 27.4, "6/28", 9),
        (14, "Test", 89, 170, 358, 27.5, 3.3, 49.7, "6/28", 14),
        (14, "T20I", 65, 64, 79, 20.5, 7.8, 15.8, "4/20", 0),
        (17, "ODI", 70, 69, 112, 26.5, 4.8, 33.0, "6/52", 3),
        (17, "Test", 70, 130, 270, 25.0, 2.7, 55.0, "6/67", 11),
        (22, "ODI", 194, 191, 269, 29.0, 4.9, 35.5, "5/23", 2),
        (22, "Test", 188, 350, 704, 26.5, 2.8, 56.9, "7/42", 32),
        (24, "ODI", 25, 24, 42, 25.0, 5.0, 30.0, "3/27", 0),
        (24, "T20I", 15, 15, 20, 23.5, 7.2, 19.5, "3/23", 0),
        (26, "ODI", 55, 54, 106, 24.0, 5.4, 26.5, "6/35", 2),
        (26, "Test", 30, 55, 113, 26.5, 3.1, 51.0, "6/51", 4),
        (26, "T20I", 60, 59, 85, 19.0, 7.0, 16.3, "4/22", 0),
        (30, "ODI", 100, 99, 157, 27.5, 5.0, 33.0, "6/16", 2),
        (30, "Test", 62, 113, 291, 22.3, 3.2, 42.0, "7/112", 14),
        (30, "T20I", 55, 54, 70, 20.5, 7.8, 15.8, "3/20", 0),
        (34, "ODI", 114, 113, 187, 25.0, 5.0, 30.0, "7/34", 6),
        (34, "Test", 78, 148, 317, 27.5, 3.0, 55.0, "6/30", 10),
        (34, "T20I", 61, 60, 83, 20.0, 7.5, 16.0, "4/18", 0),
        (36, "ODI", 247, 241, 317, 29.5, 4.5, 39.5, "5/20", 4),
        (36, "Test", 66, 110, 246, 31.0, 2.9, 64.0, "7/36", 19),
        (36, "T20I", 117, 112, 149, 20.5, 6.8, 18.0, "5/20", 2),
        (37, "ODI", 100, 99, 185, 19.5, 4.2, 28.0, "7/18", 4),
        (37, "T20I", 90, 89, 145, 14.0, 6.2, 13.5, "5/3", 2),
        (28, "ODI", 70, 65, 85, 32.0, 5.2, 37.0, "4/27", 0),
        (28, "T20I", 90, 85, 100, 22.0, 7.0, 19.0, "4/8", 0),
        (39, "ODI", 55, 53, 95, 24.0, 5.0, 29.0, "6/9", 2),
        (39, "T20I", 70, 68, 110, 15.5, 6.5, 14.3, "4/9", 1),
        (6, "ODI", 92, 80, 80, 35.0, 5.8, 36.0, "3/31", 0),
        (6, "T20I", 104, 95, 75, 28.0, 8.5, 19.8, "4/16", 0),
        (15, "ODI", 138, 90, 70, 40.0, 5.5, 43.0, "4/46", 0),
        (15, "T20I", 111, 70, 40, 30.0, 8.0, 22.5, "3/10", 0),
        (20, "ODI", 112, 80, 74, 32.0, 5.5, 35.0, "5/61", 1),
        (20, "Test", 105, 160, 200, 31.5, 3.2, 59.0, "6/22", 4),
    ]
    conn.executemany(
        """INSERT INTO player_bowling_stats
           (player_id, format, matches, innings, wickets, bowling_average, economy_rate, strike_rate, best_bowling, five_wickets)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        bowling_stats,
    )

    # ---------- FIELDING STATS ----------
    fielding = [
        (1, "ODI", 150, 0, 5),
        (1, "Test", 120, 0, 8),
        (1, "T20I", 60, 0, 3),
        (5, "ODI", 80, 15, 2),
        (5, "Test", 100, 20, 5),
        (5, "T20I", 40, 10, 1),
        (9, "ODI", 30, 8, 1),
        (9, "Test", 70, 12, 3),
        (18, "ODI", 90, 25, 4),
        (18, "Test", 150, 30, 6),
        (21, "ODI", 180, 40, 5),
        (21, "T20I", 70, 15, 2),
        (27, "ODI", 70, 20, 3),
        (27, "T20I", 50, 12, 2),
        (29, "ODI", 160, 35, 4),
        (29, "T20I", 50, 10, 1),
        (4, "ODI", 90, 0, 10),
        (4, "Test", 80, 0, 12),
        (36, "ODI", 100, 0, 8),
    ]
    conn.executemany(
        "INSERT INTO fielding_stats (player_id, format, catches, stumpings, run_outs) VALUES (?, ?, ?, ?, ?)",
        fielding,
    )

    # ---------- MATCHES (last 2+ years + older for series) ----------
    base = date(2023, 6, 1)
    matches = []
    # Generate ~80 matches across formats
    formats = ["ODI", "Test", "T20I", "T20"]
    team_pairs = [
        (1, 2), (1, 3), (1, 5), (1, 6), (1, 4), (1, 8),
        (2, 3), (2, 5), (2, 6), (3, 5), (4, 5), (6, 3),
        (7, 1), (9, 1), (10, 1), (11, 12),
    ]
    for i in range(1, 85):
        t1, t2 = random.choice(team_pairs)
        fmt = random.choice(formats)
        days_ago = random.randint(0, 900)
        mdate = base + timedelta(days=random.randint(0, 800)) if i > 40 else date.today() - timedelta(days=days_ago)
        # Keep some recent
        if i <= 25:
            mdate = date.today() - timedelta(days=random.randint(1, 60))
        venue = random.randint(1, 15)
        series_id = random.randint(1, 10)
        status = "completed"
        toss = random.choice([t1, t2])
        decision = random.choice(["bat", "bowl"])
        winner = random.choice([t1, t2, None])
        if winner is None and random.random() < 0.85:
            winner = random.choice([t1, t2])
        margin = random.randint(1, 150) if winner else None
        vtype = random.choice(["runs", "wickets"]) if winner else None
        if vtype == "wickets" and margin:
            margin = min(margin, 10)
        desc = f"{['1st', '2nd', '3rd', '4th', '5th'][i % 5]} Match - {fmt}"
        matches.append(
            (i, series_id, desc, t1, t2, venue, mdate.isoformat(), fmt, status,
             toss, decision, winner, margin, vtype)
        )

    conn.executemany(
        """INSERT INTO matches
           (match_id, series_id, match_description, team1_id, team2_id, venue_id,
            match_date, match_format, status, toss_winner_id, toss_decision,
            winner_id, victory_margin, victory_type)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        matches,
    )

    # ---------- BATTING INNINGS (sample performances) ----------
    batting_innings = []
    bowling_innings = []
    for mid in range(1, 85):
        # 2 innings-ish data
        for inn in (1, 2):
            positions = list(range(1, 12))
            random.shuffle(positions)
            for pos, pid in enumerate(random.sample(range(1, 41), k=random.randint(6, 11)), 1):
                runs = max(0, int(random.gauss(25, 30)))
                balls = max(runs, int(runs * random.uniform(0.6, 1.8)))
                if balls == 0:
                    balls = 1
                sr = round(runs / balls * 100, 1) if balls else 0
                fours = random.randint(0, min(runs // 4, 15))
                sixes = random.randint(0, min(runs // 6, 8))
                batting_innings.append(
                    (mid, pid, inn, pos, runs, balls, fours, sixes,
                     random.choice(["caught", "bowled", "lbw", "not out", "run out", None]),
                     sr)
                )
            # Bowlers
            for pid in random.sample(range(1, 41), k=random.randint(4, 7)):
                overs = round(random.uniform(2, 10), 1)
                runs_c = int(overs * random.uniform(4, 10))
                wkts = random.randint(0, 5)
                econ = round(runs_c / overs, 2) if overs else 0
                bowling_innings.append(
                    (mid, pid, inn, overs, random.randint(0, 2), runs_c, wkts, econ)
                )

    conn.executemany(
        """INSERT INTO batting_innings
           (match_id, player_id, innings_number, batting_position, runs, balls_faced, fours, sixes, dismissal_type, strike_rate)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        batting_innings,
    )
    conn.executemany(
        """INSERT INTO bowling_innings
           (match_id, player_id, innings_number, overs, maidens, runs_conceded, wickets, economy)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        bowling_innings,
    )

    conn.commit()
    conn.close()
    print(f"✅ Database initialized successfully at {DB_PATH}")
    print(f"   Tables: teams, venues, series, players, matches,")
    print(f"           player_batting_stats, player_bowling_stats,")
    print(f"           batting_innings, bowling_innings, fielding_stats")


if __name__ == "__main__":
    init_database(force=True)
