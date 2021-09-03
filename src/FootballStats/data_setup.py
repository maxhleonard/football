import bs4
import urllib3
from FootballStats.scraping.common import *
from FootballStats.scraping.fifa_index import *

def all_fifa_player_ids():

    all_players = {}
    soup = get_soup("https://www.fifaindex.com/players/")
    years = get_page_years(soup)
    for year in years:
        if year.text == "FIFA 22":
            continue
        link = FIFA_BASE_URL + year["href"]
        year_players = get_version_players(link)
        for player in year_players:
            player_link = player.find("td", attrs={"data-title":"Name"}).find("a")
            player_name = player_link.text.strip()
            player_id = player_link["href"].split("/")[2]
            try:
                all_players[player_name].append(player_id)
            except:
                all_players[player_name] = [player_id]
    return all_players

def all_fifa_version_dates():

    fifa_versions = {}
    soup = get_soup("https://www.fifaindex.com/players/")
    years = get_page_years(soup)
    for year in years:
        if year.text == "FIFA 22":
            continue
        fifa_versions[year.text] = {}
        year_link = FIFA_BASE_URL + year["href"]
        year_soup = get_soup(year_link)
        versions = get_page_versions(year_soup)
        for version in versions:
            version_date = parse_date(version.text)
            try:
                version_number = int(version["href"].split("/")[2].split("_")[1])
            except:
                version_number = None
            fifa_versions[year.text][version_date.strftime("%Y-%m-%d")] = version_number
    return fifa_versions

def all_fbref_team_ids():

    team_ids = {}

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
            club_id = club_link["href"].split("/")[3]
            if club_name in team_ids.keys():
                team_ids[club_name].append(club_id)
            else:
                team_ids[club_name] = [club_id]
    return team_ids

def all_fbref_player_ids():

    player_ids = {}
    players_soup = get_soup("https://fbref.com/en/players/")
    letters_links = ["https://fbref.com" + x["href"] for x in players_soup.find("ul", class_="page_index").find_all("a")]
    for link in letters_links:
        letters_soup = get_soup(link)
        players = letters_soup.find("div", class_="section_content")
        for player in players.find_all("a"):
            player_id = player["href"].split("/")[3]
            player_name = player.text.strip()
            if player_name in player_ids.keys():
                player_ids[player_name].append(player_id)
            else:
                player_ids[player_name] = [player_id]
    return player_ids