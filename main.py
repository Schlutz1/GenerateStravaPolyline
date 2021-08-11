import requests as r
import sqlite3
import os, sys

# Local python scripts
from strava import StravaHandler
import settings


# system globals
abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_path)
settings.getEnv()

db_file = "local.db"
conn = sqlite3.connect(os.path.join(abs_path, db_file))


# sandbox
stravaHandler = StravaHandler()
access_token = stravaHandler.getAccessToken(conn)

stravaHandler.listAthleteActivities(access_token)
