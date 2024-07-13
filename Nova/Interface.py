#This is the interface to Nova, which can be used to boot and shut down Nova and change settings.

import os
import subprocess
import pyaudio
from prompt_toolkit import prompt
import ConfigInteraction
from CheckForValidInput import CheckForValidInput
from KeyManager import GetKey, SetKey, GetKeyList

os.environ['PYTHONIOENCODING'] = 'UTF-8'

langFile = ConfigInteraction.GetLanguageFile()

version = ConfigInteraction.GetManifest()["version"]

#Constants
distanceToSuggest = 2


def Help():
    #Print all available commands
    for setting in langFile["Settings"]:
        print(setting)

def Boot():
    corePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "StartCore.py")
    corePath = '"' + corePath + '"'
    command = f'start cmd /c title Nova ^& python {corePath}'

    subprocess.Popen(command, shell=True)


def Shutdown(): #!Bugged. Disabled in the interface.
    subprocess.run('taskkill /F /fi "windowtitle eq Nova  - python*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def EditAPIkeys():
    #List all API keys and let the user change them
    
    confirm = input(langFile["Warnings"][0] + " ")

    if (confirm == "n"):
        print(langFile["Errors"][0])
        return
    elif (confirm != "y"):
        print(langFile["Errors"][1])
        return

    
    while True:
        #List the keys
        PrintHeader()
        for id in GetKeyList():
            if (GetKey(GetKeyList()[id]) == None):
                SetKey(GetKeyList()[id], "")
            
            print(id + ". " + GetKeyList()[id] + " | ", GetKey(GetKeyList()[id]))
        
        chosenKey = input("\n" + langFile["Interface"][2] + "\n> ")

        #Save the keys and exit the settings menu
        if (chosenKey == ""):
            PrintHeader()
            return
        
        #Check the input for validity
        try:
            int(chosenKey)
        except:
            print(langFile["Errors"][2])
            continue

        if (int(chosenKey) < 1 or int(chosenKey) > len(GetKeyList())):
            print(langFile["Errors"][2])
            continue
        
        chosenKey = str(chosenKey)

        #Edit the setting
        PrintHeader()
        print("\n" + langFile["Interface"][3])

        SetKey(GetKeyList()[chosenKey], prompt(f"{GetKeyList()[chosenKey]} | ", default = GetKey(GetKeyList()[chosenKey])))
        ClearConsole()

def Settings():
    global langFile
    
    try:
        settings = ConfigInteraction.GetSettings()
    except:
        print(langFile["Errors"][3])
        return
    
    while True:
        #List the settings
        PrintHeader()
        settingID = 1
        names = []
        values = []
        for name, value in settings.items():
            print(str(settingID) + ". ", name + " | ", value)
            settingID += 1
            names.append(name)
            values.append(value)
        
        chosenSettings = input("\n" + langFile["Interface"][4] + "\n> ")

        #Save the settings and exit the settings menu
        if (chosenSettings == ""):
            ConfigInteraction.SetSettings(settings)
            langFile = ConfigInteraction.GetLanguageFile() #Reload the language file in case the user switched languages
            PrintHeader()
            return
        
        #Check the input for validity
        try:
            chosenSettings = int(chosenSettings)
        except:
            print(langFile["Errors"][4])
            continue

        if (chosenSettings < 1 or chosenSettings > len(settings)):
            print(langFile["Errors"][4])
            continue
        
        #Edit the setting
        PrintHeader()
        print("\n" + langFile["Interface"][3])
        newValue = prompt(names[chosenSettings - 1] + " | ", default = settings[names[chosenSettings - 1]])
        while True:
            valid = CheckForValidInput(names[chosenSettings - 1], newValue)

            if (valid == True):
                settings[names[chosenSettings - 1]] = newValue
                ClearConsole()
                break
            else:
                PrintHeader()
                print("\n" + valid)
                newValue = prompt(names[chosenSettings - 1] + " | ", default = settings[names[chosenSettings - 1]])


def ListMicID():
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"Index: {i}, Name: {info['name']}")

    p.terminate()

def ProcessInput():
    Input = input("> ")

    #Check through all possible commands

    if (Input == "help"):
        Help()
    elif (Input == "boot"):
        print(langFile["Status"][0])
        Boot()
    elif (Input == "shutdown"):
        print(langFile["Status"][1])
        Shutdown()
    elif (Input == "reboot"):
        print(langFile["Status"][2])
        Shutdown()
        Boot()
    elif (Input == "keys"):
        EditAPIkeys()
    elif (Input == "settings"):
        Settings()
    elif (Input == "exit"): #Exit the Interface without having to forcefully close the terminal
        print("Exiting...")
        subprocess.run('taskkill /fi "windowtitle eq Interface*"', shell=True)
        return
    elif (Input == "micID"):
        ListMicID()
    elif (Input == "clear"):
        PrintHeader()
    else:
        print(langFile["Errors"][6])

    #To add: Run diagnostics
    
    ProcessInput() #Loop

def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def PrintHeader():
    ClearConsole()
    print(langFile["Interface"][0] + " (" + langFile["Interface"][5] + " " + version + "). " + langFile["Interface"][1] + " " + langFile["Interface"][6])

    if (langFile["Version"] != str(version)):
        print(langFile["Warnings"][1])


PrintHeader()
ProcessInput()