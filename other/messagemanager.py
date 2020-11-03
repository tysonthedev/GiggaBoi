import os
import discord

#this class will be able to do all of the special functions such as playing audio, or replacing text when a certain phrase is said randomly in the server
def ReplaceAllOccurences(input:str, substringToReplace:str, substringSubstituion:str):
    output = input
    upperCaseInput = input.upper()
    
    i=0
    stepbackAmount = len(substringSubstituion) - len(substringToReplace)
    stepCount = 0
    while i < len(upperCaseInput):
        foundIndex = upperCaseInput.find(substringToReplace.upper(),i)
        if foundIndex != -1:
            upperCaseInput = upperCaseInput.replace(substringToReplace.upper(),substringSubstituion,1)
            i = foundIndex + len(substringToReplace) + stepbackAmount
            output = output[0:foundIndex] + substringSubstituion + output[foundIndex + len(substringToReplace):len(output)]
        else:
            break
    return(output)