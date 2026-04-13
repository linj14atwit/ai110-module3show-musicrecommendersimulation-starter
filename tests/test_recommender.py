from src.recommender import Song, UserProfile, Recommender, score_song, asdict

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_power_ballad_ranks_below_happy_song():
    # Edge case 1: high energy but sad song should lose to a genuinely happy song
    # Stadium Tears matches on genre and energy but has very low valence (0.28)
    songs = [
        Song(id=1, title="Happy Rock Anthem", artist="Test Artist", genre="rock",
             mood="happy", energy=0.88, tempo_bpm=138, valence=0.82, danceability=0.65, acousticness=0.10),
        Song(id=2, title="Stadium Tears", artist="Echo Vault", genre="rock",
             mood="moody", energy=0.89, tempo_bpm=138, valence=0.28, danceability=0.57, acousticness=0.12),
    ]
    user = UserProfile(favorite_genre="rock", favorite_mood="happy", target_energy=0.88, likes_acoustic=False)
    results = Recommender(songs).recommend(user, k=2)
    assert results[0].title == "Happy Rock Anthem"


def test_tempo_blindness_scores_identically():
    # Edge case 2: two jazz songs identical except tempo_bpm — algorithm must score them the same
    # because tempo_bpm is not used in score_song
    slow_jazz = Song(id=1, title="Slow Jazz", artist="A", genre="jazz", mood="relaxed",
                     energy=0.35, tempo_bpm=75,  valence=0.72, danceability=0.50, acousticness=0.90)
    fast_jazz = Song(id=2, title="Fast Samba Jazz", artist="B", genre="jazz", mood="relaxed",
                     energy=0.35, tempo_bpm=172, valence=0.72, danceability=0.50, acousticness=0.90)
    user_prefs = {"genre": "jazz", "mood": "relaxed", "energy": 0.35, "likes_acoustic": True}
    slow_score, _ = score_song(user_prefs, asdict(slow_jazz))
    fast_score, _ = score_song(user_prefs, asdict(fast_jazz))
    assert slow_score == fast_score


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
