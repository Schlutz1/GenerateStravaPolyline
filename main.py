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
print(access_token)

# athlete_id = stravaHandler.getAthleteId(access_token=access_token)
# print(athlete_id)

z = stravaHandler.listActivities(access_token)
print(z)
# stravaHandler.getActivityById(
#     access_token=access_token
#     , activity_id=5767330559
# )