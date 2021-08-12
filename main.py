import requests as r
import pprint as pp
import pandas as pd
import polyline
import sqlite3
import folium
import time
import sys
import os

# Local python scripts
from strava import StravaHandler
import settings


# system globals
abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_path)
settings.getEnv()


build_path = os.path.join(abs_path, "build")

db_file = "local.db"
conn = sqlite3.connect(os.path.join(abs_path, db_file))


# strava interactions
stravaHandler = StravaHandler()
access_token = stravaHandler.getAccessToken(conn)
# print(access_token)

# athlete_id = stravaHandler.getAthleteId(access_token=access_token)
# print(athlete_id)

activities = stravaHandler.listActivities(access_token)
# pp.pprint(activities[0])

# generate data for graphing
polylines_list = [{
    'id': activity['id']
    , 'decoded_polyline': polyline.decode(activity['map']['summary_polyline'])
    , 'start_date_local': activity['start_date_local']
} for activity in activities]

df_polylines = pd.DataFrame(polylines_list)

# df_polylines.to_sql(
#     'polyline_cache'
#     , conn
#     , if_exists='replace'
# )


# generating map of runing using folium
m = folium.Map(
    location=[-33.88644, 151.13697]
    ,zoom_start=13
)

# iterate across dataframe and add each run as a layer
for i, row in df_polylines.iterrows():
    
    folium.PolyLine(
        row['decoded_polyline']
        , color='red'
        , weight=2.5
        , opacity=0.5
    ).add_to(m)

if not os.path.isdir(build_path):
    os.mkdir(build_path)

current_epoch_time = int(time.time())
m.save(os.path.join(build_path, f"{current_epoch_time}_running_heatmap.html"))