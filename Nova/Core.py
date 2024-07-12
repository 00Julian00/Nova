#Ths script connects all the different scripts in the Nova engine

from AudioTranscription import DetectHotword
from SpeechSynthesis import SpeakStream, SpeakDirect, SpeakOffline
from LanguageModelInteraction import PromptLanguageModelAPI, PromptLanguageModelLocal, LLMStreamProcessor
import ConfigInteraction
import requests
import os
import ModuleManager
import json
from datetime import datetime
from Helpers import suppress_output_decorator, suppress_output

langFile = ConfigInteraction.GetLanguageFile()

conversation = []

userName = ConfigInteraction.GetSetting("Name")
language = ConfigInteraction.GetSetting("Language")
version = ConfigInteraction.GetManifest()["version"]
offlineMode = ConfigInteraction.GetSetting("OfflineMode")

hiddenSystemPromt = f"You keep your answers as short as possible. You always use the metric system. You use the date format dd.mm.yyyy. You only mention the date and time if specifically asked to do so. You speak in the following language: {language}. You never make up information. You never promise an alternative solution if a module fails to execute. You do not use special characters, like '-', '/' etc."

systemPrompt = ConfigInteraction.GetSetting("Behaviour") + " " + hiddenSystemPromt

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def AddToConversation(type, content, functionName, PromptLanguageModel):
    if(type == 0): #User
        conversation.append({"role": "user", "content": content})
    elif(type == 1): #AI
        conversation.append({"role": "assistant", "content": content})
    elif(type == 2): #Function
        conversation.append({"role": "function", "name": functionName, "content": content})
    elif(type == 3): #System
        conversation.append({"role": "system", "content": content})

    if(PromptLanguageModel):
        CallLanguageModel()


def CallLanguageModel():
    try:
        conversationWithInfo = conversation.copy()
        conversationWithInfo.append({"role": "system", "content": "The date is " + datetime.now().strftime("%d/%m/%Y") + " The time is " + datetime.now().strftime("%H:%M")})
        conversationWithInfo.append({"role": "system", "content": f"The name of the user is {userName}."})
        
        with suppress_output():
            if (offlineMode == "False"):
                LLMresponse = PromptLanguageModelAPI(conversationWithInfo)
            else:
                LLMresponse = PromptLanguageModelLocal(conversationWithInfo)

    except Exception as e:
        print("An error occured when communicating with the Groq API:\n" + str(e))
        return
    
    processor = LLMStreamProcessor()

    if (offlineMode == "False"):
        SpeakStream(processor.ExtractData(LLMresponse))
        response, function_calls = processor.GetData()
    else:
        response = LLMresponse[0]['generated_text']
        function_calls = []
        SpeakOffline(response)


    for call in function_calls:
        if (str(call.function.arguments) == "{}"):
            print(langFile["Misc"][1] + " " + langFile["Status"][3] + " " + str(call.function.name) + " " + langFile["Status"][4] + "\n")
        else:
            print(langFile["Misc"][1] + " " + langFile["Status"][3] + " " + str(call.function.name) + " " + langFile["Status"][5] + str(call.function.arguments) + "\n")

        result = ModuleManager.CallFunction(call.function.name, json.loads(call.function.arguments))
        if result == True:
            AddToConversation(2, "The module has been executed sucessfully.", str(call.function.name), False)
        elif result == False:
            AddToConversation(2, "The model failed to execute. Try again later.", str(call.function.name), False)
        else:
            AddToConversation(2, result, str(call.function.name), False)

    if (len(function_calls) > 0):
        CallLanguageModel()
    else:
        print(langFile["Misc"][1] + " " + response + "\n")
        AddToConversation(1, response, None, False)


def StartHotwordDetection():
    while True:
        transcription = DetectHotword()

        if (transcription != None):
            print(langFile["Misc"][0] + " " + transcription + "\n")
            AddToConversation(0, transcription, None, True)

def PingGroq():
    url = "https://api.groq.com"

    try:
        requests.head(url, headers={})
    except:
        return False

    return True

def PingElevenlabs():
    url = "https://elevenlabs.io"

    try:
        requests.head(url, headers={})
    except:
        return False

    return True

def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def PrintHeader():
    print(langFile["Interface"][7] + " (" + langFile["Interface"][5] + " " + version + "). " + langFile["Interface"][1] + "\n")
    print(langFile["Status"][6] + " " + ConfigInteraction.GetSetting("Behaviour"))
    if (offlineMode == "True"):
        print(langFile["Interface"][8])
    else:
        print(langFile["Interface"][9])

    validModules, invalidModules = ModuleManager.ScanModules()

    if (validModules == 1):
        print(str(validModules) + " " + langFile["Status"][7])
    else:
        print(str(validModules) + " " + langFile["Status"][8])

    if (invalidModules > 0):
        print(str(invalidModules) + " " + langFile["Status"][9])

    print("\n" + langFile["Interface"][10])
    
def Initialize():
    print("> " + langFile["Status"][0])

    if (ConfigInteraction.GetSetting("OfflineMode") == "False"): #TODO: Switch to offline if APIs can't be reached or an API key is missing
        if (PingGroq()):
            print("> " + langFile["Status"][10])
        else:
            print(langFile["Errors"][11])
            exit()

        if (PingElevenlabs()):
            print("> " + langFile["Status"][11])
        else:
            print(langFile["Errors"][12])
            exit()

    AddToConversation(3, systemPrompt, None, False)
    print("> " + langFile["Status"][12])

    ClearConsole()
    PrintHeader()


Initialize()

StartHotwordDetection()