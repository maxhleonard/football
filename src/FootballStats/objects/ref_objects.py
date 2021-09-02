from .fifa_data import *

class Footballer():


    def __init__(self, name):

        self.name = name

    def get_fifa_url(self, fifa_year, target_date):

        fifa_name = "-".join(self.name.split()).lower()

    def get_fifa_stats(self, fifa_year, target_date):

        url = self.get_fifa_url(fifa_year, target_date)
        stats = 

