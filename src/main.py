"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    if (songs := load_songs("data/songs.csv")):
        print(f"Loaded {len(songs)} songs.")
    else:
        print("Failed to load songs.")
        return

    # Starter example profile
    # user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Edge case 1: happy high-energy pop fan
    # Expects upbeat songs — risks getting Stadium Tears (high energy, but valence 0.28)
    user_prefs = {"genre": "rock", "mood": "happy", "energy": 0.88}

    # Edge case 2: relaxed jazz listener who wants slow, low-energy jazz
    # Expects Afternoon Jazz (0.33 energy, 85bpm) — risks getting Samba Sunrise (172bpm)
    # because tempo_bpm is not used in scoring, only danceability and genre match
    # user_prefs = {"genre": "jazz", "mood": "relaxed", "energy": 0.33}

    

    print(f"User preferences: {user_prefs}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
