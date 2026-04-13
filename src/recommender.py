from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

MOOD_VALENCE = {
    "happy":   0.85,
    "relaxed": 0.70,
    "chill":   0.60,
    "focused": 0.55,
    "intense": 0.50,
    "moody":   0.40,
}

GENRE_SIMILARITY = {
    frozenset({"pop",      "indie pop"}):  0.75,
    frozenset({"lofi",     "ambient"}):    0.65,
    frozenset({"lofi",     "jazz"}):       0.50,
    frozenset({"pop",      "synthwave"}):  0.40,
    frozenset({"jazz",     "ambient"}):    0.40,
    frozenset({"rock",     "synthwave"}):  0.35,
    frozenset({"indie pop","synthwave"}):  0.30,
    frozenset({"pop",      "rock"}):       0.25,
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects ranked by score for the given user."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        results = recommend_songs(user_prefs, [asdict(s) for s in self.songs], k)
        return [Song(**song_dict) for song_dict, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable string explaining why a song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        _, reasons = score_song(user_prefs, asdict(song))
        components = " and ".join(component for component, _ in reasons)
        # combined = sum(score for _, score in reasons)
        return f"Recommended mainly for {components}"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads a songs CSV and returns a list of song dicts with typed fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Returns a (score, reasons) tuple reflecting how well a song matches user preferences."""
    user_genre    = user_prefs.get("genre", "")
    song_genre    = song["genre"]
    likes_acoustic = user_prefs.get("likes_acoustic", False)

    energy_score = 1 - abs(song["energy"] - user_prefs.get("energy", 0.5))

    if user_genre == song_genre:
        genre_score = 1.0
    else:
        genre_score = GENRE_SIMILARITY.get(frozenset({user_genre, song_genre}), 0.0)

    target_valence = MOOD_VALENCE.get(user_prefs.get("mood", ""), 0.60)
    valence_score  = 1 - abs(song["valence"] - target_valence)

    danceability_score = song["danceability"]

    acousticness_score = song["acousticness"] if likes_acoustic else 1 - song["acousticness"]

    weighted = {
        "energy":       0.35 * energy_score,
        "genre":        0.30 * genre_score,
        "valence":      0.20 * valence_score,
        "danceability": 0.10 * danceability_score,
        "acousticness": 0.05 * acousticness_score,
    }

    score = sum(weighted.values())
    top_two = sorted(weighted, key=weighted.get, reverse=True)[:2]
    reasons = tuple((component, int(weighted[component] * 100)) for component in top_two)

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top-k scored songs as (song_dict, score, explanation) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, reasons[0]) for song, score, reasons in ranked[:k]]
