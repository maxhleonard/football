from FootballStats.objects.fifa_data import *
from FootballStats.scraping import fifa_index
from FootballStats.objects.constants import *
from FootballStats.scraping.common import get_soup
from FootballStats.objects.common import *
import json
import datetime

def choose_fifa_id(ids, name):

    if len(ids) == 1:
        return ids[0]
    for ind, potential_id in enumerate(ids):
        url = fifa_index.get_fifa_url(potential_id, name, CURRENT_FIFA_YEAR, None)
        stats = fifa_index.get_player_stats(url)

def choose_fbref_id(ids, name):

    if len(ids) == 1:
        return ids[0]


class Footballer():

    def __init__(self, name, fifa_data_path=None, fbref_data_path=None):

        self.name = name
        
        #match up with Fifa Stats ID
        if fifa_data_path == None:
            fifa_ids = get_data_file("fifa_player_ids.json")
        else:
            with open(fifa_data_path) as f:
                fifa_ids = json.load(f)
                f.close()
        try:
            player_ids = fifa_ids[name]
            self.fifa_id = choose_fifa_id(player_ids, name)
            self.fifa_name = name
        except:
            first_name = name.split()[0]
            last_name = name.split()[1:]
            if first_name in fifa_ids.keys():
                player_ids = fifa_ids[first_name]
                self.fifa_id = choose_fifa_id(player_ids, first_name)
                self.fifa_name = first_name
            elif last_name in fifa_ids.keys():
                player_ids = fifa_ids[last_name]
                self.fifa_id = choose_fifa_id(player_ids, last_name)
                self.fifa_name = last_name
        
        #match up with FBREF ID
        if fbref_data_path == None:
            fbref_ids = get_data_file("fbref_player_ids.json")
        else:
            with open(fbref_data_path) as f:
                fbref_ids = json.load(f)
                f.close()
        try:
            player_ids = fbref_ids[name]
            self.fbref_id = choose_fbref_id(player_ids, name)
            self.fbref_name = name
        except:
            first_name = name.split()[0]
            last_name = name.split()[1:]
            if first_name in fbref_ids.keys():
                player_ids = fbref_ids[first_name]
                self.fbref_id = choose_fbref_id(player_ids, first_name)
                self.fbref_name = first_name
            elif last_name in fbref_ids.keys():
                player_ids = fbref_ids[last_name]
                self.fbref_id = choose_fbref_id(player_ids, last_name)
                self.fbref_name = last_name

    def get_all_fifa_versions(self):

        all_versions = []
        player_url = fifa_index.get_fifa_url(self.fifa_id, self.fifa_name, None, None)
        player_soup = get_soup(player_url)
        version_rows = fifa_index.get_page_versions(player_soup)
        fifa_year = None
        for row in version_rows:
            if "Changelog" in row.text:
                continue
            elif row["class"] == ["dropdown-header"]:
                fifa_year = fifa_index.format_fifa_year(row.text)
            elif row["class"] == ["dropdown-item"]:
                version_date = fifa_index.parse_date(row.text.split("-")[1].strip())
                fifa_version = fifa_index.get_fifa_version(fifa_year, version_date)
                all_versions.append((fifa_year, fifa_version))

        return all_versions
                

    def get_fifa_stats(self, fifa_year, target_date=None, fifa_version=None):

        if fifa_version == None:
            fifa_version = fifa_index.get_fifa_version(fifa_year, target_date)
        url = fifa_index.get_fifa_url(self.fifa_id, self.fifa_name, fifa_year, fifa_version)
        print(url)
        stats = fifa_index.get_player_stats(url)
        print(stats)
        fifa_meta = FifaMeta(self.fifa_id, self.fifa_name, fifa_year, fifa_version)
        return PlayerVersionStats(fifa_meta, stats)

    def get_all_fifa_stats(self):

        versions = self.get_all_fifa_versions()
        return [self.get_fifa_stats(ver[0], fifa_version=ver[1]) for ver in versions]
