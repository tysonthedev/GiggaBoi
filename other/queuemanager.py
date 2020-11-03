
from asyncio.windows_events import NULL

queueDictionary = dict()

#remove next item from the list then 
def GetAndPopNextItem(guild):
    if guild in queueDictionary:
        if not queueDictionary[guild]:
            queueDictionary.pop(guild)
            return NULL
        else:
            nextItem = queueDictionary[guild].pop(0)
            return nextItem
    else:
        return NULL

def GetNextItem(guild):
    if guild in queueDictionary:
        if not queueDictionary[guild]:
            queueDictionary.pop(guild)
            return NULL
        else:
            nextItem = queueDictionary[guild][0]
            return nextItem
    else:
        return NULL

def Add(guild,songData):
    if guild in queueDictionary:
        queueDictionary[guild].append(songData)
    else:
        queueDictionary[guild] = [songData]
    print(queueDictionary[guild])

def Clear(guild):
    if guild in queueDictionary:
        queueDictionary[guild].clear()