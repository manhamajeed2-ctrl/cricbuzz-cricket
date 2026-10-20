"""
Cricbuzz Cricket API client via RapidAPI.
Falls back to mock data when RAPIDAPI_KEY is missing or request fails.
"""

import os
import requests
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
HOST = "cricbuzz-cricket.p.rapidapi.com"


def _get_headers() -> Dict[str, str]:
    key = os.getenv("RAPIDAPI_KEY", "").strip()
    return {
        "x-rapidapi-key": key,
        "x-rapidapi-host": HOST,
        "Content-Type": "application/json",
    }


def _has_key() -> bool:
    return bool(os.getenv("RAPIDAPI_KEY", "").strip())


def _get(endpoint: str, params: Optional[Dict] = None) -> Optional[Any]:
    """Perform GET request. Returns None on failure."""
    if not _has_key():
        return None
    url = f"{BASE_URL}{endpoint}"
    try:
        resp = requests.get(url, headers=_get_headers(), params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json()
        # 204 No Content or other
        return None
    except Exception:
        return None


# -------------------- Live / Recent / Upcoming --------------------

def get_live_matches() -> List[Dict]:
    data = _get("/matches/v1/live")
    if data is None:
        return _mock_live_matches()
    return _parse_match_list(data)


def get_recent_matches() -> List[Dict]:
    data = _get("/matches/v1/recent")
    if data is None:
        return _mock_recent_matches()
    return _parse_match_list(data)


def get_upcoming_matches() -> List[Dict]:
    data = _get("/matches/v1/upcoming")
    if data is None:
        return _mock_upcoming_matches()
    return _parse_match_list(data)


def get_match_scorecard(match_id: int) -> Optional[Dict]:
    data = _get(f"/mcenter/v1/{match_id}/scard")
    if data is None:
        return _mock_scorecard(match_id)
    return data


def get_match_info(match_id: int) -> Optional[Dict]:
    data = _get(f"/mcenter/v1/{match_id}")
    if data is None:
        return None
    return data


def get_player_stats(player_id: int, stat_type: str = "batting") -> Optional[Dict]:
    """stat_type: batting | bowling | career"""
    endpoint = f"/stats/v1/player/{player_id}/{stat_type}"
    return _get(endpoint)


def search_players(name: str) -> List[Dict]:
    data = _get("/stats/v1/player/search", params={"plrN": name})
    if data is None:
        return []
    return data.get("player", []) if isinstance(data, dict) else []


def get_trending_players() -> List[Dict]:
    data = _get("/stats/v1/player/trending")
    if data is None:
        return _mock_trending()
    return data.get("player", []) if isinstance(data, dict) else []


# -------------------- Parsers --------------------

def _parse_match_list(data: Any) -> List[Dict]:
    """Flatten typeMatches / seriesMatches structure into simple list."""
    matches = []
    if not isinstance(data, dict):
        return matches
    for type_match in data.get("typeMatches", []):
        for series in type_match.get("seriesMatches", []):
            series_obj = series.get("seriesAdWrapper") or series
            series_name = series_obj.get("seriesName", "Unknown Series")
            for m in series_obj.get("matches", []):
                info = m.get("matchInfo", {})
                score = m.get("matchScore", {})
                matches.append({
                    "match_id": info.get("matchId"),
                    "series": series_name,
                    "description": info.get("matchDesc", ""),
                    "format": info.get("matchFormat", ""),
                    "state": info.get("state", ""),
                    "status": info.get("status", ""),
                    "team1": info.get("team1", {}).get("teamName", "Team 1"),
                    "team2": info.get("team2", {}).get("teamName", "Team 2"),
                    "team1_score": _extract_score(score, "team1Score"),
                    "team2_score": _extract_score(score, "team2Score"),
                    "venue": info.get("venueInfo", {}).get("ground", ""),
                    "city": info.get("venueInfo", {}).get("city", ""),
                    "start_date": info.get("startDate"),
                })
    return matches


def _extract_score(score_obj: Dict, key: str) -> str:
    try:
        innings = score_obj.get(key, {})
        # Prefer first innings or latest
        for k in ("inngs1", "inngs2"):
            if k in innings:
                inn = innings[k]
                runs = inn.get("runs", 0)
                wkts = inn.get("wickets", 0)
                overs = inn.get("overs", "")
                return f"{runs}/{wkts} ({overs})"
        return ""
    except Exception:
        return ""


# -------------------- Mock data (offline / no-key mode) --------------------

def _mock_live_matches() -> List[Dict]:
    return [
        {
            "match_id": 90001,
            "series": "India vs Australia 2025",
            "description": "2nd ODI",
            "format": "ODI",
            "state": "In Progress",
            "status": "India need 45 runs in 30 balls",
            "team1": "India",
            "team2": "Australia",
            "team1_score": "278/6 (45.0)",
            "team2_score": "312/8 (50.0)",
            "venue": "Wankhede Stadium",
            "city": "Mumbai",
            "start_date": None,
        },
        {
            "match_id": 90002,
            "series": "T20 World Cup Qualifier",
            "description": "Match 12",
            "format": "T20I",
            "state": "In Progress",
            "status": "England won the toss and elected to bat",
            "team1": "England",
            "team2": "South Africa",
            "team1_score": "142/4 (15.2)",
            "team2_score": "",
            "venue": "The Oval",
            "city": "London",
            "start_date": None,
        },
    ]


def _mock_recent_matches() -> List[Dict]:
    return [
        {
            "match_id": 89001,
            "series": "Border-Gavaskar Trophy",
            "description": "1st Test",
            "format": "Test",
            "state": "Complete",
            "status": "Australia won by 8 wickets",
            "team1": "India",
            "team2": "Australia",
            "team1_score": "180 & 235",
            "team2_score": "337 & 79/2",
            "venue": "Melbourne Cricket Ground",
            "city": "Melbourne",
            "start_date": None,
        },
        {
            "match_id": 89002,
            "series": "Asia Cup",
            "description": "Final",
            "format": "ODI",
            "state": "Complete",
            "status": "India won by 10 wickets",
            "team1": "India",
            "team2": "Sri Lanka",
            "team1_score": "51/0 (6.1)",
            "team2_score": "50 (15.2)",
            "venue": "R. Premadasa Stadium",
            "city": "Colombo",
            "start_date": None,
        },
    ]


def _mock_upcoming_matches() -> List[Dict]:
    return [
        {
            "match_id": 91001,
            "series": "India vs England",
            "description": "1st T20I",
            "format": "T20I",
            "state": "Upcoming",
            "status": "Starts in 2 days",
            "team1": "India",
            "team2": "England",
            "team1_score": "",
            "team2_score": "",
            "venue": "Narendra Modi Stadium",
            "city": "Ahmedabad",
            "start_date": None,
        },
    ]


def _mock_scorecard(match_id: int) -> Dict:
    return {
        "match_id": match_id,
        "status": "Mock scorecard – set RAPIDAPI_KEY for live data",
        "scorecard": [
            {
                "batTeamName": "India",
                "batsman": [
                    {"name": "Rohit Sharma", "runs": 45, "balls": 38, "fours": 5, "sixes": 2},
                    {"name": "Virat Kohli", "runs": 82, "balls": 70, "fours": 8, "sixes": 1},
                    {"name": "KL Rahul", "runs": 56, "balls": 48, "fours": 4, "sixes": 2},
                ],
                "bowler": [
                    {"name": "Pat Cummins", "overs": 10, "maidens": 1, "runs": 48, "wickets": 2},
                    {"name": "Mitchell Starc", "overs": 10, "maidens": 0, "runs": 55, "wickets": 1},
                ],
            }
        ],
    }


def _mock_trending() -> List[Dict]:
    return [
        {"id": 1, "name": "Virat Kohli", "teamName": "India"},
        {"id": 3, "name": "Jasprit Bumrah", "teamName": "India"},
        {"id": 13, "name": "Pat Cummins", "teamName": "Australia"},
        {"id": 25, "name": "Babar Azam", "teamName": "Pakistan"},
    ]
