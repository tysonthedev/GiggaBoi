

queueDictionary = dict()

#remove next item from the list then 
def GetAndPopNextItem(guild):
    if guild in queueDictionary:
        if not queueDictionary[guild]:
            queueDictionary.pop(guild)
            return 0
        else:
            nextItem = queueDictionary[guild].pop(0)
            return nextItem
    else:
        return 0

def GetNextItem(guild):
    if guild in queueDictionary:
        if not queueDictionary[guild]:
            queueDictionary.pop(guild)
            return 0
        else:
            nextItem = queueDictionary[guild][0]
            return nextItem
    else:
        return 0

def Add(guild,songData):
    if guild in queueDictionary:
        queueDictionary[guild].append(songData)
    else:
        queueDictionary[guild] = [songData]
    print(queueDictionary[guild])

def Clear(guild):
    if guild in queueDictionary:
        queueDictionary[guild].clear()