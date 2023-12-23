from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_tracker import get_time_listened, get_top_artists, get_genres_from_top_artists, get_top_tracks, get_user_profile

app = Flask(__name__)

def create_spotify_client():
    """Creates and returns a new Spotipy client instance."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="d949fdef00594bcd98e6dd5ee250e0a8",
                                                     client_secret="d9bba50de97d46838b716796b9259be1",
                                                     redirect_uri="http://localhost:8888/callback",
                                                     scope="user-top-read user-read-recently-played"))

@app.route('/')
def index():
    sp = create_spotify_client()
    user_name, profile_pic_url = get_user_profile(sp)
    total_time_listened = get_time_listened(sp)  
    top_artists = get_top_artists(sp)  
    top_tracks = get_top_tracks(sp)  
    genres_listened = get_genres_from_top_artists(top_artists)  
    genres_count = [1] * len(genres_listened)
    return render_template('index.html', genres_listened=genres_listened, genres_count=genres_count,  user_name=user_name, profile_pic_url=profile_pic_url, total_time=total_time_listened, top_artists=top_artists,  top_tracks=top_tracks)

if __name__ == '__main__':
    app.run(debug=True)
