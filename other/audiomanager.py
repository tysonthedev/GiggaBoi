import os
import discord
from discord.ext.commands.context import Context
import youtube_dl
from youtube_dl.YoutubeDL import YoutubeDL
import youtube_dl.downloader
import shutil

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(__location__)
libraryFilePath = os.path.dirname(__location__) + '\locallibrary'

def PlayAudioClip(whateverAudioClip, serverGuild):
    if '/' in whateverAudioClip:
        return GetYoutubeAudioClip(whateverAudioClip, serverGuild)
    else:
        return GetLocalAudioClip(whateverAudioClip, serverGuild)

def GetLocalLibraryList(serverGuild):
    directoryList = os.listdir(libraryFilePath)
    listFile = open(__location__ + "\\" + serverGuild + "locallibrarylist.txt", "w")
    for filename in directoryList:
        listFile.write(filename + '\n')
    listFile.close()
    return listFile.name

async def AddToLocal(discordAttachment:discord.Attachment, nameOfFile):
    await discordAttachment.save(libraryFilePath + "\\" + nameOfFile)
    return

async def RemoveFromLocal(nameOfFile):
    if(os.path.exists(libraryFilePath + "\\" + nameOfFile + ".mp3")):
        os.remove(libraryFilePath + "\\" + nameOfFile + ".mp3")
    return

def GetLocalAudioClip(searchTerm, serverGuild):
    tempFilePath = os.path.dirname(__location__) + '\\' + serverGuild + '.mp3'
    directoryList = os.listdir(libraryFilePath)
    for libraryItem in directoryList:
        if(searchTerm.upper() == libraryItem[0:len(libraryItem) - 4].upper()):
                if(os.path.exists(tempFilePath)):
                    os.remove(tempFilePath)
                shutil.copyfile(libraryFilePath + '\\' + libraryItem,tempFilePath)
                return(discord.FFmpegPCMAudio(tempFilePath))
    return(GetYoutubeAudioClip(searchTerm, serverGuild))
    return discord.FFmpegPCMAudio(libraryFilePath + '\\' + 'error.mp3')

def GetYoutubeAudioClip(url, serverGuild):
    tempFilePath = os.path.dirname(__location__) + '\\' + serverGuild + '.mp3'
    ytdlOptions = {
        'format': 'bestaudio',
        'extractaudio': True,
        'outtmpl': tempFilePath,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
    
    
    if(os.path.exists(tempFilePath)):
        os.remove(tempFilePath)
    else:
        print("file doesn't exist")
    YoutubeDL(ytdlOptions).download([url])
    print(url)
    return(discord.FFmpegPCMAudio(tempFilePath))