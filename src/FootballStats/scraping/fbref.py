import datetime
from FootballStats.scraping.common import *
from FootballStats.objects.constants import CURRENT_FBREF_SEASON

def extract_table_data(table):

    rows = table.find("tbody").find_all("tr", attrs={"class":False})
    all_data = []
    for row in rows:
        row_data = {"link":row.find("a")["href"]}
        for col in row.find_all(recursive=False, attrs={"data-stat":True}):
            row_data[col["data-stat"]] = col.text.strip()
        all_data.append(row_data)
    return all_data

def get_player_match_logs(player_id, player_name, season):

    url = "https://fbref.com/en/players/{id}/matchlogs/{season}/summary/{name}-Match-Logs".format(id=player_id, season=season, name=player_name.replace(" ", "-"))
    soup = get_soup(url)
    table = soup.find("table", id="matchlogs_all")
    #print(table)
    return extract_table_data(table)

def get_team_season_soup(team_id, team_name, season):

    if season == CURRENT_FBREF_SEASON:
        url = "https://fbref.com/en/squads/{id}/{name}-Stats".format(id=team_id, name=team_name.replace(" ", "-"))
    else:
        url = "https://fbref.com/en/squads/{id}/{season}/{name}-Stats".format(id=team_id, season=season, name=team_name.replace(" ", "-"))
    return get_soup(url)

def get_team_season_games(team_id, team_name, season):

    soup = get_team_season_soup(team_id, team_name, season)
    table = soup.find("table", id="matchlogs_for")
    return extract_table_data(table)

def date_season(date):

    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    if dt.month > 7:
        return str(dt.year) + "-" + str(dt.year + 1)
    else:
        return str(dt.year - 1) + "-" + str(dt.year)

def get_game_url(player={"id":None, "name":None}, home_team={"id":None, "name":None}, away_team={"id":None, "name":None}, date=None, season=None):

    if date == None and season == None:
        raise Exception

    if season == None:
            season = date_season(date)

    if date != None and None not in player.values():
        season_logs = get_player_match_logs(player["id"], player["name"], season)
        for game in season_logs:
            if game["date"] == date:
                return game["link"]
    
    elif None not in player.values() and None not in home_team.values():
        season_logs = get_player_match_logs(player["id"], player["name"], season)
        for game in season_logs:
            if game["venue"] == "Away" and game["opponent"] == home_team["name"]:
                return game["link"]

    elif None not in player.values() and None not in away_team.values():
        season_logs = get_player_match_logs(player["id"], player["name"], season)
        print(season_logs)
        for game in season_logs:
            if game["venue"] == "Home" and game["opponent"] == home_team["name"]:
                return game["link"]

    elif date != None and (None not in home_team.values() or None not in away_team.values()):
        if None not in home_team.values():
            team_season_games = get_team_season_games(home_team["id"], home_team["name"], season)
        elif None not in away_team.values():
            team_season_games = get_team_season_games(away_team["id"], away_team["name"], season)
        for game in team_season_games:
            if game["date"] == date:
                return game["link"]

    elif None not in home_team.values() and None not in away_team.values():
        team_season_games = get_team_season_games(home_team["id"], home_team["name"], season)
        for game in team_season_games:
            if game["venue"] == "Home" and game["opponent"] == away_team["name"]:
                return game["link"]
    
    else:
        raise Exception


def get_player_game_stats(player, opponent={"id":None, "name":None}, home=None, date=None, season=None, stats_type="summary"):

    if home == True:
        url = get_game_url(player=player, away_team=opponent, date=date, season=season)
    elif home == False:
        url = get_game_url(player=player, home_team=opponent, date=date, season=season)
    print(url)
    game_soup = get_soup(url)
    table = game_soup.find("table", id="stats_add600ae_"+stats_type)
    game_players = extract_table_data(table)
    for gp in game_players:
        if gp["player"] == player["name"]:
            return gp
