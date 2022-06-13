import sqlalchemy
import sqlite3
import pymysql
import datetime
import requests
import pandas as pd
import datetime
from . import MYSQL_CREDS

def test(user_app, token):
    # print('USER = ', user_app)
    # print('TOKEN = ', token)
    # print('DB HOST = ', MYSQL_CREDS.db_host)
    # print('DB USER = ', MYSQL_CREDS.db_user)
    # print('DB PASSWORD = ', MYSQL_CREDS.db_password)
    # print('DB NAME = ', MYSQL_CREDS.db_name)

    engine = "mysql+pymysql://{0}:{1}@{2}/{3}".format(MYSQL_CREDS.db_user, MYSQL_CREDS.db_password, MYSQL_CREDS.db_host, MYSQL_CREDS.db_name)

    data_from_database = pd.read_sql('frontend_plays', engine)

    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token =  token)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days = 1)
    yesterday_unix_stamp = int(yesterday.timestamp()) * 1000

    rqst = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time = yesterday_unix_stamp), headers = headers)

    downloaded_data = rqst.json()
    #print(downloaded_data)
    song_names = []
    artist_names = []
    album_names = []
    played_at_list = []
    timestamps = []

    for song in downloaded_data['items']:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        album_names.append(song["track"]["album"]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        # Llamar a la función de Karen
        "username" : user_app,
        "song_title" : song_names,
        "artist_name" : artist_names,
        "album_name" : album_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    downloaded_data_df = pd.DataFrame(song_dict)
    #print(song_dict['username'])

    if check_for_valid_data(downloaded_data_df):
        pre_new_songs = pd.concat([data_from_database, downloaded_data_df])
        new_songs = pd.concat([data_from_database, pre_new_songs]).drop_duplicates(keep = False)
        # print(new_songs)
        new_songs_insertion = new_songs.to_sql('frontend_plays', engine, if_exists = 'append', index = False)


def check_for_valid_data(df : pd.DataFrame):
    if df.empty:
        # print("No songs were downloaded. Finishing execution.")
        return False
    return True