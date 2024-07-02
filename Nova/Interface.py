#This is the interface to Nova, which can be used to boot and shut down Nova and change settings.

import os
import subprocess
import pyaudio
from Levenshtein import distance
from prompt_toolkit import prompt
import ConfigInteraction
from CheckForValidInput import CheckForValidInput

commands = ConfigInteraction.GetInterfaceCommands()
version = ConfigInteraction.GetManifest()["version"]

#Constants
distanceToSuggest = 2


def Help():
    #Print all available commands
    for name, description in commands.items():
        print(name + ": " + description)

def Boot():
    batch_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "run.bat")

    subprocess.Popen(['start', 'cmd', '/c', batch_file_path], shell=True)


def Shutdown(): #!Bugged. Disabled in the interface.
    subprocess.run('taskkill /F /fi "windowtitle eq Nova  - python*"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def EditAPIkeys():
    #List all API keys and let the user change them
    
    confirm = input("Warning, this will expose your API keys. Continue? [y/n] ")

    if (confirm == "n"):
        print("Canceling...")
        return
    elif (confirm != "y"):
        print("Invalid. Canceling...")
        return
    
    try:
        keys = ConfigInteraction.GetKeys()
    except:
        print("Unable to access the API keys file.")
        return
    
    while True:
        #List the settings
        PrintHeader()
        settingID = 1
        names = []
        values = []
        for name, value in keys.items():
            print(str(settingID) + ". ", name + " | ", value)
            settingID += 1
            names.append(name)
            values.append(value)
        
        chosenKeys = input("\nChoose key to edit by typing the number. Press enter to save.\n> ")

        #Save the settings and exit the settings menu
        if (chosenKeys == ""):
            ConfigInteraction.SetKeys(keys)
            PrintHeader()
            return
        
        #Check the input for validity
        try:
            chosenKeys = int(chosenKeys)
        except:
            print("Invalid input. Type the number of the key you want to edit or press enter to save.")
            continue

        if (chosenKeys < 1 or chosenKeys > len(keys)):
            print("Invalid input. Type the number of the key you want to edit or press enter to save.")
            continue
        
        #Edit the setting
        PrintHeader()
        print("\nType the new value and press enter to save. Press enter to keep the current value:")
        keys[names[chosenKeys - 1]] = prompt(names[chosenKeys - 1] + " | ", default = keys[names[chosenKeys - 1]])
        ClearConsole()

def Settings():
    try:
        settings = ConfigInteraction.GetSettings()
    except:
        print("Unable to access the settings file.")
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
        
        chosenSettings = input("\nChoose setting to edit by typing the number. Press enter to save.\n> ")

        #Save the settings and exit the settings menu
        if (chosenSettings == ""):
            ConfigInteraction.SetSettings(settings)
            PrintHeader()
            return
        
        #Check the input for validity
        try:
            chosenSettings = int(chosenSettings)
        except:
            print("Invalid input. Type the number of the setting you want to edit or press enter to save.")
            continue

        if (chosenSettings < 1 or chosenSettings > len(settings)):
            print("Invalid input. Type the number of the setting you want to edit or press enter to save.")
            continue
        
        #Edit the setting
        PrintHeader()
        print("\nType the new value and press enter to save. Press enter to keep the current value:")
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

def CheckForCloseCommand(command): #Check if an input is close to a command and suggest it
    for name, description in commands.items():
        if (distance(command, name) <= distanceToSuggest):
            print(f"Invalid. Did you mean {name}?")
            return
    print("Invalid. Type 'help' to see a list of all available commands")

def ProcessInput():
    Input = input("> ")

    #Check through all possible commands

    if (Input == "help"):
        Help()
    elif (Input == "boot"):
        print("Booting...")
        Boot()
    elif (Input == "shutdown"):
        print("Shutting down...")
        Shutdown()
    elif (Input == "reboot"):
        print("Rebooting...")
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
        CheckForCloseCommand(Input)

    #To add: Run diagnostics
    
    ProcessInput() #Loop

def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

def PrintHeader():
    ClearConsole()
    print(f'Nova Interface (Version {version}). Developed by Julian. Type "help" to see a list of all available commands\n')

PrintHeader()
ProcessInput()