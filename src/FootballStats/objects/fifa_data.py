
FIFA_BASE_URL = "https://www.fifaindex.com"

class FifaMeta():

    def __init__(self, fifa_id, fifa_name, fifa_year, fifa_version):

        self.fifa_name = fifa_name
        self.fifa_id = fifa_id
        self.fifa_year = fifa_year
        self.fifa_version = fifa_version


class PlayerVersionStats():

    def __init__(self, stats_meta, stats):

        self.stats_meta = stats_meta
        self.bio = FifaBio(stats_meta, stats["bio"])
        self.club_info = FifaClubInfo(stats_meta, stats["club_info"])
        self.internation_info = FifaInternationalInfo(stats_meta, stats["international_info"])
        self.specialties = stats["specialties"]
        self.traits = stats["traits"]
        try:
            self.ball_skills = FifaBallSkills(stats_meta, stats["ball_skills"])
        except:
            self.ball_skills = FifaBallSkills(stats_meta, {})
        try:
            self.defence = FifaDefence(stats_meta, stats["defence"])
        except:
            self.defence = FifaDefence(stats_meta, {})
        try:
            self.mental = FifaMental(stats_meta, stats["mental"])
        except:
            self.mental = FifaMental(stats_meta, {})
        try:
            self.passing = FifaPassing(stats_meta, stats["passing"])
        except:
            self.passing = FifaPassing(stats_meta, {})
        try:
            self.physical = FifaPhysical(stats_meta, stats["physical"])
        except:
            self.physical = FifaPhysical(stats_meta, {})
        try:
            self.shooting = FifaShooting(stats_meta, stats["shooting"])
        except:
            self.shooting = FifaShooting(stats_meta, {})
        try:
            self.goalkeeper = FifaGoalkeeper(stats_meta, stats["goalkeeper"])
        except:
            self.goalkeeper = FifaGoalkeeper(stats_meta, {})

        
class FifaBio():

    def __init__(self, stats_meta, stats):

        self.stats_meta = stats_meta
        self.name = stats["name"]
        self.overall_rating = stats["overall_rating"]
        self.potential_rating = stats["potential_rating"]
        self.height = stats["height"]
        self.weight = stats["weight"]
        self.preferred_foot = stats["preferred_foot"]
        self.birth_date = stats["birth_date"]
        self.age = stats["age"]
        self.preferred_positions = stats["preferred_positions"]
        self.player_work_rate = stats["player_work_rate"]
        self.weak_foot = stats["weak_foot"]
        self.skill_moves = stats["skill_moves"]
        self.value = stats["value"]
        self.wage = stats["wage"]

class FifaClubInfo():

    def __init__(self, stats_meta, stats):

        self.stats_meta = stats_meta
        self.club_name = stats["club_name"]
        self.position = stats["position"]
        self.kit_number = stats["kit_number"]
        self.joined_club = stats["joined_club"]
        self.contract_ends = stats["contract_ends"]

class FifaInternationalInfo():

    def __init__(self, stats_meta, stats):

        self.stats_meta = stats_meta
        self.country = stats["country"]
        self.position = stats["position"]
        self.kit_number = stats["kit_number"]

class FifaStatsCategory():

    def __init__(self, stats_meta, stats, attributes):

        self.stats_meta = stats_meta
        for attribute in attributes:
            try:
                setattr(self, attribute, stats[attribute])
            except:
                setattr(self, attribute, None)

class FifaBallSkills(FifaStatsCategory):

    def __init__(self, stats_meta, stats):
        super().__init__(stats_meta, stats, ["ball_control","dribbling"])

class FifaDefence(FifaStatsCategory):

    def __init__(self, stats_meta, stats):
        super().__init__(stats_meta, stats, ["marking","slide_tackle","stand_tackle"])

class FifaMental(FifaStatsCategory):

    def __init__(self, stats_meta, stats):
        super().__init__(stats_meta, stats, ["aggression","reactions","att_position","interceptions","vision","composure"])

class FifaPassing(FifaStatsCategory):

    def __init__(self, stats_meta, stats):
        super().__init__(stats_meta, stats, ["crossing","short_pass","long_pass"])

class FifaPhysical(FifaStatsCategory):

    def __init__(self, stats_meta, stats):
        super().__init__(stats_meta, stats, ["acceleration","stamina","strength","balance","sprint_speed","agility","jumping"])

class FifaShooting(FifaStatsCategory):

    def __init__(self, stats_meta, stats):
        super().__init__(stats_meta, stats, ["heading","shot_power","finishing","long_shots","curve","fk_acc","penalties","volleys"])

class FifaGoalkeeper(FifaStatsCategory):

    def __init__(self, stats_meta, stats):
        super().__init__(stats_meta, stats, ["gk_positioning","gk_diving","gk_handling","gk_kicking","gk_reflexes"])

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

