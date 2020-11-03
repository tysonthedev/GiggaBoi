import os
import discord
from discord.ext.commands.context import Context
import youtube_dl
from youtube_dl.YoutubeDL import YoutubeDL
import youtube_dl.downloader

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print(__location__)
libraryFilePath = os.path.dirname(__location__) + '\locallibrary'

def PlayAudioClip(whateverAudioClip):
    if '/' in whateverAudioClip:
        return GetYoutubeAudioClip(whateverAudioClip)
    else:
        return GetLocalAudioClip(whateverAudioClip)
def GetLocalLibraryList():
    directoryList = os.listdir(libraryFilePath)
    listFile = open(__location__ + "\locallibrarylist.txt", "w")
    for filename in directoryList:
        listFile.write(filename + '\n')
    listFile.close()
    return listFile.name

def GetLocalAudioClip(searchTerm):
    directoryList = os.listdir(libraryFilePath)
    for libraryItem in directoryList:
        if(searchTerm.upper() == libraryItem[0:len(libraryItem) - 4].upper()):
            return discord.FFmpegPCMAudio(libraryFilePath + '\\' + libraryItem)
    return discord.FFmpegPCMAudio(libraryFilePath + '\\' + 'error.mp3')
def GetYoutubeAudioClip(url):
    ytdlOptions = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': os.path.dirname(__location__) + '\\temp.mp3',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
    #ytdlOptions = {
    #    'format':'bestaudio/best',
    #    'outtmpl':os.path.dirname(__location__) + '\\temp.mp3',
    #    'postprocessors': 
    #        [{
    #            'key':'FFmpegExtractAudio',
    #            'preferredcodec':'mp3',
    #            'preferredquality':'0'
    #        }]
    #}
    if(os.path.exists(os.path.dirname(__location__) + '\\temp.mp3')):
        os.remove(os.path.dirname(__location__) + '\\temp.mp3')
    else:
        print("file doesn't exist")
    YoutubeDL(ytdlOptions).download([url])
    return(discord.FFmpegPCMAudio(os.path.dirname(__location__) + '\\temp.mp3', executable= os.path.dirname(__location__) + '\\ffmpeg/bin\\ffmpeg.exe'))