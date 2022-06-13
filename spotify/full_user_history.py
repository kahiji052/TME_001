import sqlalchemy
import sqlite3
import pymysql
import pandas as pd
from . import MYSQL_CREDS

def get_full_user_history(user_app):
    engine = "mysql+pymysql://{0}:{1}@{2}/{3}".format(MYSQL_CREDS.db_user, MYSQL_CREDS.db_password, MYSQL_CREDS.db_host, MYSQL_CREDS.db_name)

    user_selection = pd.read_sql_query("SELECT*FROM frontend_plays WHERE username = '{0}'".format(user_app), engine)

    full_user_history = user_selection.sort_values(by = 'timestamp', ascending = False)
    json = full_user_history.to_json()
    #html = full_user_history.to_html()

    return json