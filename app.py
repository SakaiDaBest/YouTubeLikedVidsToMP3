from flask import Flask, request, url_for, session, redirect
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from pathlib import Path
import yt_dlp as youtube_dl
from youtubesearchpython import VideosSearch
import os
import pandas as pd

#Code by Wong Wei Jun : D

app = Flask(__name__)
app.secret_key = "pihfwaeiufopa278349hjiafawei"
app.config['SESSION_COOKIE_NAME'] = 'Wong_Cookie'
TOKEN_INFO = "token_info"


@app.route('/')
def login():
    sp_oauth = create_youtube_oauth()
    auth_url, _ = sp_oauth.authorization_url(prompt='consent')
    return redirect(auth_url)


@app.route('/redirect') 
def redirect_page():  
    sp_oauth = create_youtube_oauth()
    code = request.args.get('code')
    sp_oauth.fetch_token(code=code)
    credentials = sp_oauth.credentials
    session[TOKEN_INFO] = credentials_to_dict(credentials)
    return redirect(url_for('get_tracks', _external=True))


@app.route('/getTracks')
def get_tracks():
    try:
        token_info = get_token()
    except Exception as e:
        print(f"Error: {e}")
        return redirect("/")  

    credentials = dict_to_credentials(token_info)
    youtube = build('youtube', 'v3', credentials=credentials)
    all_songs = []

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId="LL",
        maxResults=50
    )

    while request:
        response = request.execute()
        items = response.get("items", [])
        for item in items:
            video_title = item["snippet"]["title"]
            channel_title = item["snippet"].get("videoOwnerChannelTitle", "Unknown Channel")
            all_songs.append(f"{video_title} - {channel_title}")
        request = youtube.playlistItems().list_next(request, response)

    # Save to Downloads folder
    csv_path = os.path.join(Path.home(), "Downloads", "songs.csv")
    df = pd.DataFrame(all_songs, columns=["column"])
    df.to_csv(csv_path, index=False)
    download_liked_videos(csv_path)

    return f"Download started for {len(all_songs)} liked songs. Check your Downloads/songs folder."


def create_youtube_oauth():
    return Flow.from_client_secrets_file(
        os.path.abspath("client_secrets.json"),
        scopes=['https://www.googleapis.com/auth/youtube.readonly'],
        redirect_uri=url_for('redirect_page', _external=True)
    )


def credentials_to_dict(creds):
    return {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }


def dict_to_credentials(data):
    return Credentials(
        token=data['token'],
        refresh_token=data.get('refresh_token'),
        token_uri=data['token_uri'],
        client_id=data['client_id'],
        client_secret=data['client_secret'],
        scopes=data['scopes']
    )


def get_token():
    token_info = session.get(TOKEN_INFO)
    if not token_info:
        raise Exception("No token found in session.")
    credentials = dict_to_credentials(token_info)
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        session[TOKEN_INFO] = credentials_to_dict(credentials)
    return session[TOKEN_INFO]


def scrape_vid_id(query):
    print(f"🔍 Searching YouTube for: {query}")
    search = VideosSearch(query, limit=1)
    result = search.result()["result"]
    if result:
        return result[0]["id"]
    return None


def download_from_ids(video_ids):
    SAVE_PATH = os.path.join(Path.home(), "Downloads", "songs")
    os.makedirs(SAVE_PATH, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': 'C:/ffmpeg/bin',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_ids)


def download_from_titles(titles):
    ids = []
    for title in titles:
        vid_id = scrape_vid_id(title)
        if vid_id:
            ids.append(f"https://www.youtube.com/watch?v={vid_id}")
    print("🎶 Downloading MP3s...")
    download_from_ids(ids)


def download_liked_videos(csv_path):
    if not os.path.exists(csv_path):
        print("songs.csv not found.")
        return
    df = pd.read_csv(csv_path)
    titles = df["column"].tolist()
    if not titles:
        print("No songs found in songs.csv.")
        return
    download_from_titles(titles)


if __name__ == "__main__":
    app.run(debug=True)