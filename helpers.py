import requests
import json

from flask import session, url_for


def process_data(json_result):
    items = []
    for i, item in enumerate(json_result):
        link = item["external_urls"]["spotify"]
        name = item["name"] if item["name"] else "No playlist name."
        items.append(f"<p>{i + 1}. <a href={link}>{name}</a></p>")
    output = "".join(items)
    return output


def get_top_tracks(time_range, limit=30):
    headers = {"Authorization": "Bearer " + session["access_token"]}
    response = requests.get(
        f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}_term&limit={limit}",
        headers=headers,
    )
    if not response:
        return "No listening data"
    json_result = json.loads(response.content)["items"]
    return json_result


def get_top_artists(time_range, limit=30):
    headers = {"Authorization": "Bearer " + session["access_token"]}
    response = requests.get(
        f"https://api.spotify.com/v1/me/top/artists?time_range={time_range}_term&limit={limit}",
        headers=headers,
    )
    if not response:
        return "No listening data"
    json_result = json.loads(response.content)["items"]
    return json_result


def create_top_song_dict(json_result):
    items = []
    for item in json_result:
        album_image = item["album"]["images"][0]["url"]
        link = item["external_urls"]["spotify"]
        name = item["name"] if item["name"] else "No playlist name."
        items.append({"name": name, "link": link, "image_url": album_image})
    return items


def get_playlists():
    headers = {"Authorization": "Bearer " + session["access_token"]}
    all_playlists = []
    offset = 0

    while True:
        response = requests.get(
            f"https://api.spotify.com/v1/me/playlists?limit=50&offset={offset}",
            headers=headers,
        )
        if not response:
            return None
        json_result = json.loads(response.content)["items"]
        all_playlists.extend(json_result)
        if len(json_result) < 50:
            break
        offset += 50

    return all_playlists


def create_playlist_song_dict(json_result):
    items = []
    for item in json_result:
        album_image = (
            item["track"]["album"]["images"][0]["url"]
            if item["track"]["album"]["images"]
            else url_for("static", filename="no_image.png")
        )
        link = (
            item["track"]["external_urls"]["spotify"]
            if item["track"]["external_urls"]
            else None
        )
        name = item["track"]["name"] if item["track"]["name"] else "No playlist name."
        items.append({"name": name, "link": link, "image_url": album_image})
    return items


def create_artist_dict(json_result):
    items = []
    for item in json_result:
        artist_image = (
            item["images"][0]["url"]
            if item["images"]
            else url_for("static", filename="no_image.png")
        )
        link = item["external_urls"]["spotify"]
        name = item["name"]
        items.append({"name": name, "link": link, "image_url": artist_image})
    return items
