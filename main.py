import discord
import os
import requests
from discord.ui import Button, View
import math
import random
import inflect
from troll_game import *

response = requests.get("http://ddragon.leagueoflegends.com/cdn/12.18.1/data/en_US/champion.json")
data = response.json()

intents = discord.Intents().all()

client = discord.Client(intents = intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

  print(message.author)
  if message.author == client.user:
    return
    
  if message.content.lower().startswith("combos"):
    embed = discord.Embed(title = "Bot Lane Combos",
      description = "1. Kindred | Taric \n 2. Caitlyn | Lux\n3. Sion | Ivern\n",
      color = discord.Color(0x979c9f))
    await message.channel.send(embed=embed)

  if message.content.lower().startswith("troll"):
    await message.channel.send(":troll:")
    await message.channel.send("<@303094753128480768>")

  if message.content.lower().startswith("ping the troll"):
    await message.channel.send(":troll:")
    await message.channel.send("<@303094753128480768>")

  if message.content.lower().startswith("champ"):
    await message.channel.send(":troll:")
    await message.channel.send(message.author.mention)

  parts = message.content.split(" ")
  
  for part in parts:
    part = part.capitalize()
    print(part)
    if part in data['data']:
      embed = discord.Embed(title = data['data'][part]['id'],
      description = data['data'][part]['blurb'],
      color = discord.Color(0x00FF00))
      await message.channel.send(embed=embed)

  if message.content.lower().startswith("game"):
    await troll_game(message)
   
client.run(os.environ['token'])

