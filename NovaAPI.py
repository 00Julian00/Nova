import os
import json
import sys
import multiprocessing
import time
import threading
from queue import Queue

current_dir = os.path.dirname(os.path.abspath(__file__))
CorePath = os.path.join(current_dir, 'Nova')
sys.path.append(CorePath)

from CheckForValidInput import CheckForValidInput
import KeyManager
import Core

novaThread = None
novaStatus = [0]
detectHotword = True

tasks = Queue(maxsize=0)
results = Queue(maxsize=0)

def SetSetting(name, value):
    if (CheckForValidInput(name, value) == True):
        with open(os.path.join(CorePath, 'Configs', 'NovaSettings.config'), 'r+') as file:
            settings = json.load(file)
            try:
                settings[name] = value
                file.seek(0)
                file.truncate()
                file.write(json.dumps(settings, indent=4))
            except:
                raise Exception("Setting does not exist.")
    else:
        raise TypeError("Value of setting is invalid.")
    
def GetSetting(name):
    with open(os.path.join(CorePath, 'Configs', 'NovaSettings.config'), 'r') as file:
        settings = json.load(file)
        try:
            return settings[name]
        except:
            raise Exception(f"{name} was not found.")
        
def SetKey(name, value):
    KeyManager.SetKey(name, value)

def GetKey(name):
    try:
        return KeyManager.GetKey(name)
    except:
        raise Exception(f"{name} was not found.")
    
def StartNova(hotword):
    global novaStatus
    global novaThread
    global tasks
    global results
    global detectHotword

    detectHotword = hotword

    #Reset the queues, in case there is leftover data in them
    tasks = Queue(maxsize=0)
    results = Queue(maxsize=0)

    novaThread = threading.Thread(target=Core.StartFromAPI, args=(novaStatus, detectHotword, tasks, results,))
    novaThread.start()

def StopNova():
    global novaThread
    global novaStatus

    novaStatus = 0
    tasks.put({"task": "Exit", "parameters": []})

def GetStatus():
    return novaStatus[0]

def AddToConversation(role, content):
    tasks.put({"task": "AddToConversation", "parameters": [{"role": role, "content": content}]})
    results.get()

def GetConversation():
    tasks.put({"task": "GetConversation", "parameters": []})
    return results.get()

def SetConversation(conversation):
    tasks.put({"task": "SetConversation", "parameters": conversation})
    results.get()

def RunWithSpeech():
    tasks.put({"task": "RunInferenceWithTTS", "parameters": []})
    results.get()

def Run():
    tasks.put({"task": "RunInferenceTextOnly", "parameters": []})
    return (results.get())

def ToggleHotwordDetection(detect):
    global detectHotword
    detectHotword = detect

def Speak(text):
    tasks.put({"task": "Speak", "parameters": [text]})
    results.get()