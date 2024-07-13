import os
import json
import sys
import multiprocessing
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
CorePath = os.path.join(current_dir, 'Nova')
sys.path.append(CorePath)

from CheckForValidInput import CheckForValidInput
import KeyManager
import Core

isNovaRunning = multiprocessing.Value('i', 0) #0 = Not running, 1 = Running, 2 = Currently starting
NovaProcess = multiprocessing.Process(target=Core.StartFromAPI, args=(isNovaRunning,))

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
            raise Exception("Setting does not exist.")
        
def SetKey(name, value):
    KeyManager.SetKey(name, value)

def GetKey(name):
    try:
        return KeyManager.GetKey(name)
    except:
        raise Exception("This key does not exist.")
    
def StartNova():
    global NovaProcess
    global isNovaRunning
    isNovaRunning.value = 2
    if NovaProcess.is_alive():
        NovaProcess.kill()
    NovaProcess.start()

def StopNova():
    global NovaProcess
    global isNovaRunning
    isNovaRunning.value = 0
    NovaProcess.terminate()
    NovaProcess.join(timeout=1)
    if NovaProcess.is_alive():
        NovaProcess.kill()

def GetStatus():
    return isNovaRunning.value