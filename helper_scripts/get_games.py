# Script to get all regular season games from My Sports Feed API and post to database
import os
from ohmysportsfeedspy import MySportsFeeds
from not_yours import MSF_API_KEY, MSF_PASSWORD
import requests

msf = MySportsFeeds(version="1.2")
msf.authenticate(MSF_API_KEY, MSF_PASSWORD)

result = msf.msf_get_data(league='mlb',season='2019-regular',feed='full_game_schedule',format='json')

for gameentry in result['fullgameschedule']['gameentry']:
    r = requests.post('http://localhost:5000/api/games', json=gameentry)
