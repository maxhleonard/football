from FootballStats.scraping.common import *
from FootballStats.objects.common import get_data_file
import datetime

FIFA_BASE_URL = "https://www.fifaindex.com"

def get_page_years(soup):

    navbar = soup.find_all("nav")[1]
    return navbar.find_all("li")[1].find("div", class_="dropdown-menu").find_all(recursive=False)

def get_page_versions(soup):

    navbar = soup.find_all("nav")[1]
    return navbar.find_all("li")[2].find("div", class_="dropdown-menu").find_all(recursive=False)

def get_players_nav(soup):

    return soup.find("div", id="bigpagination").find("nav").find_all("li")
    
def get_page_players(soup):

    return soup.find_all(attrs={"data-playerid":True})

def parse_date(text):

    if "." in text:
        try:
            date = datetime.datetime.strptime(text, "%b. %d, %Y")
        except:
            comps = text.replace(".", "").replace(",","").split()
            comps[0] = comps[0][:3]
            date_text = " ".join(comps)
            date = datetime.datetime.strptime(date_text, "%b %d %Y")
    else:
        date = datetime.datetime.strptime(text, "%B %d, %Y")
    return date

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

def get_fifa_url(fifa_id, fifa_name, fifa_year, fifa_version):

        if fifa_year == None or fifa_version == None:
            return FIFA_BASE_URL + "/player/{id}/{name}/".format(id=fifa_id, name=fifa_name.replace(" ", "-").lower())
        else:
            return FIFA_BASE_URL + "/player/{id}/{name}/{year}_{version}".format(id=fifa_id, name=fifa_name.replace(" ", "-").lower(), year=fifa_year.replace(" ", "").lower(), version=fifa_version)


def format_fifa_year(year):

    parts = year.split()
    if len(parts[1]) == 1:
        parts[1] = "0" + parts[1]
    return " ".join(parts)

def get_version_players(url):

    page = 1
    players = []
    version_soup = get_soup(url)
    page_navs = get_players_nav(version_soup)
    last_page_url = url + page_navs[-1].find("a")["href"]
    while True:
        page_url = url + "?page=" + str(page)
        page_soup = get_soup(page_url)
        players += get_page_players(page_soup)
        if page_url == last_page_url:
            break
        page += 1
    return players

def get_all_fifa_versions():

    versions = {}
    home_soup = get_soup(FIFA_BASE_URL + "/players/")
    all_years = get_page_years(home_soup)
    for year in all_years:
        fifa_year = year.text
        versions[fifa_year] = []
        year_link = FIFA_BASE_URL + year["href"]
        year_soup = get_soup(year_link)
        year_versions = get_page_versions(year_soup)
        for version in year_versions:
            version_date = parse_date(version.text)
            version_link = FIFA_BASE_URL + version["href"]
            versions[fifa_year].append({"date":version_date.strftime("%Y-%m-%d"), "link":version_link})
    return versions

def parse_span_data_row(row):

    all_text = row.text
    spans = row.find_all("span")
    value_text = " ".join(x.text.strip() for x in row.find_all(recursive=False))
    data_name = row.text.replace(value_text, "").strip()
    data_value = spans[-1].text.strip()
    return data_name, data_value

def parse_bio_card(card):

    name = None
    overall_rating = None
    potential_rating = None
    height = None
    weight = None
    preferred_foot = None
    birth_date = None
    age = None
    preferred_positions = []
    player_work_rate = None
    weak_foot = None
    skill_moves = None
    value = None
    wage = None

    if card != None:
        header = card.find(class_="card-header")
        spans = header.find("span").find_all("span")
        overall = spans[0]
        potential = spans[1]
        name = header.text.replace(overall.text, "").replace(potential.text, "").strip()
        overall_rating = int(overall.text)
        potential_rating = int(potential.text)

        info_lines = card.find(class_="card-body").find_all("p")
        for line in info_lines:
            if "Height" in line.text:
                height = int(line.find(class_="data-units-metric").text.replace(" cm", ""))
            elif "Weight" in line.text:
                weight = int(line.find(class_="data-units-metric").text.replace(" kg", ""))
            elif "Preferred Foot" in line.text:
                preferred_foot = parse_span_data_row(line)[1]
            elif "Birth Date" in line.text:
                birth_date = parse_date(parse_span_data_row(line)[1]).strftime("%Y-%m-%d")
            elif "Age" in line.text:
                age = int(parse_span_data_row(line)[1])
            elif "Preferred Positions" in line.text:
                for pos in line.find_all("a"):
                    preferred_positions.append(pos["title"])
            elif "Player Work Rate" in line.text:
                player_work_rate = parse_span_data_row(line)[1]
            elif "Weak Foot" in line.text:
                weak_foot = len(line.find_all("i", class_="fas"))
            elif "Skill Moves" in line.text:
                skill_moves = len(line.find_all("i", class_="fas"))
            elif "Value" in line.text and "data-currency-euro" in line["class"]:
                value = float(parse_span_data_row(line)[1].replace("???", "").replace(".",""))
            elif "Wage" in line.text and "data-currency-euro" in line["class"]:
                wage = float(parse_span_data_row(line)[1].replace("???", "").replace(".", ""))

    return {"name":name, "overall_rating":overall_rating, "potential_rating":potential_rating, "height":height, "weight":weight, "preferred_foot":preferred_foot, "birth_date":birth_date, "age":age, "preferred_positions":preferred_positions, "player_work_rate":player_work_rate, "weak_foot":weak_foot, "skill_moves":skill_moves, "value":value, "wage":wage}


def parse_club_card(card):

    club_name = None
    position = None
    kit_number = None
    joined_club = None
    contract_ends = None

    if card != None:
        club_name = card.find(class_="card-header").text.strip()
        info_lines = card.find(class_="card-body").find_all("p")
        for line in info_lines:
            if "Position" in line.text:
                position = line.find("span").text
            elif "Kit Number" in line.text:
                kit_number = line.find("span").text
            elif "Joined Club" in line.text:
                joined_club = parse_date(line.find("span").text).strftime("%Y-%m-%d")
            elif "Contract Length" in line.text:
                contract_ends = int(line.find("span").text)
    
    return {"club_name":club_name, "position":position, "kit_number":kit_number, "joined_club":joined_club, "contract_ends":contract_ends}
            

def parse_international_card(card):

    country = None
    position = None
    kit_number = None

    if card != None:
        country = card.find(class_="card-header").text.strip()
        info_lines = card.find(class_="card-body").find_all("p")
        for line in info_lines:
            if "Position" in line.text:
                position = line.find("span").text
            elif "Kit Number" in line.text:
                kit_number = line.find("span").text
    
    return {"country":country, "position":position, "kit_number":kit_number}


def parse_attributes_card(card):

    attributes = []
    if card != None:
        for attribute in card.find(class_="card-body").find_all("p"):
            attributes.append(attribute.text.replace("(CPU AI Only)", "").strip())
    return attributes

def parse_stats_card(card):

    stats = {}
    stat_category = card.find(class_="card-header").text.strip()
    stat_category = stat_category.lower().replace(" ", "_")
    for stat in card.find(class_="card-body").find_all("p"):
        stat_name, stat_num = parse_span_data_row(stat)
        stat_name = stat_name.lower().replace(" ", "_").replace(".", "")
        stats[stat_name] = int(stat_num)
    return stat_category, stats

def get_player_stats(url):

    player_soup = get_soup(url)
    stats = {}
    all_cards = player_soup.find_all(class_="card")
    # sort data cards
    stats_cards = []
    club_card = None
    international_card = None
    bio_card = None
    traits_card = None
    specialties_card = None
    for card in all_cards:
        if "team" in card.parent["class"]:
            if "Contract" in card.text:
                club_card = card
            else:
                international_card = card
        elif "item" in card.parent["class"]:
            if "Traits" in card.find(class_="card-header").text:
                traits_card = card
            elif "Specialities" in card.find(class_="card-header").text:
                specialties_card = card
            else:
                stats_cards.append(card)
        else:
            bio_card = card
    
    stats["bio"] = parse_bio_card(bio_card)
    stats["club_info"] = parse_club_card(club_card)
    stats["international_info"] = parse_international_card(international_card)
    stats["traits"] = parse_attributes_card(traits_card)
    stats["specialties"] = parse_attributes_card(specialties_card)
    for stat in stats_cards:
        category, stats_data = parse_stats_card(stat)
        stats[category] = stats_data
    
    return stats