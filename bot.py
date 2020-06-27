import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl
import random

description = '''ALSQ bot sample '''

bot = commands.Bot(command_prefix='$', description=description)

@bot.event
async def on_ready():
    print("Logged in as {} {}".format(bot.user.name, bot.user.id))
    print("---------")

@bot.command(pass_context=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')
@bot.command()
async def roll(ctx, dice: str):
    # rolls a dice in NdN format.
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send("Format has to be in NdN")
        return
        
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(decription='For when you wanna settle the score some other way')
async def choose(msg, *choices: str):
    # chooses between multiple choices
    await msg.channel.send(random.choice(choices))
@bot.command()
async def repeat(msg, times: int, content: str):
    #repeats a message multiple times.
    for i in range(times):
        await msg.channel.send(content)

@bot.command()
async def leave(msg):
    channel = msg.message.author.voice.channel
    voice = get(bot.voice_clients, guild=msg.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await msg.channel.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await msg.channel.send("Don't think I am in a voice channel")

@bot.command()
async def play(msg, url: str):
    song_loc = os.path.isfile("song.mp3")
    try:
        if song_loc:
            os.remove("song.mp3")
            print("Removed previos song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await msg.channel.send("ERROR: Music playing failed")
        return
    await msg.channel.send("Getting everything ready now")

    voice =  get(bot.voice_clients, guild=msg.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now \n")
        ydl.download([url])
    
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
    name_n = name.rsplit("-", 2)
    await msg.channel.send(f"Playing {name_n[0]}")
    print("playing\n")
@bot.group()
async def cool(msg):
    # says if a user is cool
    if msg.invoked_subcommand is None:
        await msg.channel.send("No, {0.subcommand_passed} is not cool".format(msg))
#hi user
@bot.command()
async def hi(ctx):
    await ctx.send("こんにちは, {}".format(ctx.author.name))

# ban user
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(msg, member: discord.Member = None, reason = None):
    if reason == None:
        await msg.channel.send(f"Woah {msg.author.mention}, Make sure you provide a reason!")
    else:
        message_ok = f"You have been banned from {msg.guild.name} for {reason}"
        await member.send(message_ok)
        await member.ban(reason=reason)

# unbans  user
@bot.command(pass_context=True)
async def join(msg):
    channel = msg.author.voice.channel
    await channel.connect()
@bot.command()
async def server_stats(msg):
    online = 0
    idle = 0
    offline = 0
    sentdex_guild = bot.get_guild(704422919706509445)
    
    for i in sentdex_guild.members:
        if str(i.status) == "online":
            online += 1
        if str(i.status) == "offline":
            offline += 1
        else:
            idle += 1
    embed = discord.Embed(title="Server stats", color=0x00ff00)
    embed.add_field(name="Number of members: ", value=f"{sentdex_guild.member_count}", inline=True)
    embed.add_field(name="online: ", value=f"{online}", inline=True)
    embed.add_field(name="offline: ", value=f"{offline}", inline=True)
    embed.add_field(name="idle: ", value=f"{idle}", inline=True)
    await msg.channel.send(embed=embed)
@bot.command()
async def clean(msg, count: int):
    # fix count delete commands
    if count <= 100:
        await msg.channel.purge(limit=count+1)
    else:
        await msg.send("you can delete only 100 messages at a time")
@cool.command(name='bot')
async def _bot(msg):
    # is the bot cool
    await msg.send("Yes, the bot is cool")


bot.run('NzIxNjU2MTI4NTU1MDU3MTgy.XvEDvg.9F2ozJT-Gf3C5R1ier9OJrKAcCM')
