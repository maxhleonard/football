


def best_odds(trades, outcomes=["home","draw","away"]):

	used = 0
	winnings = 0

	for ind, row in trades.iterrows():
		best = max([row["home_odds"], row["draw_odds"], row["away_odds"]])
		for outcome in outcomes:
			if row[outcome + "_odds"] == best:
				used += 100
				if row["winner"] == outcome:
					if best < 0:
						winnings += (10000 / abs(best)) + 100
					else:
						winnings += best + 100
	print(used, winnings)