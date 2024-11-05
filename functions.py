import discord
import requests
import json
import random
import wikipedia
from googlesearch import search


#Function to create an embed
def createEmbed(titl):
    embed = discord.Embed(title=titl, color=discord.Color.red())
    return embed

#Help Embed
def helpEmbed():
    embed = discord.Embed(title="Help Commands",
                          description="Commands Available in the Bot.",
                          color=discord.Color.purple())
    embed.add_field(
        name="Extras:",
        value="To get Details of a certain Command use `?help [command name]`",
        inline=False)
    embed.add_field(
        name="NOTE:",
        value=
        "Values with **[] are Required** while values with **{} are Optional**.",
        inline=False)
    embed.add_field(name="User Commands:",
                    value="help\nStatus\nDm\nTr\nCode\nMath\nnextjam",
                    inline=False)

    embed.add_field(name="Fun Commands:",
                    value="Ball\nCoin\nDice\nWiki\nChuckNorris",
                    inline=False)
    embed.set_thumbnail(
        url=
        "https://media.discordapp.net/attachments/957348693902753822/968856641778909204/unknown.png?width=475&height=473"
    )
    return embed

#wikipedia get info command
def getInfo(toSearchFor):
  try:
    results = wikipedia.summary(toSearchFor, sentences=5)
    embed = discord.Embed(title="Information on {}".format(toSearchFor),description=results,color=discord.Color.red())
    return embed

  except:
    query = toSearchFor
    for q in search(query, tld='co.in', lang='en',safe='on',num=10, stop=10, pause=2):
      pageErrorEmbed = discord.Embed(title="Couldn't find what you're looking for!\nTry these links.", description=q,color = 0x27FF13)
      print(q)
      return pageErrorEmbed
    

#chuck norris facts
def getChuck():
  url = "https://api.chucknorris.io/jokes/random"
  results = requests.request("GET",url)
  formattedFact = json.loads(results.text)
  embed= discord.Embed(title="Chuck Norris facts:",description=formattedFact["value"],color=0xff6600)

  return embed

  