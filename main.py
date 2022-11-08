import discord
import os
import requests
from discord.ui import Button, View
import math
import random
from troll_game import *
from replit import db

response = requests.get(
  "http://ddragon.leagueoflegends.com/cdn/12.18.1/data/en_US/champion.json")
data = response.json()

intents = discord.Intents().all()

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

  print(message.author)
  if message.author == client.user:
    return

  if message.content.lower().startswith("combos"):
    embed = discord.Embed(
      title="Bot Lane Combos",
      description="1. Kindred | Taric \n 2. Caitlyn | Lux\n3. Sion | Ivern\n",
      color=discord.Color(0x979c9f))
    await message.channel.send(embed=embed)

  if message.content.lower().startswith("troll"):
    await message.channel.send(":troll:")
    await message.channel.send("<@303094753128480768>")

  if message.content.lower().startswith("ping the troll"):
    await message.channel.send(":troll:")
    await message.channel.send("<@303094753128480768>")

  if message.content.lower().startswith("patch notes"):
    await message.channel.send(
      "```05/10/2022: Hammer spawn increased to 3\n05/10/2022: Hammer spawn changed from entire board to bottom 6 rows\n01/11/2022: Log added under 'log' command and high score tracking added```"
    )

  if message.content.lower().startswith("champ"):
    await message.channel.send(":troll:")
    await message.channel.send(message.author.mention)

  parts = message.content.split(" ")

  for part in parts:
    part = part.capitalize()
    print(part)
    if part in data['data']:
      embed = discord.Embed(title=data['data'][part]['id'],
                            description=data['data'][part]['blurb'],
                            color=discord.Color(0x00FF00))
      await message.channel.send(embed=embed)

  if message.content.lower().startswith("game"):
    await troll_game(message)

  if message.content.lower().startswith("log"):
    if (db['scores'] != None):
      past = db['scores']
      end = past[-10:]
      description = " "
      for score in end:
        description += "`" + score[1][10:19] + " ` :  `  " + score[
          0] + " ` : ` " + score[2] + " ` : ` Score:" + str(
            score[3]) + " `\n\n"
      embed = discord.Embed(title='',
                            description=description,
                            color=discord.Color(0x00FF00))
      await message.channel.send(embed=embed)
    else:
      pass

  if message.content.lower().startswith("reset"):
    db['scores'] = []

  if message.content.lower().startswith("highscores"):
    scores = db['highScores'].value
    sorted_list = sorted(scores, key=lambda x: x[1], reverse=True)
    print(sorted_list)
    description = ""
    for x in range(5):
      if (len(sorted_list) > x):
        description += "```" + str(
          x + 1) + ". " + sorted_list[x][0] + "        Score: " + str(
            sorted_list[x][1]) + "``` \n"
    embed = discord.Embed(title='Troll Scores',
                          description=description,
                          color=discord.Color(0x00FF00))
    await message.channel.send(embed=embed)


client.run(
  'MTAyNTE1NzM5NDg1NjE1NzMwNw.GCX75p.qPZIQt_sxQPnyRjEK8OOHCoEdebIiJwea9dSEc')
