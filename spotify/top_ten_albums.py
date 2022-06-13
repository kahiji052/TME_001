import sqlalchemy
import sqlite3
import pymysql
import pandas as pd
from . import MYSQL_CREDS

def get_user_top_albums(user_app):
    engine = "mysql+pymysql://{0}:{1}@{2}/{3}".format(MYSQL_CREDS.db_user, MYSQL_CREDS.db_password, MYSQL_CREDS.db_host, MYSQL_CREDS.db_name)
    
    user_selection = pd.read_sql_query("SELECT*FROM frontend_plays WHERE username = '{0}'".format(user_app), engine)

    album_ranking = user_selection.value_counts(subset = ['album_name', 'artist_name'])
    #print(album_ranking)

    album_ranking = album_ranking.to_dict()
    album_ranking = dict(sorted(album_ranking.items(), key = lambda x : -x[1]) [:10])
    #print(album_ranking)

    key_list = []
    for key in album_ranking.keys():
        key_list.append(key)
    #print(key_list)

    list_of_top_albums = []
    list_of_artists = []
    for x, y in key_list:
        list_of_top_albums.append(x)
        list_of_artists.append(y)
    #print(list_of_top_albums)

    top_albums_dict = {
        "top_albums" : list_of_top_albums,
        "artist" : list_of_artists
    }

    top_albums_df = pd.DataFrame(top_albums_dict)
    top_albums_df.index += 1
    print(top_albums_df)

    json = top_albums_df.to_json()
    print(json)
    return (json)