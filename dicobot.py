import random
import youtube_dl
import discord
from discord.ext import commands


BOT_PREFIX = '!'
bot = commands.Bot(command_prefix=BOT_PREFIX)

players = {}



@bot.command(pass_context=True)
async def hello(context):
    await bot.say('Hello {}'.format(context.message.author.mention))


@bot.command()
async def pick(*choices : str):
    print(choices)
    await bot.say('{} picks {} !'.format(bot.user.name, random.choice(choices)))


@bot.command(pass_context=True)
async def clear(context, number=100):
    channel = context.message.channel
    bot_name = bot.user.name
    messages = []
    async for msg in bot.logs_from(channel, limit=int(number)):
        messages.append(msg)
    try:
        await bot.delete_messages(messages)
    except discord.Forbidden:
        await bot.say('{} does not have the permession to delete message in {} channel !'.format(bot_name, channel))
    except discord.errors.ClientException:
        await bot.say('{} will only delete from 2 to {} messages.'.format(bot_name, number))


@bot.command(pass_context=True)
async def join(context, destination_channel=None):
    if not destination_channel:
        voice_channel = context.message.author.voice.voice_channel
        if voice_channel is None:
            await bot.say('{} can not find {} in any voice channel !'.format(bot.user.name, context.message.author.mention))
        else:
            await bot.join_voice_channel(voice_channel)
    else:
        for chnl in context.message.server.channels:
            if chnl.name == destination_channel:
                channel = chnl
                break
        try:    
            await bot.join_voice_channel(channel)
        except discord.ext.commands.errors.CommandInvokeError:
            await bot.say('{} could not join voice channel {}...'.format(bot.user.name, destination_channel))


@bot.command(pass_context=True)
async def leave(context):
    server = context.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()


@bot.command(pass_context=True)
async def play(context, url):
    server = context.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


@bot.command(pass_context=True)
async def pause(context):
    id = context.message.server.id
    players[id].pause()


@bot.command(pass_context=True)
async def stop(context):
    id = context.message.server.id
    players[id].stop()


@bot.command(pass_context=True)
async def resume(context):
    id = context.message.server.id
    players[id].resume()



@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name='Observe Humans'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#bot.run(TOKEN)
