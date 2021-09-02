from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


def scrape_page(driver):

	odds = []
	results = driver.find_element_by_id("tournamentTable").find_elements_by_tag_name("tr")
	for row in results:
		if row.get_attribute("class") ==  "center nob-border":
			date = row.text.replace(" 1 X 2 B's", "")
		elif "deactivate" in row.get_attribute("class"):
			game = {"date":date}
			cols = row.find_elements_by_tag_name("td")
			game["time"] = cols[0].text
			teams = cols[1].text.split("-")
			game["home"] = teams[0].strip()
			try:
				game["away"] = teams[1].strip()
			except:
				print(cols[1].text)
			game["score"] = cols[2].text
			try:
				game["home_odds"] = int(cols[3].text)
			except:
				game["home_odds"] = None
			try:
				game["draw_odds"] = int(cols[4].text)
			except:
				game["draw_odds"] = None
			try:
				game["away_odds"] = int(cols[5].text)
			except:
				game["away_odds"] = None
			game["num_makers"] = int(cols[6].text)
			odds.append(game)
	return odds

def scrape_odds():

	options = Options()
	options.headless = True
	driver = webdriver.Chrome(options=options)
	odds = []
	for year in ["-" + str(y) + "-" + str(y+1) for y in range(2003, 2021)] + [""]:
		url = "https://www.oddsportal.com/soccer/england/premier-league{year}/results/".format(year=year)
		print(url)
		driver.get(url)
		time.sleep(1)
		while True:	
			try:
				odds += scrape_page(driver)
			except:
				time.sleep(2)
				odds == scrape_page(driver)
			try:
				pages = driver.find_element_by_id("pagination").find_elements_by_tag_name("a")
			except:
				break
			next_link = pages[-2].get_attribute("href")
			if url == next_link:
				break
			else:
				url = next_link
				driver.get(url)
				print(url)
				time.sleep(1)

	return pd.DataFrame(odds)

def get_correct_profit(home, draw, away, winner):

	if winner == "home":
		winning_odds = home
	elif winner == "draw":
		winning_odds = draw
	elif winner == "away":
		winning_odds = away

	if winning_odds < 0:
		return (10000 / abs(winning_odds)) + 100
	else:
		return winning_odds + 100

def prep_odds(df):

	df["winner"] = df["score"].apply(lambda x: "home" if int(x.split(":")[0]) > int(x.split(":")[1]) else ("away" if int(x.split(":")[0]) < int(x.split(":")[1]) else "draw"))
	df["predicted_winner"] = df.apply(lambda x: "home" if x["home__odds"] < x["away_odds"] and x["home_odds"] < x["draw_odds"] else ("draw" if x["draw_odds"] < x["home_odds"] and x["draw_odds"] < x["away_odds"] else "away"), axis=1)
	return df




