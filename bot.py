import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl
import random
import time

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
@bot.command(description='repeats the given word as many times as given')
async def repeat(msg, times: int, content: str):
    #repeats a message multiple times.
    for i in range(times):
        await msg.channel.send(content)

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
@bot.group()
async def cool(msg):
    # says if a user is cool
    if msg.invoked_subcommand is None:
        await msg.channel.send("No, {0.subcommand_passed} is not cool".format(msg))
#hi user
@bot.command(description='Send welcome message')
async def hi(msg):
    times = int(time.strftime('%H'))
    if times <= 12:
        await msg.channel.send("おはよう, {}".format(msg.author.name))
    elif times > 12 and times <= 17:
         await msg.channel.send("こんにちは, {}".format(msg.author.name))
    elif times > 17 and times <= 22:
         await msg.channel.send("こんばんは, {}".format(msg.author.name))
@bot.command(description='say goodbye')
async def bye(msg):
    await msg.channel.send("さよなら, {}".format(msg.author.name))
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

@bot.command(pass_context=True, description='join the voice channel')
async def join(msg):
    channel = msg.author.voice.channel
    await channel.connect()
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
async def ship(msg, member: discord.Member = None, member1: discord.Member = None):
    num = random.randint(0, 100)
    embed = discord.Embed(title="Test love")
    embed.add_field(name=f"{member.display_name} and {member1.display_name}", value=f"{num}%", inline=True)
    await msg.channel.send(embed=embed)

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
    embed.set_image(url="https://i.makeagif.com/media/2-05-2016/BrBZFm.mp4")
    await msg.channel.send(embed=embed)

bot.run('NzIxNjU2MTI4NTU1MDU3MTgy.Xvb6qg.OHVIjbTU6ax5IqbRg7kHIRnQ-Lg')