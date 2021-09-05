from FootballStats.objects.fifa_data import *
from FootballStats.scraping import fifa_index
from FootballStats.objects.constants import *
import pkg_resources
import json
import datetime

def get_fifa_url(fifa_id, fifa_name, fifa_year, fifa_version):

        if target_date == None:
            return FIFA_BASE_URL + "/player/{id}/{name}/".format(id=fifa_id, name=fifa_name)
        else:
            return FIFA_BASE_URL + "/players/{id}/{name}/{year}_{version}".format(id=fifa_id, name=fifa_name, year=fifa_year.replace(" ", "").lower(), version=fifa_version)

def choose_fifa_id(ids, name):

    if len(ids) == 1:
        return ids[0]
    for ind, potential_id in enumerate(ids):
        url = get_fifa_url(potential_id, name, CURRENT_FIFA_YEAR, None)
        stats = fifa_index.get_player_stats(url)


def get_data_file(filename):

    file_path = pkg_resources.resource_filename("FootballStats", "data/{filename}".format(filename=filename))
    with open(file_path) as f:
        data = json.load(f)
        f.close()
    return data

def get_fifa_version(fifa_year, target_date):

    fifa_versions = get_data_file("fifa_versions.json")
    if target_date in fifa_versions[fifa_year].keys():
        return fifa_versions[fifa_year][target_date]

    dates = [datetime.datetime.strptime(x, "%Y-%m-%d") for x in fifa_versions[fifa_year].keys()]
    if target_date == None:
        dates.sort()
        return fifa_versions[fifa_year][dates[-1].strftime("%Y-%m-%d")]
    dates = [(x, abs(target_date - x)) for x in dates]
    dates.sort(key=lambda x: x[1])
    return fifa_versions[fifa_year][dates[0][0].strftime("%Y-%m-%d")]


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
        player_url = get_fifa_url(self.fifa_id, self.fifa_name, None, None)
        player_soup = get_soup(player_url)
        version_rows = get_page_versions(player_soup)
        fifa_year = None
        for row in version_rows:
            if "Changelog" in row.text:
                continue
            elif row["class"] == "dropdown-header":
                fifa_year = row.text
            elif row["class"] == "dropdown-item":
                version_date = parse_date(row.text.split("-")[1].strip()).strftime("%Y-%m-%d")
                fifa_version = get_fifa_version(fifa_year, version_date)
                all_versions.append((fifa_year, fifa_version))
        return all_versions
                

    def get_fifa_stats(self, fifa_year, target_date=None):

        fifa_version = get_fifa_version(fifa_year, target_date)
        url = get_fifa_url(self.fifa_id, self.fifa_name, fifa_year, fifa_version)
        stats = fifa_index.get_player_stats(url)
        return PlayerVersionStats(fifa_year, fifa_version, stats)

