
import requests as r
import os, sys

# Local python scripts
import settings


# system globals
abs_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_path)
settings.getEnv()

print(os.getenv("STRAVA_CLIENT_ID"))

