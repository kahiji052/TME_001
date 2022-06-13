import sqlalchemy
import sqlite3
import pymysql
import pandas as pd
from . import MYSQL_CREDS

def get_user_top_artists(user_app):
    engine = "mysql+pymysql://{0}:{1}@{2}/{3}".format(MYSQL_CREDS.db_user, MYSQL_CREDS.db_password, MYSQL_CREDS.db_host, MYSQL_CREDS.db_name)

    user_selection = pd.read_sql_query("SELECT*FROM frontend_plays WHERE username = '{0}'".format(user_app), engine)

    artist_ranking = user_selection.value_counts(subset = ['artist_name'])
    #print(artist_ranking)

    artist_ranking = artist_ranking.to_dict()
    artist_ranking = dict(sorted(artist_ranking.items(), key = lambda x : -x[1]) [:10])
    #print(artist_ranking)

    key_list = []
    for key in artist_ranking.keys():
        key_list.append(key)

    list_of_top_artists = []
    for x, in key_list:
        list_of_top_artists.append(x)
    #print(list_of_top_artists)

    top_artists_dict = {
        "top_artists" : list_of_top_artists
    }

    top_artists_df = pd.DataFrame(top_artists_dict)
    top_artists_df.index += 1
    #print(top_artists_df)

    json = top_artists_df.to_json()
    return json
