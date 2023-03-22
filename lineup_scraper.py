import requests
from bs4 import BeautifulSoup

url = "https://rotogrinders.com/lineups/mlb"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

player_names = []

for player_list in soup.find_all("ul", class_="players unconfirmed"):
    for player in player_list.find_all("li"):
        player_name_element = player.find("a", class_="player-popup")
        if player_name_element is not None:
            player_names.append(player_name_element.get("title"))

print(player_names)