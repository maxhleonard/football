import matplotlib.pyplot as plt
from FootballStats.objects.common import get_data_file
import datetime

def fifa_stat_progression(stats, category, attribute):

    stat_years = []
    fifa_versions = get_data_file("fifa_versions.json")
    for stats_version in stats:
        fifa_version = stats_version.stats_meta.fifa_version
        fifa_year = stats_version.stats_meta.fifa_year
        for version_date, ver in fifa_versions[fifa_year].items():
            if fifa_version == ver:
                date = datetime.datetime.strptime(version_date, "%Y-%m-%d")
                break
        attribute_value = getattr(getattr(stats_version, category), attribute)
        stat_years.append((date, attribute_value))
    stat_years.sort(key=lambda x: x[0])
    X = [x[0] for x in stat_years]
    y = [x[1] for x in stat_years]
    plt.plot(X, y)
    plt.title(stats[0].stats_meta.fifa_name + " - " + attribute.replace("_", " "))
    plt.xlabel("FIFA Version Date")
    plt.xlabel("FIFA Attribute Score")
    plt.show()

'''
from FootballStats.objects.ref_objects import *
from FootballStats.functions.visualizations import *
f = Footballer(name="Cristiano Ronaldo")
stats = f.get_all_fifa_stats()
'''
