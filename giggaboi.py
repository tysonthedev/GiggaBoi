from asyncio.windows_events import NULL
from operator import truediv
import time
import discord
from discord import guild
from discord.ext.commands.context import Context
from discord.player import FFmpegAudio, FFmpegPCMAudio
from discord.voice_client import VoiceClient
import nacl
import json
import os
from other import audiomanager
from discord import channel
from discord.channel import VoiceChannel
from discord.message import Message
from discord.ext.commands import Bot
from discord.ext.commands import command
from discord import Client
from discord import File
from other import messagemanager
from other import connectionmanager
from other.audiomanager import GetLocalLibraryList
from other.connectionmanager import ConnectionStatus
from other import queuemanager

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
configFile = open(os.path.join(__location__, 'config.json'))
jsonConfig = json.loads(configFile.read())
TOKEN = jsonConfig['TOKEN']
client = Bot(command_prefix='\\')

@client.event
async def on_ready():
        print('Logged in as ' + str(client.user))

@client.event
async def on_message(message:discord.Message):
    await client.process_commands(message)
    print('Message from:' + str(message.author) + " content:" + str(message.content) + " channelId:" + str(message.channel.id))
    if message.author == client.user:
        return
    else:
    #this will all eventually move to messagemanager
        print (message.content.upper())
        if 'POTATO' in message.content.upper():
            await message.channel.send(messagemanager.ReplaceAllOccurences(message.content,'potato','PotAHto'))
        if "TOMATO" in message.content.upper():
            await message.channel.send("TomAHto")        
        if 'BITCOIN' in message.content.upper():
            await gilfoylesayshi(message.author)   

@client.command()
async def connect(ctx: Context):
    await connectionmanager.connect(client,ctx, False)

@client.command()
async def disconnect(ctx:Context):
    await connectionmanager.disconnect(client,ctx, False)
    queuemanager.Clear(str(ctx.guild.id))
    
@client.command()
async def killconnections(ctx):
    await connectionmanager.closeAllConnection(client)

@client.command(name="library",help="Gives a file listing the local library")
async def library(ctx:Context):
    await ctx.channel.send("Library List",file=File(open(audiomanager.GetLocalLibraryList(str(ctx.guild.id)),"rb"),"library_list.txt"))

@client.command()
async def play(ctx, *,args):
    resultTuple = await connectionmanager.connect(client,ctx, False)
    voiceClient = resultTuple[1]
    connectionStatus = resultTuple[0]

    if connectionStatus == ConnectionStatus.connectedNow:
        voiceClient.play(audiomanager.PlayAudioClip(args,str(ctx.guild.id)),after=lambda x: playNextSong(voiceClient,ctx))
    elif connectionStatus == ConnectionStatus.alreadyConnected:
        if voiceClient.is_playing() or voiceClient.is_paused():
            print("bot is already playing audio will add song to the queue")
            queuemanager.Add(str(ctx.guild.id),args)
        else:            
            voiceClient.play(audiomanager.PlayAudioClip(args, str(ctx.guild.id)),after=lambda x: playNextSong(voiceClient,ctx))
    elif connectionStatus == ConnectionStatus.connectedToAnotherChannel:
        if voiceClient.is_playing() == False and voiceClient.is_paused() == False:
            print("bot is connected to another channel and isn't playing audio \nIt will now disconnect and connect to the correct voice channel!")
            await connectionmanager.disconnect(client,ctx, True)
            resultTuple = await connectionmanager.connect(client,ctx, True)
            voiceClient = resultTuple[1]
            connectionStatus = resultTuple[0]
            voiceClient.play(audiomanager.PlayAudioClip(args,str(ctx.guild.id)),after=lambda x: playNextSong(voiceClient,ctx))
        else:
            print("bot is currently connected to another channel and playing audio \n Audio will not be played in this channel and won't be added to the queue")

@client.command()
async def skip(ctx):
    connectionmanager.getVoiceClient(client,ctx).stop()

@client.command()
async def pause(ctx):
    connectionmanager.getVoiceClient(client,ctx).pause()

@client.command()
async def resume(ctx):
    connectionmanager.getVoiceClient(client,ctx).resume()

@client.command()
async def queue(ctx):
    await ctx.send(queuemanager.queueDictionary[str(ctx.guild.id)])

@client.command()
async def stop(ctx):
    queuemanager.Clear(str(ctx.guild.id))
    connectionmanager.getVoiceClient(client,ctx).stop()

def playNextSong(voiceClient,ctx):
    print("PLAYING NEXT SONG FUNCTION")
    if queuemanager.GetNextItem(str(ctx.guild.id)) == NULL:
        print("QUEUE FOR GUILD:" + str(str(ctx.guild.id)) + " IS EMPTY")
    else:
        print("PLAYING NEXT SONG")
        voiceClient.play(audiomanager.PlayAudioClip(queuemanager.GetAndPopNextItem(str(ctx.guild.id)),str(ctx.guild.id)),after=lambda x: playNextSong(voiceClient,ctx))
#will eventually move to messagemanager
async def gilfoylesayshi(user:discord.user):
    for voiceClient in client.voice_clients:
        if voiceClient.guild == user.guild:
            if user.voice == None or user.voice.channel != voiceClient.channel:
                return
            else:
                voiceClient.play(audiomanager.GetLocalAudioClip('gilfoylesayshi'))

client.run(TOKEN)
