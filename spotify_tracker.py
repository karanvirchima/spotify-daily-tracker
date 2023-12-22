import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="d949fdef00594bcd98e6dd5ee250e0a8",
                                                     client_secret="d9bba50de97d46838b716796b9259be1",
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
    sp = create_spotify_client()
    total_time_listened = get_time_listened(sp)
    top_artists = get_top_artists(sp)
    genres_listened = get_genres_from_top_artists(top_artists)

    print(f"Total Time Listened: {total_time_listened} minutes")
    print("Top Artists:", top_artists)
    print("Genres Listened:", genres_listened)

# The Flask app part would be in a separate file
# from flask import Flask, render_template
# app = Flask(__name__)

# @app.route('/')
# def index():
#     sp = create_spotify_client()
#     total_time_listened = get_time_listened(sp)
#     top_artists = get_top_artists(sp)
#     return render_template('index.html', total_time=total_time_listened, top_artists=top_artists)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    main()
