import discord
from discord.ext import commands
import random

description = '''ALSQ bot sample '''

bot = commands.Bot(command_prefix='$', description=description)

@bot.event
async def on_ready():
    print("Logged in as {} {}".format(bot.user.name, bot.user.id))
    print("---------")

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
async def choose(ctx, *choices: str):
    # chooses between multiple choices
    await ctx.send(random.choice(choices))
@bot.command()
async def repeat(ctx, times: int, content: str):
    #repeats a message multiple times.
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    # says when a member joined.
    await ctx.send("{0.name} joined in {0.joined_at}".format(member))

@bot.group()
async def cool(ctx):
    # says if a user is cool
    if ctx.invoked_subcommand is None:
        await ctx.send("No, {0.subcommand_passed} is not cool".format(ctx))

@bot.command()
async def hi(ctx):
    await ctx.send("こんにちは, {}".format(ctx.author.name))

@bot.command(pass_context=True)
async def nick(ctx, member: discord.Member, nickname):
    await member.edit(nick=nickname)
    await ctx.send("changed {member.name}'s nickname to {nickname}")

@bot.command()
async def clean(ctx, count: int):
    # fix count delete commands
    if count <= 100:
        await ctx.channel.purge(limit=count+1)
    else:
        await ctx.send("you can delete only 100 messages at a time")
@cool.command(name='bot')
async def _bot(ctx):
    # is the bot cool
    await ctx.send("Yes, the bot is cool")

bot.run('NzIxNjU2MTI4NTU1MDU3MTgy.XvEDvg.9F2ozJT-Gf3C5R1ier9OJrKAcCM')