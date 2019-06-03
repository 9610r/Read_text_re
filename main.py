import discord
from discord.ext import commands
import asyncio
import os
import subprocess
import ffmpeg
from voice_generator import creat_WAV_file_for_
#from test1 import talk

client = commands.Bot(command_prefix='.')
voice_client = None


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

'''
@client.command()
async def join(ctx):
    voice_channel = discord.utils.get(ctx.guild.channels, id=ctx.author.voice.channel.id)
    print(ctx.voice_client)
    await voice_channel.connect()
'''

@client.command()
async def join(ctx):
    # 送信者のVCを取得
    vc = ctx.author.voice.channel
    # Botが既に他のVCに参加しているか
    if ctx.voice_client:
        # 参加している場合は移動
        await ctx.voice_client.move_to(vc)
    else:
        # 参加していない場合はVCに接続
        await vc.connect()

@client.command()
async def start(ctx):
    vc = ctx.author.voice.channel
    ctx.voice_client.play(discord.FFmpegPCMAudio('output.wav'))

@client.command()
async def bye(ctx):
    await ctx.voice_client.disconnect()

@client.event
async def on_message(message):
    if message.content.startswith('.'):
        pass

    else:
        print(message.content)
        creat_WAV_file_for_(message.content)
        #talk(message.content)
        #voice_channel = message.author.voice.channel
        #voice_client = await voice_channel.connect()
        source = discord.FFmpegPCMAudio("output.wav")
        message.guild.voice_client.play(source)
    await client.process_commands(message)







client.run("TOKEN")
