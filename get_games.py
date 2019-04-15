from ohmysportsfeedspy import MySportsFeeds
import requests

API_ENDPOINT = 'http://localhost:5000/api/games'

msf = MySportsFeeds(version="1.2")
msf.authenticate("9479b181-74e6-4368-bd43-27f11d", "BrandAntlers22")

output = msf.msf_get_data(league='mlb',season='2019-regular',feed='full_game_schedule',format='json')

print(len(output['fullgameschedule']['gameentry']))
# print(output['fullgameschedule']['gameentry'])

for index, day in enumerate(output['fullgameschedule']['gameentry']):
        r = requests.post('http://localhost:5000/api/games', json=day)