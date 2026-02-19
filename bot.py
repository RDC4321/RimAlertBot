import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from datetime import datetime, timedelta

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	print("Received /start command")
	await update.message.reply_text("RimAlertBot is live from AWS!\nHi Lods!\n\nFeatures:\n1. /score(YYYY-MM-DD) - shows all the completed NBA games on that day.\n/score (no dates) will show games completed today.\n\n2./live - shows all currently live/in progress NBA games today.\n\n3./team - shows current games & scheduled games of a specific team.\n\n4./schedule - shows all the scheduled games for the next 7 days. ")

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
	api_key = os.getenv("BALLDONTLIE_API_KEY")

	if context.args:
		date_input = context.args[0]
		try:
			datetime.strptime(date_input,"%Y-%m-%d")
		except ValueError:
			await update.message.reply_text("Invalid date format. Use YYYY-MM-DD.")
			return
	else:
		date_input = datetime.now().strftime("%Y-%m-%d") 
	url = "https://api.balldontlie.io/v1/games"
	headers = {
		"Authorization": f"Bearer {api_key}"
	}
	params = {
		"dates[]":date_input
	}

	response = requests.get(url, headers=headers, params=params)

	if response.status_code != 200:
		await update.message.reply_text("Error fetching games.")
		return

	data = response.json()
	games = data.get("data",[])

	if not games:
		await update.message.reply_text(f"No NBA games on {date_input}")
		return
	message = f"NBA Games on {date_input}:\n\n"

	for game in games:
		home = game["home_team"]["full_name"]
		away = game["visitor_team"]["full_name"]
		home_score = game["home_team_score"]
		away_score = game["visitor_team_score"]
		status = game["status"]

		message += f"{away} {away_score} - {home_score} {home}\n"
		message += f"Status: {status}\n\n"

	await update.message.reply_text(message)

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
	api_key = os.getenv("BALLDONTLIE_API_KEY")
	today = datetime.now().strftime("%Y-%m-%d")
	url = "https://api.balldontlie.io/v1/games"
	headers = {
		"Authorization": f"Bearer {api_key}"
	}
	params = {
		"dates[]": today
	}
	response = requests.get(url, headers=headers, params=params)
	if response.status_code != 200:
		await update.message.reply_text("Error fetching live games.")
		return
	data = response.json()
	games = data.get("data",[])
	live_games = []
	for game in games:
		if game["status"] not in ["Final","Scheduled"]:
			live_games.append(game)
	if not live_games:
		await update.message.reply_text("No live NBA games right now")
		return
	message = "Live NBA games:\n\n"
	for game in live_games:
		home = game["home_team"]["full_name"]
		away = game["visitor_team"]["full_name"]
		home_score = game["home_team_score"]
		away_score = game["visitor_team_score"]
		status = game["status"]
		message += f"{away} {away_score} - {home_score} {home}\n"
		message += f"Status: {status}\n\n"
	await update.message.reply_text(message)

async def team(update:Update, context: ContextTypes.DEFAULT_TYPE):
	if not context.args:
		await update.message.reply_text("Please provide a team name. Example: /team Lakers")
		return
	original_query = " ".join(context.args)
	team_query = original_query.lower()
	api_key = os.getenv("BALLDONTLIE_API_KEY")
	today = datetime.now().strftime("%Y-%m-%d")
	url = "https://api.balldontlie.io/v1/games"
	headers = {
		"Authorization": f"Bearer {api_key}"
	}
	dates_list = [
		(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
		for i in range(7)
	]
	params = [("dates[]",date) for date in dates_list]
	
	response = requests.get(url, headers=headers,params=params)
	if response.status_code != 200:
		await update.message.reply_text("Error fetching games")
		return
	data = response.json()
	games = data.get("data",[])
	today_match = None
	future_match = None
	for game in games:
		home = game["home_team"]["full_name"]
		away = game["visitor_team"]["full_name"]
		game_date = game["date"][:10]
		if team_query in home.lower() or team_query in away.lower():
			if game_date == today:
				today_match = game
				break
			elif game_date > today and future_match is None:
				future_match = game
	if today_match:
		home = today_match["home_team"]["full_name"]
		away = today_match["visitor_team"]["full_name"]
		home_score = today_match["home_team_score"]
		away_score = today_match["visitor_team_score"]
		status = today_match["status"]
		message = f"{away} {away_score} - {home_score} {home}\n"
		message += f"Status: {status}"
		await update.message.reply_text(message)
		return
	if future_match:
		home = future_match["home_team"]["full_name"]
		away = future_match["visitor_team"]["full_name"]
		game_date = future_match["date"][:10]
		message = f"Next Game:\n{away} vs {home}\nDate: {game_date}"
		await update.message.reply_text(message)
		return
	await update.message.reply_text(f"No upcoming games found for {original_query}.")

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
	api_key = os.getenv("BALLDONTLIE_API_KEY")
	url = "https://api.balldontlie.io/v1/games"
	headers = {
		"Authorization": f"Bearer {api_key}"
	}
	dates_list = [
		(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
		for i in range(7)
	]
	params = [("dates[]", date) for date in dates_list]
	response = requests.get(url, headers=headers,params=params)
	if response.status_code !=200:
		await udpate.message.reply_text("Error fetching schedule.")
		return
	data = response.json()
	games = data.get("data",[])
	if not games:
		await update.message.reply_text("No scheduled games in the next 7 days.")
		return
	games_sorted = sorted(games, key=lambda g: g["date"])
	message = "NBA Schedule (Next 7 days):\n\n"
	for game in games_sorted:
		full_datetime = game["date"]
		date_part = full_datetime[:10]
	
		home = game["home_team"]["full_name"]
		away = game["visitor_team"]["full_name"]
		message += f"{date_part} - {away} vs {home}\n"
	await update.message.reply_text(message) 

def main():
	app = ApplicationBuilder().token(TOKEN).build()
	app.add_handler(CommandHandler("start", start))
	app.add_handler(CommandHandler("score", score))
	app.add_handler(CommandHandler("live", live))
	app.add_handler(CommandHandler("team", team))
	app.add_handler(CommandHandler("schedule",schedule))
	print("Bot is running...")
	app.run_polling()

if __name__ == "__main__":
	main()
