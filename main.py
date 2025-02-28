import json
import os
import urllib.parse
from datetime import datetime

from flask import Flask, redirect, request, session, render_template
import requests
from dotenv import load_dotenv
from helpers import *

app = Flask(__name__)
app.secret_key = os.urandom(12)

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"


@app.before_request
def verify_token():
    if request.endpoint in ["login", "callback", "refresh_token", "home", "static"]:
        return

    if "access_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session.get("expires_at", 0):
        return redirect("/refresh-token")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    if "access_token" in session:
        return redirect("/get_input")

    scope = "user-read-private user-read-email playlist-read-collaborative playlist-modify-private playlist-modify-public user-top-read user-read-recently-played playlist-read-private"

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True,
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


@app.route("/callback")
def callback():
    if "error" in request.args:
        return redirect("/")

    if "code" in request.args:
        request_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

    response = requests.post(TOKEN_URL, data=request_body)
    token_info = response.json()

    session["access_token"] = token_info["access_token"]
    session["refresh_token"] = token_info["refresh_token"]
    session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]

    return redirect("/get_input")


@app.route("/get_input")
def get_input():
    return render_template("get_input.html")


@app.route("/get_interval_listening_data")
def get_listening_interval():
    return render_template("get_listening_interval.html")


@app.route("/short_term_listening_data")
def get_short_listening_data():
    top_tracks = get_top_tracks("short", limit=30)
    items = create_top_song_dict(top_tracks)
    return render_template("songs.html", songs=items)


@app.route("/mid_term_listening_data")
def get_mid_listening_data():
    top_tracks = get_top_tracks("medium", limit=30)
    items = create_top_song_dict(top_tracks)
    return render_template("songs.html", songs=items)


@app.route("/long_term_listening_data")
def get_long_listening_data():
    top_tracks = get_top_tracks("long", limit=30)
    items = create_top_song_dict(top_tracks)
    return render_template("songs.html", songs=items)


@app.route("/display_playlists")
def display_playlists():
    json_result = get_playlists()

    if json_result == None:
        return "There are no playlists available."

    items = []
    for item in json_result:
        id = item["id"]
        image_url = item["images"][0]["url"]
        link = item["external_urls"]["spotify"]
        name = item["name"] if item["name"] else ""
        items.append({"name": name, "link": link, "image_url": image_url, "id": id})
    return render_template("playlist.html", playlists=items)


@app.route("/playlist_songs/<playlist_id>", methods=["GET", "POST"])
def playlist_songs(playlist_id):
    headers = {"Authorization": "Bearer " + session["access_token"]}
    all_tracks = []
    offset = 0

    while True:
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50&offset={offset}",
            headers=headers,
        )
        if not response:
            return "No such playlist exists"
        json_result = json.loads(response.content)["items"]
        all_tracks.extend(json_result)
        if len(json_result) < 50:
            break
        offset += 50
    items = create_playlist_song_dict(all_tracks)

    playlist_name = request.args.get("playlist_name", "")
    playlist_link = request.args.get("playlist_link", "")

    return render_template(
        "playlist_songs.html",
        songs=items,
        playlist_name=playlist_name,
        playlist_link=playlist_link,
    )


@app.route("/get_interval_artist_data")
def get_artist_interval():
    return render_template("get_artist_interval.html")


@app.route("/short_term_artist_data")
def get_short_artist_data():
    top_artists = get_top_artists("short", limit=30)
    items = create_artist_dict(top_artists)
    return render_template("artists.html", artists=items)


@app.route("/mid_term_artist_data")
def get_mid_artist_data():
    top_artists = get_top_artists("medium", limit=30)
    items = create_artist_dict(top_artists)
    return render_template("artists.html", artists=items)


@app.route("/long_term_artist_data")
def get_long_artist_data():
    top_artists = get_top_artists("long", limit=30)
    items = create_artist_dict(top_artists)
    return render_template("artists.html", artists=items)


@app.route("/refresh-token")
def refresh_token():
    if "refresh_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
            "client_id": CLIENT_ID,
        }

    response = requests.post(TOKEN_URL, data=request_body)
    new_token_info = response.json()

    session["access_token"] = new_token_info["access_token"]
    session["expires_at"] = datetime.now().timestamp() + new_token_info["expires_in"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
