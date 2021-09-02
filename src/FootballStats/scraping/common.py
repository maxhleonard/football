import urllib3
import bs4

pm = urllib3.PoolManager()


def get_soup(url):

    return bs4.BeautifulSoup(pm.request("GET", url).data, "html.parser")