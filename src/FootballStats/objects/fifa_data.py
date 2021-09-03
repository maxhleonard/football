
FIFA_BASE_URL = "https://www.fifaindex.com"

class PlayerVersionStats():

    def __init__(self, player, fifa_year, fifa_version, stats):

        self.player = player
        self.year = year
        


class FifaPlayerRow():

    def __init__(self, row, fifa_year, fifa_version):

        self.fifa_year = fifa_year
        self.fifa_version = fifa_version
        self.player_id = int(row["data-playerid"])
        self.nationality = row.find("td", attrs={"data-title":"Nationality"}).find("a")["title"]
        ovr_pot = row.find("td", attrs={"data-title":"OVR / POT"}).find_all("span")
        self.overall_rating = int(ovr_pot[0].text)
        self.potential_rating = int(ovr_pot[1].text)
        name_block = row.find("td", attrs={"data-title":"Name"}).find("a")
        self.name = name_block.text
        self.link = FIFA_BASE_URL + name_block["href"]
        self.prefered_positions = [pos["title"] for pos in row.find("td", attrs={"data-title":"Preferred Positions"}).find_all("a")]

