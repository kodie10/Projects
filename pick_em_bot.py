import asyncio
import sqlite3
from datetime import date
from datetime import datetime
import discord
import pytz
import requests
from discord import Intents
from discord.ext import commands
from discord.ext.commands import has_permissions, CommandError

conn = sqlite3.connect('pick_em_bot.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        user_id INTEGER,
        matchday INTEGER,
        match_name TEXT,
        predicted_home INTEGER,
        predicted_away INTEGER
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS running_scores (
        user_id INTEGER,
        points INTEGER DEFAULT 0
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS matchdays (
        matchday INTEGER PRIMARY KEY
        )
''')
conn.commit()


def get_keys(path):
    with open(path, 'r') as file:
        key = file.readline().strip()
    return key


discord_key = get_keys('discord_key.txt')
api_key = get_keys('api_key.txt')
intents = Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

predictions = {}
running_scores = {}
bot.remove_command('help')


def get_match_scores(matchday):
    headers = {'X-Auth-Token': api_key}
    url = f'https://api.football-data.org/v2/competitions/PL/matches?season=2023&matchday={matchday}'

    response = requests.get(url, headers=headers)
    data = response.json()
    matches = data['matches']
    match_scores = {}

    for match in matches:
        if match['status'] == 'FINISHED':  # Only consider matches that have finished
            match_key = str(matchday)
            if match_key not in match_scores:
                match_scores[match_key] = []

            home_team = match['homeTeam']['name']
            away_team = match['awayTeam']['name']
            home_score = match['score']['fullTime']['homeTeam']
            away_score = match['score']['fullTime']['awayTeam']

            if home_score is not None and away_score is not None:
                match_name = f"{home_team} vs {away_team}"
                match_scores[match_key].append({
                    'teams': match_name,
                    'actual_home': home_score,
                    'actual_away': away_score
                })
    return match_scores


def get_current_matchday():
    response = requests.get('https://api.football-data.org/v2/competitions/PL/matches?season=2023',
                            headers={'X-Auth-Token': api_key})
    matches = response.json()
    today = date.today()

    for match in matches['matches']:
        match_date = date.fromisoformat(match['utcDate'][:10])
        if match_date >= today:
            return match['season']['currentMatchday']

    return None


@bot.command()
@has_permissions(administrator=True)
async def calculate_points(ctx, matchday=get_current_matchday()):
    c.execute("""
        SELECT 1
        FROM matchday
        WHERE matchday = ?
    """, (matchday,))

    if c.fetchone():
        await ctx.send(f"Scores for matchday {matchday} have already been calculated")
    actual_scores = get_match_scores(matchday)
    points = {}

    # Query the database for user predictions for the given matchday
    c.execute("""
    SELECT user_id, match_name, predicted_home, predicted_away
    FROM predictions
    WHERE matchday = ?
    """, (matchday,))

    user_predictions_results = c.fetchall()

    for user_id, match_name, predicted_home, predicted_away in user_predictions_results:
        # Initialize points for the user if not already initialized
        if user_id not in points:
            points[user_id] = 0

        # Loop through actual match results to find the corresponding match
        for actual in actual_scores[str(matchday)]:
            if match_name == actual['teams']:
                # Check if the prediction was spot-on
                if (predicted_home == actual['actual_home'] and
                        predicted_away == actual['actual_away']):
                    points[user_id] += 3
                # Check if the user predicted the outcome correctly (win, lose, or draw)
                elif (predicted_home - predicted_away ==
                      actual['actual_home'] - actual['actual_away']):
                    points[user_id] += 1
                else:
                    if predicted_home == actual['actual_home']:
                        points[user_id] += 1
                    elif predicted_away == actual['actual_away']:
                        points[user_id] += 1

    # Now, store/update the points in the SQLite database
    for user_id, newly_calculated_points in points.items():
        c.execute("""
        SELECT 1
        FROM running_scores
        WHERE user_id = ?
        """, (user_id,))

        if c.fetchone():
            # Update existing score
            c.execute("""
            UPDATE running_scores
            SET points = points + ?
            WHERE user_id = ?
            """, (newly_calculated_points, user_id))
        else:
            # Insert new score
            c.execute("""
            INSERT INTO running_scores (user_id, points)
            VALUES(?, ?)
            """, (user_id, newly_calculated_points))

    c.execute("""
        INSERT INTO matchday (matchday)
        VALUES (?)
    """, (matchday,))

    conn.commit()

    await ctx.send(f"points for matchday {matchday} have been calculated")


@bot.command()
async def leaderboard(ctx, matchday: int = int(get_current_matchday())):
    # Fetch user scores from the database
    c.execute("""
        SELECT user_id, points
        FROM running_scores
        ORDER BY points DESC
    """)

    results = c.fetchall()

    # Create a discord embed for the leaderboard
    embed = discord.Embed(title=f"Leaderboard for Matchday {matchday}",
                          description="Here are the point standings:", color=discord.Color.green())

    for user_id, point in results:
        user = bot.get_user(user_id)
        embed.add_field(name=user.name, value=f"{point} Points", inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Bot Commands", description="List of commands are:", color=discord.Color.blue())

    embed.add_field(name="!predict <match week>", value="Use to make score predictions for user chosen match week",
                    inline=False)
    embed.add_field(name="!show_predictions <match week>", value="Shows your predictions for the chosen match week",
                    inline=False)

    embed.add_field(name="!leaderboard <match week>", value="shows the current score for the chosen match week")

    embed.add_field(name="!all_predictions <match week>", value="Shows all predictions made for the chosen match week",
                    inline=False)

    embed.add_field(name="!calculate_scores <match week>",
                    value="admin only, calculates scores for the chosen match week can only be run once per week so "
                          "wait until all matches have been played", inline=False)

    embed.add_field(name="!add_scores <username> <point value to add>",
                    value="admin only, manually edit scores in database table")

    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def all_predictions(ctx, matchday: int = int(get_current_matchday())):
    # Create an embed object for the predictions
    embed = discord.Embed(title=f"Predictions for Matchday {matchday}",
                          description="Here are all the user predictions for this matchday:",
                          color=discord.Color.blue())

    # Query the database for predictions on the given matchday
    c.execute("""
    SELECT user_id, match_name, predicted_home, predicted_away
    FROM predictions
    WHERE matchday = ?
    """, (matchday,))

    results = c.fetchall()

    user_predictions_map = {}
    for user_id, match_name, home_score, away_score in results:
        if user_id not in user_predictions_map:
            user_predictions_map[user_id] = []
        user_predictions_map[user_id].append(f"{match_name}: {home_score}-{away_score}")

    # Loop through the fetched results and populate the embed
    for user_id, predictions in user_predictions_map.items():
        user = bot.get_user(user_id)
        prediction_list = '\n'.join(predictions)
        embed.add_field(name=user.name, value=prediction_list, inline=False)

    await ctx.send(embed=embed)


async def collect_predictions(ctx, match_day: int):
    user = ctx.author
    dm_channel = user.dm_channel
    if dm_channel is None:
        dm_channel = await user.create_dm()

    response = requests.get(f'https://api.football-data.org/v2/competitions/PL/matches?matchday={match_day}',
                            headers={'X-Auth-Token': api_key})
    matches = response.json()

    if 'matches' in matches:
        utc = pytz.timezone('UTC')
        eastern = pytz.timezone('US/Eastern')

        for match in matches['matches']:
            home_name = match['homeTeam']['name']
            away_name = match['awayTeam']['name']
            utc_time = datetime.fromisoformat(match['utcDate'][:-1])
            utc_time = utc.localize(utc_time)
            eastern_time = utc_time.astimezone(eastern)

            await dm_channel.send(f"Enter your prediction for {home_name} vs {away_name} "
                                  f"on {eastern_time.strftime('%D')} at {eastern_time.strftime('%H:%M %p %Z')} format- Home Score-Away Score")

            def check(msg):
                return msg.author == user and isinstance(msg.channel, discord.DMChannel) and '-' in msg.content

            try:
                prediction = await bot.wait_for('message', timeout=60.0, check=check)
                home_score, away_score = map(int, prediction.content.split('-'))

                c.execute("""
                SELECT 1
                FROM predictions
                WHERE user_id = ? AND match_name = ? AND matchday = ?
                """, (user.id, f'{home_name} vs {away_name}', match_day))

                if c.fetchone():
                    # Update existing prediction
                    c.execute("""
                    UPDATE predictions
                    SET predicted_home = ?, predicted_away = ?
                    WHERE user_id = ? AND match_name = ? AND matchday = ?
                    """, (home_score, away_score, user.id, f'{home_name} vs {away_name}', match_day))
                else:
                    # Insert new prediction
                    c.execute("""
                    INSERT INTO predictions(user_id, matchday, match_name, predicted_home, predicted_away)
                    VALUES(?, ?, ?, ?, ?)
                    """, (user.id, match_day, f'{home_name} vs {away_name}', home_score, away_score))

                conn.commit()

            except asyncio.TimeoutError:
                await dm_channel.send('Sorry, you took too long to make a prediction for this match.')
    else:
        await dm_channel.send("No matches found for this game week.")


@bot.command()
async def predict(ctx, matchday: int):
    user = ctx.author

    # Get current datetime in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Fetch the matches for the given matchday
    response = requests.get(f'https://api.football-data.org/v2/competitions/PL/matches?season=2023&matchday={matchday}',
                            headers={'X-Auth-Token': api_key})
    matches = response.json()

    # Check if the matches for the given matchday are valid
    if 'matches' in matches:
        # Parse the kickoff time of the first match of the matchday to a datetime object
        first_match_time = datetime.fromisoformat(matches['matches'][0]['utcDate'][:-1])
        first_match_time = pytz.utc.localize(first_match_time)

        # If the current datetime is after the kickoff time of the first match, do not allow predictions
        if current_time_utc > first_match_time:
            await ctx.send("Sorry, you cannot make predictions after the first game has kicked off.")
        else:
            # If current datetime is before the kickoff time of the first match, allow predictions
            predictions[user.id] = []
            await collect_predictions(ctx, matchday)
    else:
        await ctx.send("Invalid match week.")


@bot.command()
async def show_predictions(ctx, current_matchday=get_current_matchday()):
    user = ctx.author.id

    # Query the database for predictions
    c.execute("""
    SELECT match_name, predicted_home, predicted_away
    FROM predictions 
    WHERE user_id = ? AND matchday = ?
    """, (user, current_matchday))

    predictions = c.fetchall()

    # Create an embed object
    embed = discord.Embed(title=f"Your Predictions for Matchday {current_matchday}",
                          description=f"Here are your predictions for this week:",
                          color=discord.Color.random())

    # Add the predictions to the embed
    for prediction in predictions:
        match_name, predicted_home, predicted_away = prediction
        embed.add_field(name=match_name, value=f"{predicted_home}-{predicted_away}", inline=False)

    # Check if there are any predictions for the current matchday
    if len(embed.fields) == 0:
        await ctx.send("You haven't made any predictions for the current matchday.")
    else:
        # Send the embed object in the channel
        await ctx.send(embed=embed)


@bot.command()  # ensures that the user has administrator permissions
@has_permissions(administrator=True)
async def add_score(ctx, user_name: discord.Member, score: int):
    try:
        # Fetch the user object from the username
        user = user_name

        if not user:
            await ctx.send(f"Couldn't find user with the username: {user_name}")
            return

        user_id = user.id
        # First, retrieve the current score for the user
        c.execute("SELECT points FROM running_scores WHERE user_id = ?", (user_id,))
        result = c.fetchone()

        # If the user has an existing score, add to it
        if result:
            current_score = result[0]
            new_score = current_score + score

            # Update the user's existing score in the database
            c.execute("UPDATE running_scores SET points = ? WHERE user_id = ?", (new_score, user_id))

        # If the user doesn't have an existing score, insert a new entry
        else:
            c.execute("INSERT INTO running_scores (user_id, points) VALUES (?, ?)", (user_id, score))
            new_score = score

        conn.commit()

        # Notify everyone that the score has been updated/added
        await ctx.send(
            f"@everyone POTENTIAL SHENANIGANS! The score for user <@{user_id}> has been updated to {new_score} points!")

    except CommandError as ce:
        await ctx.send(f"You do not have the required permissions to use this command")

    except Exception as e:
        await ctx.send(f"Error updating/adding score: {e}")


bot.run(discord_key)
