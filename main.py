from webserver import keep_alive
import os
import discord
from discord.ext import commands
import random
import googletrans
import time
import datetime as dt
from discord.utils import get
from functions import *

intents = discord.Intents.all()
activity = discord.Game(name="BWJ Server | ?help")
#intents.member = True
bot = commands.Bot(command_prefix="?",
                   activity=activity,
                   intents=intents,
                   help_command=None)
translator = googletrans.Translator()
dtm = dt.datetime.now()

#Fun commands list
ballResponses = ["Yes", "No", "Maybe...", "Sure.", "I have no Idea."]
coinResponses = ["Heads", "Tails"]


#bot functions
@bot.event
async def on_connect():
    print("Brrrrr....")


@bot.event
async def on_member_join(member):
    await member.send(
        ':tada: Thanks for Joining the BWJ server! I hope you enjoy you stay here! :tada:'
    )
    await member.send(embed=createEmbed(
        "For More information check #:pushpin:-rules.\n To Get Roles check #:star:-roles-Роли."
    ))





@bot.command(aliases=["c", "cd"])
async def code(ctx, *, code):
    await ctx.message.delete()
    await ctx.send('`' + code + '`')


#Translate command
@bot.command(aliases=["translate", "t"])
async def tr(ctx, langTo, *, text):
  try:
    languages = googletrans.LANGUAGES
    results = translator.translate(text, dest=langTo)
    srcLang = translator.detect(text)
    langName = languages[srcLang.lang]
    embed = discord.Embed(title="Translated from {} to {}".format(
            langName, langTo),description=results.text,color=discord.Color.blue())
    embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
  except:
    await ctx.send(":x: Couldn't translate that!")



#purge command
@bot.command(aliases=['purge','clear'])
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")


#To send translation of a particular message to the Command user's DMs
@bot.command()
async def dm(ctx, dstLang):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(
            embed=createEmbed('Oops! You cant use this command in DMs.'))
        return
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    try:
        languages = googletrans.LANGUAGES
        results = translator.translate(message.content, dest=dstLang)
        srcLang = translator.detect(message.content)
        langName = languages[srcLang.lang]
        embed = discord.Embed(title="Translated from {} to {}".format(
            langName, dstLang),
                              description=results.text,
                              color=discord.Color.blue())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar_url)
        await ctx.author.send(embed=embed)
    except:
        await ctx.send(":x: Couldn't translate that!")


#To check if the bot is online
@bot.command()
async def status(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(
            embed=createEmbed('Oops! You cant use this command in DMs.'))
        return
    await ctx.message.delete()
    embed = discord.Embed(
        title=":green_circle: Online",
        description=
        "Hello {}! Im up and Running at GodSpeed, Thanks for asking!".format(
            ctx.author.display_name),
        color=discord.Color.green())
    await ctx.send(embed=embed)


#wikipedia command
@bot.command(aliases=["info"])
async def wiki(ctx, *, query):
  #try:
  await ctx.send(embed=getInfo(query))

  #except:
    #await ctx.send(embed=createEmbed(":x: Can't find the info you're looking for!"))


#8 ball command
@bot.command(aliases=["8"])
async def ball(ctx):
    response = random.choice(ballResponses)
    ballEmbed = discord.Embed(
        title=":8ball: 8 Ball",
        description="**8Ball said, {}**".format(response),
        color=0x000000)
    await ctx.send(embed=ballEmbed)


#Coin flip command
@bot.command(aliases=["flip", "toss"])
async def coin(ctx):
    tossResults = random.choice(coinResponses)
    coinEmbed = discord.Embed(
        title=":coin: Coin",
        description="**Coin flipped to {}**".format(tossResults),
        color=0xFCDF00)
    await ctx.send(embed=coinEmbed)


#Dice throw command
@bot.command(aliases=["throw"])
async def dice(ctx, first: int = None, second: int = None):
    if first == None or second == None:
        await ctx.send(embed=createEmbed(":game_die: Dice rolled to {}!".format(
            random.randrange(1, 6))))

    else:
        await ctx.send(embed=createEmbed("Dice rolled to {}".format(
            random.randrange(first, second))))


@dice.error
async def diceError(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send(embed=createEmbed(":x: Please provide a valid number!"))


#chuck norris facts command
@bot.command(aliases=["fact"])
async def chuck(ctx):
  await ctx.send(embed=getChuck())

  
      
#Help command
@bot.group(invoke_without_command=True)
async def help(ctx):
    await ctx.send(embed=helpEmbed())




#code help command
@help.command()
async def Code(ctx):
    codeEmbed = discord.Embed(title="Convert your message into code block.",
                              description="?code [message]",
                              color=discord.Color.red())
    codeEmbed.add_field(
        name="Note:",
        value="Values with **[] are Required** and **{} are optional**.")
    codeEmbed.add_field(name="Aliases:", value="c, cd, code", inline=False)
    await ctx.send(embed=codeEmbed)


#translate help command
@help.command()
async def Tr(ctx):
    trEmbed = discord.Embed(
        title="To translate your message in a specified language.",
        description="?tr [language] [message]",
        color=discord.Color.red())
    trEmbed.add_field(
        name="Note:",
        value="Values with **[] are Required** and **{} are optional**.")
    trEmbed.add_field(name="Aliases:", value="t, translate, tr", inline=False)
    await ctx.send(embed=trEmbed)


#Dm translate help command
@help.command()
async def Dm(ctx):
    dmEmbed = discord.Embed(
        title="To get translation of a message in your DMs.",
        description="?DM [language]",
        color=discord.Color.red())
    dmEmbed.add_field(
        name="Usage:",
        value=
        "In order to translate a message you should reply to that messsage and use the command."
    )
    dmEmbed.add_field(
        name="Note:",
        value="Values with **[] are Required** and **{} are optional**.")
    await ctx.send(embed=dmEmbed)


#status help command
@help.command()
async def Status(ctx):
    statEmbed = discord.Embed(
        title="Sends a message to let know that the bot is Online.",
        description="?status",
        color=discord.Color.red())
    await ctx.send(embed=statEmbed)


#8ball help command
@help.command()
async def Ball(ctx):
    ballEmbed = discord.Embed(
        title="Ask any questions to the 8Ball and it will answer.",
        description="?ball [question]", color=discord.Color.red())
    ballEmbed.add_field(
        name="Note:",
        value="Values with **[] are Required** and **{} are optional**.")
    ballEmbed.add_field(name="Aliases:", value="8, ball", inline=False)
    await ctx.send(embed=ballEmbed)


#Coin help command
@help.command()
async def Coin(ctx):
    coinEmbed = discord.Embed(title="Toss a Virtual Coin.",
                              description="?coin", color=discord.Color.red())
    coinEmbed.add_field(name="Aliases:",
                        value="flip, toss, coin",
                        inline=False)
    await ctx.send(embed=coinEmbed)


#Dice help command
@help.command()
async def Dice(ctx):
    diceEmbed = discord.Embed(
        title=
        "Roll a Dice between **1 to 6** or **any random range of number**.",
        description="?dice {first number} {second number}", color=discord.Color.red())
    diceEmbed.add_field(name="Aliases:", value="dice, throw", inline=False)
    diceEmbed.add_field(
        name="Note:",
        value="Values with **[] are Required** and **{} are optional**.")
    await ctx.send(embed=diceEmbed)


#Wikipedia help command
@help.command()
async def Wiki(ctx):
    wikiEmbed = discord.Embed(
        title="Gives you information about almost anything.",
        description="?wiki [topic]", color=discord.Color.red())
    wikiEmbed.add_field(name="Aliases:", value="wiki, info", inline=False)
    wikiEmbed.add_field(
        name="Note:",
        value="Values with **[] are Required** and **{} are optional**.")
    await ctx.send(embed=wikiEmbed)

#chuck norris help command
@help.command()
async def ChuckNorris(ctx):
  chuckEmbed = discord.Embed(title="Sends a Funny Chuck Norris fact.", description = "?chuck", color = 0xcc6600)
  chuckEmbed.add_field(name="Aliases:", value="fact, chuck", inline=False)
  await ctx.send(embed=chuckEmbed)

#main help command
@help.command()
async def Help(ctx):
    helpEmbed = discord.Embed(title="Sends a list of all Available Commands.",
                              description="?help {command name}",
                              color=discord.Color.red())
    helpEmbed.add_field(
        name="Note:",
        value="Values with **[] are Required** and **{} are optional**.")
    await ctx.send(embed=helpEmbed)


#GameJam command
@bot.command()
async def nextjam(ctx):
    jamEmbed = discord.Embed(
        title="BWJ Game Jam",
        description=
        'The Next BWJ Game Jam Will start from **1 September,2022** to **10 September,2022**.',
        color=0xff8787,
        timestamp=ctx.message.created_at,
        url="https://itch.io/jam/black-and-white-jam-9")
    jamEmbed.set_thumbnail(
        url=
        "https://img.itch.zone/aW1hZ2UyL2phbS8zMTgzMTMvODU1OTY3NC5naWY=/original/G9b05s.gif"
    )
    jamEmbed.add_field(name="Rules:",
                       value="https://itch.io/jam/black-and-white-jam-googolplex",
                       inline=False)
    jamEmbed.add_field(name="Voting!",value="As a celebration for the 10th BWJ Jam, the theme will be revealed when the jam begins( :sparkles: **Secret theme** :sparkles: )")
    jamEmbed.add_field(
        name="**Note:**",
        value="**This Command will be updated as per the Jam.**",
        inline=False)

    await ctx.send(embed=jamEmbed)





keep_alive()

TOKEN = os.environ.get("DISCORD_BOT_SECRET")

bot.run(TOKEN)
