#Ths script connects all the different scripts in the Nova engine

from AudioTranscription import DetectHotword
from SpeechSynthesis import TTS
from LanguageModelInteraction import PromptLanguageModel, LLMStreamProcessor
import ConfigInteraction
import requests
import os
import ModuleManager
import json
from datetime import datetime

#This is the array that stores the entire conversation
conversation = []

userName = ConfigInteraction.GetSetting("Name")
language = ConfigInteraction.GetSetting("Language")
version = ConfigInteraction.GetManifest()["version"]

hiddenSystemPromt = f"Keep your answers as short as possible. Always use the metric system. Use the date format dd.mm.yyyy. Only mention the date and time if specifically asked to do so. Speak in the following language: {language}. Never make up information. Never promise an alternative solution if a module fails to execute. Do not use special characters, like '-', '/' etc."

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
        LLMresponse = PromptLanguageModel(conversationWithInfo)
    except Exception as e:
        print("An error occured when communicating with the Groq API:\n" + str(e))
        return
    
    processor = LLMStreamProcessor()

    TTS(processor.ExtractData(LLMresponse))

    response, function_calls = processor.GetData()

    for call in function_calls:
        if (str(call.function.arguments) == "{}"):
            print("AI: Calling module " + str(call.function.name) + " with no parameters\n")
        else:
            print("AI: Calling module " + str(call.function.name) + " with parameters " + str(call.function.arguments) + "\n")

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
        print("AI: " + response + "\n")
        AddToConversation(1, response, None, False)


def StartHotwordDetection():
    while True:
        transcription = DetectHotword()

        if (transcription != None):
            print("User: " + transcription + "\n")
            AddToConversation(0, transcription, None, True)

def PingGroq():
    url = "https://api.groq.com"

    try:
        response = requests.head(url, headers={})
    except:
        return False

    return True

def PingElevenlabs():
    url = "https://elevenlabs.io"

    try:
        response = requests.head(url, headers={})
    except:
        return False

    return True

def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def PrintHeader():
    print(f"Nova AI Assistant (Version {version}). Developed by Julian.\n")
    print("Loaded behaviour: " + ConfigInteraction.GetSetting("Behaviour"))

    validModules, invalidModules = ModuleManager.ScanModules()

    if (validModules == 1):
        print(f"{validModules} Module is loaded.")
    else:
        print(f"{validModules} Modules are loaded.")

    if (invalidModules > 0):
        print(f"{invalidModules} Modules have an invalid file structure and could therefore not be loaded.")

    print("\nConversation history:")
    
def Initialize():
    print("> Booting...")

    if (PingGroq()):
        print("> Connection to Groq successful.")
    else:
        print("Failed to connect to Groq. Please check your internet connection.")
        exit()

    if (PingElevenlabs()):
        print("> Connection to Elevenlabs successful.")
    else:
        print("Failed to connect to Elevenlabs. Please check your internet connection.")
        exit()

    AddToConversation(3, systemPrompt, None, False)
    print("> Initialized Language Model.")

    ClearConsole()
    PrintHeader()


Initialize()

StartHotwordDetection()