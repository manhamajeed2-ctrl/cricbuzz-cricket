-- Cricbuzz LiveStats Database Schema
-- Supports all 25 SQL practice questions

PRAGMA foreign_keys = ON;

-- Teams
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT NOT NULL,
    team_type TEXT DEFAULT 'international'  -- international, league, domestic
);

-- Venues
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY,
    venue_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    capacity INTEGER
);

-- Series
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY,
    series_name TEXT NOT NULL,
    host_country TEXT,
    match_type TEXT,  -- Test, ODI, T20I, T20
    start_date DATE,
    end_date DATE,
    total_matches INTEGER
);

-- Players
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    country TEXT NOT NULL,
    playing_role TEXT,  -- Batsman, Bowler, All-rounder, Wicket-keeper
    batting_style TEXT,
    bowling_style TEXT,
    date_of_birth DATE
);

-- Matches
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    series_id INTEGER,
    match_description TEXT,
    team1_id INTEGER,
    team2_id INTEGER,
    venue_id INTEGER,
    match_date DATE,
    match_format TEXT,  -- Test, ODI, T20I, T20
    status TEXT,  -- completed, live, upcoming
    toss_winner_id INTEGER,
    toss_decision TEXT,  -- bat, bowl
    winner_id INTEGER,
    victory_margin INTEGER,
    victory_type TEXT,  -- runs, wickets
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_id) REFERENCES teams(team_id)
);

-- Player Career Batting Stats (aggregated by format)
CREATE TABLE IF NOT EXISTS player_batting_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    format TEXT NOT NULL,  -- Test, ODI, T20I
    matches INTEGER DEFAULT 0,
    innings INTEGER DEFAULT 0,
    runs INTEGER DEFAULT 0,
    highest_score INTEGER DEFAULT 0,
    average REAL DEFAULT 0,
    strike_rate REAL DEFAULT 0,
    centuries INTEGER DEFAULT 0,
    fifties INTEGER DEFAULT 0,
    fours INTEGER DEFAULT 0,
    sixes INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE(player_id, format)
);

-- Player Career Bowling Stats (aggregated by format)
CREATE TABLE IF NOT EXISTS player_bowling_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    format TEXT NOT NULL,
    matches INTEGER DEFAULT 0,
    innings INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    bowling_average REAL DEFAULT 0,
    economy_rate REAL DEFAULT 0,
    strike_rate REAL DEFAULT 0,
    best_bowling TEXT,
    five_wickets INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE(player_id, format)
);

-- Innings Batting Performances (for detailed queries)
CREATE TABLE IF NOT EXISTS batting_innings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    innings_number INTEGER,
    batting_position INTEGER,
    runs INTEGER DEFAULT 0,
    balls_faced INTEGER DEFAULT 0,
    fours INTEGER DEFAULT 0,
    sixes INTEGER DEFAULT 0,
    dismissal_type TEXT,
    strike_rate REAL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Innings Bowling Performances
CREATE TABLE IF NOT EXISTS bowling_innings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    innings_number INTEGER,
    overs REAL DEFAULT 0,
    maidens INTEGER DEFAULT 0,
    runs_conceded INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    economy REAL,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Fielding Stats
CREATE TABLE IF NOT EXISTS fielding_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    format TEXT NOT NULL,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    run_outs INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE(player_id, format)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format ON matches(match_format);
CREATE INDEX IF NOT EXISTS idx_players_country ON players(country);
CREATE INDEX IF NOT EXISTS idx_players_role ON players(playing_role);
CREATE INDEX IF NOT EXISTS idx_batting_player ON batting_innings(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_player ON bowling_innings(player_id);
CREATE INDEX IF NOT EXISTS idx_batting_stats_format ON player_batting_stats(format);
CREATE INDEX IF NOT EXISTS idx_bowling_stats_format ON player_bowling_stats(format);
