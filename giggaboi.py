from operator import truediv
import time
import discord
from discord import guild
from discord import message
from discord import permissions
from discord.ext import commands
from discord.ext.commands import has_permissions
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
permissionErrorMessage = "You don't have permission to run this command"

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
            message.aut
            await message.channel.send(messagemanager.ReplaceAllOccurences(message.content,'potato','PotAHto'))
        if "TOMATO" in message.content.upper():
            await message.channel.send(messagemanager.ReplaceAllOccurences(message.content,'tomato','TomAHto'))
        if 'BITCOIN' in message.content.upper():
            await gilfoylesayshi(message.author)

@client.command(name="connect",help="Connects GiggaBoi to the voice server you are in")
async def connect(ctx: Context):
    await connectionmanager.connect(client,ctx, False)

@client.command(name="disconnect",help="Disconnects GiggaBoi from the voice server you are in")
async def disconnect(ctx:Context):
    await connectionmanager.disconnect(client,ctx, False)
    queuemanager.Clear(str(ctx.guild.id))
    
@client.command(name="killconnections",help="(admins only) Kills all instances of GiggaBoi cross server")
@commands.has_permissions(administrator=True)
async def killconnections(ctx:Context):
    await connectionmanager.closeAllConnection(client)
@killconnections.error
async def killconnectionserror(ctx,error):
    await ctx.send(permissionErrorMessage)
@client.command(name="library",help="Gives a file listing the local library")
async def library(ctx:Context):
    await ctx.channel.send("Library List",file=File(open(audiomanager.GetLocalLibraryList(str(ctx.guild.id)),"rb"),"library_list.txt"))

@client.command(name="play", help="Plays audio. local file/link example:\play <name of file or url>. youtube search example: \play /<search>")
async def play(ctx:Context, *,args):
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

@client.command(name="skip", help="Skips current audio")
async def skip(ctx:Context):
    connectionmanager.getVoiceClient(client,ctx).stop()

@client.command(name="pause", help="Pauses current audio")
async def pause(ctx:Context):
    connectionmanager.getVoiceClient(client,ctx).pause()

@client.command(name="resume", help="Resumes current audio")
async def resume(ctx:Context):
    connectionmanager.getVoiceClient(client,ctx).resume()

@client.command(name="queue", help="Prints out the current queue(JSON)")
async def queue(ctx:Context):
    if(queuemanager.queueDictionary):
        if(str(ctx.guild.id) in queuemanager.queueDictionary):
            await ctx.send(queuemanager.queueDictionary[str(ctx.guild.id)])
            return
    await ctx.send("queue is empty")

@client.command(name="stop", help="Stops current audio and empties the queue")
async def stop(ctx:Context):
    queuemanager.Clear(str(ctx.guild.id))
    connectionmanager.getVoiceClient(client,ctx).stop()

@client.command(name="addattached", help="(admins only) Adds the mp3 file you attach to the local library with the title you give it. example: \\addattached <name you want to give it> and also attach your mp3")
@commands.has_permissions(administrator=True)
async def addattached(ctx:Context, * ,args ):
    if(ctx.message.attachments):
        if(".mp3" in ctx.message.attachments[0].filename):
            await audiomanager.AddToLocal(ctx.message.attachments[0],args + ".mp3")
        else:
            await ctx.send("please attach an mp3 file")
            return
    else:
        await ctx.send("please attach an mp3 file")
        return
    return
@addattached.error
async def addattachedError(ctx,error):
    await ctx.send(permissionErrorMessage)

#@client.command(name="addcurrent", help="(admins only) Adds the mp3 that is currently being placed to the local library with a title you give it. example: \\addcurrent <name you want to give it>")
#async def addcurrent(ctx:Context):
#    return

@client.command(name="removelocal", help="(admins only) Removes a local file from the local library example: \\removelocal <name of file to remove>")
@commands.has_permissions(administrator=True)
async def removelocal(ctx:Context,*,args):
    await audiomanager.RemoveFromLocal(args)
    return
@removelocal.error
async def removelocalError(ctx,error):
    await ctx.send(permissionErrorMessage)
def playNextSong(voiceClient,ctx):
    print("PLAYING NEXT SONG FUNCTION")
    if queuemanager.GetNextItem(str(ctx.guild.id)) == 0:
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
