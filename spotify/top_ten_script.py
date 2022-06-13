import sqlalchemy
import sqlite3
import pymysql
import pandas as pd
from . import MYSQL_CREDS

def get_user_top_ten(user_app):
    # print('USER = ', user_app)
    # print('DB HOST = ', MYSQL_CREDS.db_host)
    # print('DB USER = ', MYSQL_CREDS.db_user)
    # print('DB PASSWORD = ', MYSQL_CREDS.db_password)
    # print('DB NAME = ', MYSQL_CREDS.db_name)

    engine = "mysql+pymysql://{0}:{1}@{2}/{3}".format(MYSQL_CREDS.db_user, MYSQL_CREDS.db_password, MYSQL_CREDS.db_host, MYSQL_CREDS.db_name)

    user_selection = pd.read_sql_query("SELECT*FROM frontend_plays WHERE username = '{0}'".format(user_app), engine)
    song_ranking = user_selection.value_counts(subset = ['song_title', 'artist_name', 'album_name'])
    
    ranking_dict = song_ranking.to_dict()
    ranking_dict = dict(sorted(ranking_dict.items(), key = lambda x : -x[1]) [:10])

    #print(ranking_dict)

    key_list = []
    for key in ranking_dict.keys():
        key_list.append(key)

    list_of_songs, list_of_artists, list_of_albums = split_keys(key_list)
    #print(list_of_songs, list_of_artists, list_of_albums)

    list_of_values = get_list_of_plays(ranking_dict)
    #print(list_of_values)

    user_top_ten_dict = {
    "song_name" : list_of_songs,
    "artist_name" : list_of_artists,
    "album_name" : list_of_albums,
    "num_plays" : list_of_values
    }

    user_top_ten_dict_df = pd.DataFrame(user_top_ten_dict)
    user_top_ten_dict_df.index += 1
    json = user_top_ten_dict_df.to_json()
    # html = user_top_ten_dict_df.to_html()
    return json

def split_keys(lst):
    lst1 = []
    lst2 = []
    lst3 = []
    for x, y, z in lst:
        lst1.append(x)
        lst2.append(y)
        lst3.append(z)
    return (lst1, lst2, lst3)

def get_list_of_plays(ranking_dict):
    values_list = []
    for value in ranking_dict.values():
        values_list.append(value)
    return values_list