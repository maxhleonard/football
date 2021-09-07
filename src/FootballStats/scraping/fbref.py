import datetime

def get_player_match_logs(player_id, player_name, season):

    if season != None:
        url = "https://fbref.com/en/players/{id}/matchlogs/{season}/summary/{name}-Match-Logs".format(id=player_id, season=season, name=player_name)
    elif 

def date_season(date):

    dt = datetime.datetime.strptime(date, "%Y-%m-%d")
    if dt.month > 7:
        return str(dt.year) + "-" + str(dt.year + 1)
    else:
        return str(dt.year - 1) + "-" + str(dt.year)

def get_game_url(player_id=None, player_name=None, home_team=None, away_team=None, date=None, season=None):

    if date != None:
        if player_id != None and player_name != None:
            if season == None:
                season = date_season(date)
            season_logs_soup = get_player_match_logs(player_id, player_name, season)
            

def get_player_game_stats(player_id, player_name, ):

   