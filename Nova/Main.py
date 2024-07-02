#Ths script connects all the different scripts in the Nova engine

from AudioTranscription import DetectHotword
from SpeechSynthesis import TTS
from LanguageModelInteraction import PromptLanguageModel, LLMStreamProcessor
import ConfigInteraction
import requests
import os

#This is the array that stores the entire conversation
conversation = []

adressation = ConfigInteraction.GetSetting("Adressation")
language = ConfigInteraction.GetSetting("Language")
version = ConfigInteraction.GetManifest()["version"]

hiddenSystemPromt = f"Keep your answers as short as possible. Always use the metric system. Never use the imperial system. Adress the user as {adressation} where applicable. Speak in the following language: {language}. Never make up information. If you do not know a piece of information, attempt to find out the information. If that is not possible, admit that you do not know the information. If asked to calculate something, do not provide the calculation, just provide the answer. Do not use special characters, like '-', '/' etc."

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
    #Call GPT. It is put into a try-except block to cath potential errors when calling the API.    
    try:
        LLMresponse = PromptLanguageModel(conversation)
    except Exception as e:
        print("An error occured when communicating with the Groq API:\n" + str(e))
        return
    
    processor = LLMStreamProcessor()

    TTS(processor.ExtractData(LLMresponse))

    response, function_calls = processor.GetData()

    print("Response: " + response)

    AddToConversation(1, response, None, False)


def StartHotwordDetection():
    while True:
        transcription = DetectHotword()

        if (transcription != None):
            print("Hotword detected: " + transcription)
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
    print(f"Nova AI Assistant (Version {version}). Developed by Julian")
    print("")
    print("Loaded behaviour: " + ConfigInteraction.GetSetting("Behaviour"))

    print("Starting the Hotword detection...\n")
    
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