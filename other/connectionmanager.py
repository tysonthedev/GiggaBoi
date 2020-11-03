from asyncio.windows_events import NULL
import os
import discord
from discord.client import Client
from discord.enums import Enum
from discord.ext.commands.context import Context
from discord.voice_client import VoiceClient
import discord.utils
from discord import guild
from enum import Enum

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class ConnectionStatus(Enum):
    alreadyConnected = 1
    connectedNow = 2
    connectedToAnotherChannel = 3
    userNotConnected = 4
    disconnectedNow = 5

async def connect(client:Client, ctx:Context, forceConnect):
    for voiceClient in client.voice_clients:
        #if true this means that we have found the correct server the message was sent from
        if voiceClient.guild == ctx.author.guild:
            if forceConnect:
                    targetChannel = ctx.author.voice.channel
                    voiceClient = await targetChannel.connect()
                    return (ConnectionStatus.connectedNow,voiceClient)
            if ctx.author.voice == None:
                print("User isn't connected to a voice channel")
                return (ConnectionStatus.userNotConnected,NULL)
            elif ctx.author.voice.channel == voiceClient.channel:
                print("already connected")
                return (ConnectionStatus.alreadyConnected,voiceClient)
            elif ctx.author.voice.channel != voiceClient.channel:
                return (ConnectionStatus.connectedToAnotherChannel,voiceClient)
    targetChannel = ctx.author.voice.channel
    voiceClient = await targetChannel.connect()
    return (ConnectionStatus.connectedNow, voiceClient)

async def disconnect(client:Client, ctx:Context, forceDisconnect):
    for voiceClient in client.voice_clients:
            if voiceClient.guild == ctx.author.guild:
                if forceDisconnect:
                    await voiceClient.disconnect()
                    return (ConnectionStatus.disconnectedNow, NULL)
                elif ctx.author.voice == None:
                    print("User isn't connected to a voice channel")
                    return (ConnectionStatus.userNotConnected, NULL)
                elif ctx.author.voice.channel != voiceClient.channel:
                    print("connected to another voice channel")
                    return (ConnectionStatus.connectedToAnotherChannel, voiceClient)
                else:
                    await voiceClient.disconnect()
                    return (ConnectionStatus.disconnectedNow, NULL)

async def closeAllConnection(client:Client):
    print("Killing All Connections!")
    for voiceClient in client.voice_clients:
        print("Killed Connection")
        await voiceClient.disconnect()
    
def getVoiceClient(client:Client, ctx:Context):
    for voiceClient in client.voice_clients:
        if voiceClient.guild == ctx.author.guild:
            if ctx.author.voice == None:
                print("User isn't connected to a voice channel")
                return NULL
            elif ctx.author.voice.channel != voiceClient.channel:
                print("connected to another voice channel")
                return NULL
            else:
                return voiceClient