import requests
from bs4 import BeautifulSoup
import json

url = "https://rotogrinders.com/lineups/mlb"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
players = []

for ul in soup.find_all('ul', {'class': 'players unconfirmed'}):
    for li in ul.find_all('li', {'class': 'player'}):
        name = li.find('a', {'class': 'player-popup'}).get('title')
        players.append(name)

# create a dictionary containing the player names
data = {'players': players}

# convert the dictionary to a JSON object
json_data = json.dumps(data)

# save the JSON object to a file
with open('players.json', 'w') as f:
    f.write(json_data)