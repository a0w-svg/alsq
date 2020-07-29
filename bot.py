import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import random
import time
import emoji

description = '''ALSQ bot sample '''
bot = commands.Bot(command_prefix='$', description=description)

@bot.event
async def on_ready():
    print("Logged in as {} {}".format(bot.user.name, bot.user.id))
    print("---------")

@bot.command(pass_context=True)
async def nick(ctx, member: discord.Member = None, nick: str = None):
     if nick == None:
        ctx.send("please add  nick")
     if member == None:
        await member.edit(nick=nick)
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
@bot.command(description='repeats the given word as many times as given')
async def repeat(msg, times: int, content: str):
    #repeats a message multiple times.
    for i in range(times):
        await msg.channel.send(content)
"""
@bot.command(description='leaves the voice channel')
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
"""
"""
@bot.command(description='Play music from youtube link')
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
            'preferredquality': '98',
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
    voice.source.volume = 0.7
    name_n = name.rsplit("-", 2)
    await msg.channel.send(f"Playing {name_n[0]}")
    print("playing\n")
 """
@bot.group()
async def cool(msg):
    # says if a user is cool
    if msg.invoked_subcommand is None:
        await msg.channel.send("No, {0.subcommand_passed} is not cool".format(msg))
#hi user
@bot.command(description='''Send welcome message 
                            up to 12  display おはよう (Good morning)
                            from 12 to 17 display こんにちは (Good afternoon) 
                            from 17 to 22 display こんばんは (Good evening)''')
async def hi(msg, member: discord.Member = None):
    times = int(time.strftime('%H'))
    message = None
    if member == None:
       message = msg.author.name
    else:
        message = member.mention
    if times <= 12:
        await msg.channel.send("おはよう, {}".format(message))
    elif times > 12 and times <= 17:
        await msg.channel.send("こんにちは, {}".format(message))
    elif times > 17 and times <= 22:
        await msg.channel.send("こんばんは, {}".format(message))

@bot.command(description='say goodbye')
async def bye(msg, member: discord.Member = None):
    if member == None:
        await msg.channel.send("さよなら, {}".format(msg.author.name))
    else:
        await msg.channel.send("さよなら, {}".format(member.mention))
# ban user
@bot.command(description='Ban user')
@commands.has_permissions(ban_members = True)
async def ban(msg, member: discord.Member = None, reason = None):
    if reason == None:
        await msg.channel.send(f"Woah {msg.author.mention}, Make sure you provide a reason!")
    else:
        message_ok = f"You have been banned from {msg.guild.name} for {reason}"
        await member.send(message_ok)
        await member.ban(reason=reason)
"""
@bot.command(description='paper, rock, scissors')
async def jkp(msg, chose: str = None):
    ls = ['paper', 'rock', 'scissors']
    a = random.choice(ls)
    if chose == None:
        await msg.channel.send("Wrong argument please type $jkp <rock, paper, scissors>, {}".format(msg.author.name))
    if a == 'paper' and chose == 'rock':
        await msg.channel.send("Bot chose paper, you lost")
    if a == 'rock' and chose == 'paper':
        await msg.channel.send("Bot chose rock, you winner")
    if a == 'scissors' and chose == 'rock':
        await msg.channel.send("Bot chose scissors, you winner")
    if a == 'rock' and chose == 'scissors':
        await msg.channel.send("Bot chose rock, you lost")
    if a == 'paper' and chose == 'scissors':
        await msg.channel.send("Bot chose paper, you winner")
    if a == 'scissors' and chose == 'paper':
        await msg.channel.send("Bot chose scissors, you lost")
"""
"""
@bot.command(pass_context=True, description='join the voice channel')
async def join(msg):
    channel = msg.author.voice.channel
    await channel.connect()
 """
@bot.command(description='display server stats')
async def server_stats(msg):
    online = 0
    idle = 0
    offline = 0
    sentdex_guild = bot.get_guild(726566631530168330)
    
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
@bot.command(description='delete max 100 messages')
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

@bot.command(description='Love test')
async def ship(msg, user: discord.Member = None, user2: discord.Member = None):
    val = random.randint(0, 100)
    if user == None or user2 == None:
        await msg.send("please type two members")
    else:
        if val <= 30:
            em = str(emoji.emojize(':broken_heart:'))
        if val > 30 and val <= 60:
            em = str(emoji.emojize(':blue_heart:'))
        if val > 60 and val <= 80:
            em = str(emoji.emojize(':two_hearts:'))
        if val > 80 and val <= 100:
            em = str(emoji.emojize(':cupid:'))
        embed = discord.Embed(title="Love test")
        embed.add_field(name="Your score:", value=f"{val}%")
        embed.add_field(name="Reaction", value=f"{em}")
        await msg.send(embed=embed)

@bot.command(description='marry user')
async def marry(msg, member: discord.Member):
    embed = discord.Embed(title="Marry")
    embed.add_field(name="all the best for a new way of life", value=f"{msg.author.name} married {member.display_name}")
    await msg.channel.send(embed=embed)

@bot.command(description='divorce')
async def divorce(msg, member: discord.Member):
    embed = discord.Embed(title="divorce")
    embed.add_field(name="Why did this happen? :(", value=f"{msg.author.name} got divorced {member.display_name}")
    await msg.channel.send(embed=embed)

@bot.command(description='send gif with bomb')
async def allahakbar(msg):
    embed = discord.Embed(title="gif with bomb")
    embed.set_image(url="https://media.discordapp.net/attachments/488103401545007105/727484372235845713/emote.gif")
    await msg.channel.send(embed=embed)

@bot.command(description='gif')
async def kill(msg):
    embed = discord.Embed(title="Kill you")
    embed.set_image(url="https://cdn.discordapp.com/emojis/708571810639380502.gif?v=1")
    await msg.channel.send(embed=embed)


bot.run('NzIxNjU2MTI4NTU1MDU3MTgy.XvshwA.RV3BfDx2FPP48_rNfd3EQT2rS9M')
