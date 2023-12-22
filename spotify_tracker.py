import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="d949fdef00594bcd98e6dd5ee250e0a8",
                                               client_secret="4e3f8248eae6443c9edf9203c4a56a80",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-top-read user-read-recently-played"))

def get_time_listened(sp):
    total_time = 0
    results = sp.current_user_recently_played(limit=50)
    for item in results['items']:
        total_time += item['track']['duration_ms']
    return total_time / 60000  # Convert to minutes

def get_top_artists(sp, time_range='short_term', limit=10):
    top_artists = sp.current_user_top_artists(time_range=time_range, limit=limit)
    return [(artist['name'], artist['genres']) for artist in top_artists['items']]

def get_genres_from_top_artists(top_artists):
    genres = set()
    for name, artist_genres in top_artists:
        genres.update(artist_genres)
    return list(genres)

def main():
    total_time_listened = get_time_listened(sp)
    top_artists = get_top_artists(sp)
    genres_listened = get_genres_from_top_artists(top_artists)

    print(f"Total Time Listened: {total_time_listened} minutes")
    print("Top Artists:", top_artists)
    print("Genres Listened:", genres_listened)

if __name__ == "__main__":
    main()

