import bs4
import urllib3
from .scraping.common import *
from .scraping.fifa_index import *
from .objects.fifa_data import *

def all_fifa_player_ids():

    all_players = []
    all_versions = get_all_fifa_versions()
    for year, versions in all_versions.items():
        if year == "FIFA 22":
            continue
        version_players = get_version_players(versions[0]["link"])
        for player in version_players:
            player_row = FifaPlayerRow(player, year, versions[0]["date"])
            all_players.append((player_row.name, player_row.player_id))
    return all_players


def all_fbref_ids():

    team_ids = {}
    player_ids = {}

    country_clubs_soup = get_soup("https://fbref.com/en/squads/")
    countries = country_clubs_soup.find("table", id="countries").find("tbody").find_all("tr", attrs={"class":False})
    country_links = ["https://fbref.com" + c.find("a")["href"] for c in countries]
    for link in country_links:
        country_soup = get_soup(link)
        clubs = country_soup.find(id="clubs").find("tbody").find_all("tr", attrs={"class":False})
        print(link)
        for club in clubs:
            club_link = club.find("a")
            club_name = club_link.text.strip()
            club_id = club_link["href"].split("/")[2]
            if club_name in team_ids.keys():
                team_ids[club_name].append(club_id)
            else:
                team_ids[club_name] = [club_id]
    
    players_soup = get_soup("https://fbref.com/en/players/")
    letters_links = ["https://fbref.com" + x["href"] for x in players_soup.find("ul", class_="page_index").find_all("a")]
    for link in letters_links:
        letters_soup = get_soup(link)
        players = letters_soup.find("div", class_="section_content")
        for player in players.find_all("a"):
            player_id = player["href"].split("/")[2]
            player_name = player.text.strip()
            if player_name in player_ids.keys():
                player_ids[player_name].append(player_id)
            else:
                player_ids[player_name] = [player_id]
    return team_ids, player_ids