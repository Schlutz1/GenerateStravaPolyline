
import os
import requests as r


# system globals
abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_path)
settings.getEnv()


class AuthHandler():
    '''
    Documentation on Strava auth flow can be found here:
    - https://developers.strava.com/docs/getting-started 
    - https://developers.strava.com/docs/authentication/
    
    App assumes the existence of some:
    - client_id
    - client_secret
    - refresh_token 
    '''

    def __init__(self):
        
        # definitions for strava app
        self.refresh_uri = "https://www.strava.com/api/v3/oauth/token"


if __name__ == "__main__" :

    access_token = "01c8ac9f50173cd1478441aaeb8ac44628c5a1c7"
    databaseHandler = DatabaseHandler()
    
    df_activities = databaseHandler.getStravaActivities(access_token)
    print(df_activities.shape)
    print(df_activities)
    # df_activities.to_sql(
    #     'sandbox'
    #     , conn
    # )