#Ths script connects all the different scripts in the Nova engine

from AudioTranscription import DetectHotword, Initialize as HotwordInit
from SpeechSynthesis import SpeakStream, SpeakDirect, SpeakOffline, Initialize as SpeechInit
from LanguageModelInteraction import PromptLanguageModelAPI, PromptLanguageModelLocal, LLMStreamProcessor, Initialize as LangInit
import ConfigInteraction
import requests
import os
import ModuleManager
import json
from datetime import datetime
from Helpers import suppress_output_decorator, suppress_output
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import time
from queue import Queue

langFile = ConfigInteraction.GetLanguageFile()

conversation = []

userName = ConfigInteraction.GetSetting("Name")
language = ConfigInteraction.GetSetting("Language")
version = ConfigInteraction.GetManifest()["version"]
offlineMode = ConfigInteraction.GetSetting("OfflineMode")

hiddenSystemPromt = f"""You keep your answers as short as possible. You always use the metric system. You use the date format dd.mm.yyyy.
You only mention the date and time if specifically asked to do so. You speak in the following language: {language}.
You never make up information. You never promise an alternative solution if a module fails to execute.
You do not use special characters, like '-', '/' etc. Your response will be read out by a text-to-speech system. For that to work,
you use the following guidelines:.
01.01.1970 becomes 'First of January. 19 70'. 32°C becomes '32 degrees Celcius'. 12:31 becomes '12:31 o'clock'."""

systemPrompt = ConfigInteraction.GetSetting("Behaviour") + " " + hiddenSystemPromt

useConsole = True
runHotwordDetection = True

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
        CallLanguageModel("Text", True)


def CallLanguageModel(modality, speak):
    conversationWithInfo = conversation.copy()
    conversationWithInfo.append({"role": "system", "content": "The date is " + datetime.now().strftime("%d/%m/%Y") + " The time is " + datetime.now().strftime("%H:%M")})
    conversationWithInfo.append({"role": "system", "content": f"The name of the user is {userName}."})
    
    if (modality == "Text"):
        if (offlineMode == "False"):
            LLMresponse = PromptLanguageModelAPI(conversationWithInfo, speak) #If speak then stream to improve latency
        else:
            LLMresponse = PromptLanguageModelLocal(conversationWithInfo)
    elif (modality == "Audio"):
        pass
    elif (modality == "Image"):
        pass
    elif (modality == "Video"):
        pass
    
    processor = LLMStreamProcessor()

    if (offlineMode == "False" and speak):
        SpeakStream(processor.ExtractData(LLMresponse))
        response, function_calls = processor.GetData()
    elif (offlineMode == "True" and speak):
        response = LLMresponse['choices'][0]['message']['content'].replace("assistant", "")#Temporary fix for strange model behaviour
        function_calls = []
        SpeakOffline(response)
    elif (offlineMode == "Mixed" and speak):
        response = LLMresponse['choices'][0]['message']['content'].replace("assistant", "")#Temporary fix for strange model behaviour
        function_calls = []
        SpeakDirect(response)

    if (not speak and offlineMode == "False"): #Extract the response seperatly when not speaking the answer
        response = LLMresponse.choices[0].message.content
        function_calls = []
    elif (not speak and (offlineMode == "True" or offlineMode == "Mixed")):
        response = LLMresponse['choices'][0]['message']['content'].replace("assistant", "")#Temporary fix for strange model behaviour
        function_calls = []


    for call in function_calls:
        if (useConsole):
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
        CallLanguageModel("Text", True)
    else:
        if (useConsole):
            print(langFile["Misc"][1] + " " + response + "\n")
        AddToConversation(1, response, None, False)

    return response

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

    if (offlineMode == "True"): #If using the local LLM, inform that modules are unavailable in the current version
        print(langFile["Interface"][8] + " offline. " + langFile["Interface"][9])
    elif (offlineMode == "Mixed"):
        print(langFile["Interface"][8] + " mixed. " + langFile["Interface"][9])
    else:
        print(langFile["Interface"][8] + " online.")

    validModules, invalidModules = ModuleManager.ScanModules()

    if (validModules == 1):
        print(str(validModules) + " " + langFile["Status"][7])
    else:
        print(str(validModules) + " " + langFile["Status"][8])

    if (invalidModules > 0):
        print(str(invalidModules) + " " + langFile["Status"][9])

    print("\n" + langFile["Interface"][10])
    
def Initialize():
    if (useConsole):
        print("> " + langFile["Status"][0])

    HotwordInit()
    LangInit()
    SpeechInit()

    if (ConfigInteraction.GetSetting("OfflineMode") == "False" and useConsole): #TODO: Switch to offline if APIs can't be reached or an API key is missing
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

    if useConsole:
        print("> " + langFile["Status"][12])
        ClearConsole()
        PrintHeader()

def DequeueTask(task):
    global conversation
    
    match task["task"]:
        case "Exit":
            exit()
        case "GetConversation":
            return conversation
        case "AddToConversation":
            for param in task["parameters"]:
                conversation.append(param)
            return None
        case "SetConversation":
            conversation = task["parameters"]
            return None
        case "RunInferenceWithTTS":
            CallLanguageModel("Text", True)
            return None
        case "RunInferenceTextOnly":
            return CallLanguageModel("Text", False)
        case "Speak":
            SpeakDirect(task["parameters"][0])
    

def IdleLoop(tasks, results):
    while True:
        while not tasks.empty(): #Do everything the API has commanded to do before running another hotword check
            results.put(DequeueTask(tasks.get()))
        
        if (runHotwordDetection):
            transcription = DetectHotword()
            if (transcription != None):
                if (useConsole):
                    print(langFile["Misc"][0] + " " + transcription + "\n")
                AddToConversation(0, transcription, None, True)

def StartFromAPI(novaStatus, detectHotword, taskQueue, resultQueue):
    global useConsole
    global runHotwordDetection
    useConsole = False
    runHotwordDetection = detectHotword
    
    novaStatus[0] = 2
    Initialize()
    novaStatus[0] = 1
    IdleLoop(taskQueue, resultQueue)

def Start():
    Initialize()
    IdleLoop(Queue(maxsize=0), Queue(maxsize=0))