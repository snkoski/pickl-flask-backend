# Script to add all teams to database
import requests

teams = [
    {
        'city': 'Arizona',
        'name': 'Diamondbacks',
        'abbreviation': 'ARI',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/109.jpg'
    },
    {
        'city': 'Baltimore',
        'name': 'Orioles',
        'abbreviation': 'BAL',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/110.jpg'
    },
    {
        'city': 'Atlanta',
        'name': 'Braves',
        'abbreviation': 'ATL',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/144.jpg'
    },
    {
        'city': 'Boston',
        'name': 'Red Sox',
        'abbreviation': 'BOS',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/111.jpg'
    },
    {
        'city': 'Chicago',
        'name': 'Cubs',
        'abbreviation': 'CHC',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/112.jpg'
    },
    {
        'city': 'Chicago',
        'name': 'White Sox',
        'abbreviation': 'CWS',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/145.jpg'
    },
    {
        'city': 'Cincinnati',
        'name': 'Reds',
        'abbreviation': 'CIN',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/113.jpg'
    },
    {
        'city': 'Cleveland',
        'name': 'Indians',
        'abbreviation': 'CLE',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/114.jpg'
    },
    {
        'city': 'Colorado',
        'name': 'Rockies',
        'abbreviation': 'COL',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/115.jpg'
    },
    {
        'city': 'Detroit',
        'name': 'Tigers',
        'abbreviation': 'DET',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/116.jpg'
    },
    {
        'city': 'Houston',
        'name': 'Astros',
        'abbreviation': 'HOU',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/117.jpg'
    },
    {
        'city': 'Kansas City',
        'name': 'Royals',
        'abbreviation': 'KC',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/118.jpg'
    },
    {
        'city': 'Los Angeles',
        'name': 'Angels',
        'abbreviation': 'LAA',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/108.jpg'
    },
    {
        'city': 'Los Angeles',
        'name': 'Dodgers',
        'abbreviation': 'LAD',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/119.jpg'
    },
    {
        'city': 'Miami',
        'name': 'Marlins',
        'abbreviation': 'MIA',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/146.jpg'
    },
    {
        'city': 'Milwaukee',
        'name': 'Brewers',
        'abbreviation': 'MIL',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/158.jpg'
    },
    {
        'city': 'Minnesota',
        'name': 'Twins',
        'abbreviation': 'MIN',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/142.jpg'
    },
    {
        'city': 'New York',
        'name': 'Mets',
        'abbreviation': 'NYM',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/121.jpg'
    },
    {
        'city': 'New York',
        'name': 'Yankees',
        'abbreviation': 'NYY',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/147.jpg'
    },
    {
        'city': 'Oakland',
        'name': 'Athletics',
        'abbreviation': 'OAK',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/133.jpg'
    },
    {
        'city': 'Pittsburgh',
        'name': 'Pirates',
        'abbreviation': 'PIT',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/134.jpg'
    },
    {
        'city': 'Philadelphia',
        'name': 'Phillies',
        'abbreviation': 'PHI',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/143.jpg'
    },
    {
        'city': 'San Diego',
        'name': 'Padres',
        'abbreviation': 'SD',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/135.jpg'
    },
    {
        'city': 'San Francisco',
        'name': 'Giants',
        'abbreviation': 'SF',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/137.jpg'
    },
    {
        'city': 'Seattle',
        'name': 'Mariners',
        'abbreviation': 'SEA',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/136.jpg'
    },
    {
        'city': 'St. Louis',
        'name': 'Cardinals',
        'abbreviation': 'STL',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/138.jpg'
    },
    {
        'city': 'Tampa Bay',
        'name': 'Rays',
        'abbreviation': 'TB',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/139.jpg'
    },
    {
        'city': 'Texas',
        'name': 'Rangers',
        'abbreviation': 'TEX',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/140.jpg'
    },
    {
        'city': 'Toronto',
        'name': 'Blue Jays',
        'abbreviation': 'TOR',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/141.jpg'
    },
    {
        'city': 'Washington',
        'name': 'Nationals',
        'abbreviation': 'WAS',
        'logo': 'https://www.mlbstatic.com/mlb.com/images/share/120.jpg'
    },
]

for team in teams:
    r = requests.post('http://localhost:5000/api/teams', json=team)
