#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module implements authentication flow for Strava app
    Documentation on Strava auth flow can be found here:
    * https://developers.strava.com/docs/getting-started 
    * https://developers.strava.com/docs/authentication/
    
    App assumes the existence of some:
    * client_id
    * client_secret
    * refresh_token 
"""

# standard libs
import requests as r
import pandas as pd
import json
import time
import os

# handler authorisation flow
class AuthHandler():

    def __init__(self):
        
        self._id = "authentication.py"

        # definitions for strava app
        self.refresh_uri = "https://www.strava.com/api/v3/oauth/token"

        # could potentially do this via dependency injection if multiple users for the app
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.athlete_id = os.getenv("STRAVA_ATHLETE_ID")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")

    def refreshAccessToken(self, conn):
        ''' refreshes expired access token for user account '''
        
        # generate payload for refresh
        payload = {
            'client_id': self.client_id
            , 'client_secret': self.client_secret
            , 'refresh_token': self.refresh_token
            , 'grant_type': 'refresh_token'
        }
        
        # post top refresh uri
        resp = r.post(self.refresh_uri, data=payload)

        if resp.status_code != 200:
            print("{_id}: refreshAccessToken post returnd status_code != 200")
        
        # conver to table, append athelete ID, and write to local database
        resp_json = json.loads(resp.text)
        resp_json['athlete_id'] = self.athlete_id

        access_token_table = pd.DataFrame([resp_json])
        access_token_table.to_sql(
            'access_tokens'
            , conn
            , if_exists = 'replace' # can lazily replace here, as only one athlete
        )
        
        # return access token
        return resp_json['access_token']

    def getAccessToken(self, conn):
        ''' gets access token, optionally refreshes as required '''

        access_token_lookup = pd.read_sql(
            'SELECT access_token, expires_at FROM access_tokens WHERE athlete_id = 123456;'
            , conn
        )

        current_epoch_time = int(time.time())
        if current_epoch_time >= access_token_lookup['expires_at'][0]:
           # if cached token is expired generate new token

           access_token = refreshAccessToken(conn)
        else:
            access_token = access_token_lookup['access_token'][0]

        return access_token