from .common import *
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

def get_version_players(url):

    page = 1
    players = []
    version_soup = get_soup(url)
    page_navs = get_players_nav(version_soup)
    last_page_url = url + page_navs[-1].find("a")["href"]
    print("LAST", last_page_url)
    while True:
        page_url = url + "?page=" + str(page)
        print(page_url)
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
                preferred_foot = line.find("span").text
            elif "Birth Date" in line.text:
                birth_date = parse_date(line.find("span").text).strftime("%Y-%m-%d")
            elif "Age" in line.text:
                age = int(line.find("span").text)
            elif "Preferred Positions" in line.text:
                for pos in line.find_all("a"):
                    preferred_positions.append(pos["title"])
            elif "Player Work Rate" in line.text:
                player_work_rate = line.find("span").text
            elif "Weak Foot" in line.text:
                weak_foot = len(line.find_all("i", class_="fas"))
            elif "Skill Moves" in line.text:
                skill_moves = len(line.find_all("i", class_="fas"))
            elif "Value" in line.text and "data-currency-euro" in line["class"]:
                value = float(line.find("span").text.replace("€", "").replace(".",""))
            elif "Wage" in line.text and "data-currency-euro" in line["class"]:
                wage = float(line.find("span").text.replace("€", "").replace(".", ""))

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
            attributes.append(attribute.text.replace("(CPU AI Only)", ""))
    return attributes

def parse_stats_card(card):

    stats = {}
    stat_category = card.find(class_="card-header").text.strip()
    for stat in card.find(class_="card-body").find_all("p"):
        stat_num = stat.find("span").text
        stat_name = stat.text.replace(stat_num, "").strip()
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