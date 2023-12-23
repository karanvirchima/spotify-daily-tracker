import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="d949fdef00594bcd98e6dd5ee250e0a8",
                                                     client_secret="d9bba50de97d46838b716796b9259be1",
                                                     redirect_uri="http://localhost:8888/callback",
                                                     scope="user-top-read user-read-recently-played"))

def get_time_listened(sp):
    total_time_ms = 0
    results = sp.current_user_recently_played(limit=50)
    for item in results['items']:
        total_time_ms += item['track']['duration_ms']
    
    # Convert milliseconds to hours, minutes, and seconds
    total_seconds = total_time_ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the string to return it as "X hrs Y min Z sec"
    return f"{hours} hrs {minutes} min {seconds} sec"

# def get_top_artists(sp, time_range='short_term', limit=5):
#     top_artists = sp.current_user_top_artists(time_range=time_range, limit=limit)
#     return [(artist['name'], artist['genres']) for artist in top_artists['items']]

def get_top_artists(sp, time_range='short_term', limit=5):
    top_artists = sp.current_user_top_artists(time_range=time_range, limit=limit)
    artists_and_genres = [(artist['name'], artist['genres']) for artist in top_artists['items']]
    print("Top Artists and Genres:", artists_and_genres)  # Debug print
    return artists_and_genres

def get_genres_from_top_artists(top_artists):
    genres = set()
    for artist_name, artist_genres in top_artists:
        genres.update(artist_genres)
    print("Fetched Genres:", genres)  # Debug print
    return list(genres)


def get_top_tracks(sp, time_range='short_term', limit=5):
    top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    return [(track['name'], track['artists'][0]['name']) for track in top_tracks['items']]

def get_user_profile(sp):
    user_profile = sp.current_user()
    return user_profile['display_name']

def get_user_profile(sp):
    user_profile = sp.current_user()
    display_name = user_profile['display_name']
    # The user's profile picture is stored in an array; grab the first one if it exists
    profile_pic_url = user_profile['images'][0]['url'] if user_profile['images'] else None
    return display_name, profile_pic_url

def main():
    sp = create_spotify_client()
    user_name = get_user_profile(sp)
    profile_pic_url = get_user_profile(sp)
    total_time_listened = get_time_listened(sp)
    top_artists = get_top_artists(sp)
    top_tracks = get_top_tracks(sp)
    genres_listened = get_genres_from_top_artists(top_artists)

    print(f"Total Time Listened: {total_time_listened} minutes")
    print("Top Artists:", top_artists)
    print("Top Tracks:", top_tracks)
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
