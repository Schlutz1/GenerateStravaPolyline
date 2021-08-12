#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module interacts with strava API
    Documentation on Strava auth flow can be found here:
    * https://developers.strava.com/docs/getting-started 
    * https://developers.strava.com/docs/authentication/
    
    Handler assumes the existence of some:
    * client_id
    * client_secret
    * refresh_token
    Which are created using the above links 
"""

# standard libs
import requests as r
import pandas as pd
import json
import time
import os


# handles interactions with Strava API
class StravaHandler():

    def __init__(self):
        
        self._id = "strava.StravaHandler"

        # definitions for strava app
        self.refresh_uri = "https://www.strava.com/api/v3/oauth/token"
        self.athlete_uri = "https://www.strava.com/api/v3/athlete"
        self.activities_uri = "https://www.strava.com/api/v3/activities"

        # could potentially do this via dependency injection if multiple users for the app
        self.client_id = os.getenv("STRAVA_CLIENT_ID")
        self.athlete_id = os.getenv("STRAVA_ATHLETE_ID")
        self.refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")
        self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")

    def refreshAccessToken(self, conn) -> str:
        ''' refreshes expired access token for user account '''
        print(f"{self._id}: refreshing access token")
        
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
            print(f"{self._id}: refreshAccessToken post returned status_code != 200")
        
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

    def getAccessToken(self, conn) -> str:
        ''' gets access token, optionally refreshes as required '''

        access_token_lookup = pd.read_sql(
            'SELECT access_token, expires_at FROM access_tokens WHERE athlete_id = 123456;'
            , conn
        )

        current_epoch_time = int(time.time())
        if current_epoch_time >= access_token_lookup['expires_at'][0] :
           # if cached token is expired generate new token
            print(f"{self._id}: refreshing access token")
            access_token = self.refreshAccessToken(conn)
        else:
            print(f"{self._id}: loading cached access token")
            access_token = access_token_lookup['access_token'][0]

        return access_token

    def _getStravaEndpoint(self, uri, headers = None, payload = None):
        ''' Private fn, gets data from Strava API'''
        
        # make get request
        resp = r.get(
            uri
            , headers=headers
            , data=payload
        )

        if resp.status_code != 200:
            print(f"{self._id}: GET {uri} returned status_code != 200")

        return json.loads(resp.text)

    def getAthleteId(self, access_token) -> str:
        ''' use to get athlete Id from Strava API '''

        headers = {'Authorization': f'Bearer {access_token}'}
        athlete_profile = self._getStravaEndpoint(
            self.athlete_uri
            , headers = headers
        )

        return athlete_profile['id']

    def listActivities(self, access_token):
        ''' Returns the activities of an athlete for a specific athelete ID '''
        print(f"{self._id}: extracting all athlete activities")        

        headers = {'Authorization': f'Bearer {access_token}'}
        page = 1
        per_page = 50
        all_activities_list = []

        # paginate over pages until all activities extracted
        while True:
            payload = {
                'page': page
                , 'per_page': per_page
            }

            activities_list = self._getStravaEndpoint(
                uri=self.athlete_uri + '/activities'
                , headers=headers
                , payload=payload
            )

            all_activities_list += activities_list
            # print(len(all_activities_list))

            if len(activities_list) == 0:
                break
            else:
                page += 1
        
        n_activities = len(all_activities_list)
        print(f"{self._id}: returning {n_activities} activities")    
        return all_activities_list

    def getActivityById(self, access_token, activity_id):
        ''' Returns the given activity that is owned by the authenticated athlete for a specific activity ID'''

        headers = {'Authorization': f'Bearer {access_token}'}

        activity = self._getStravaEndpoint(
            uri=self.activities_uri + f'/{activity_id}'
            , headers=headers
        )
        return activity