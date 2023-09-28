#This is the interface to Nova, which can be used to boot and shut down Nova, as well as change settings and add new Modules and access documentation
#It is run in a CMD terminal, via another script

import os
import subprocess
import pyaudio
import sys
from Levenshtein import distance
from prompt_toolkit import prompt
import ctypes
import time

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), 'NovaEngine'))

import ConfigInteraction

#Load the APIkeys file
keys = ConfigInteraction.GetKeys()

settings = ConfigInteraction.GetSettings()

commands = ConfigInteraction.GetInterfaceCommands()

#Constants
distanceToSuggest = 2


def Help():
    #Print all available commands
    for name, description in commands.items():
        print(name + ": " + description)
    

def Boot():
    #Start Main.py as a CMD console. Changes the working directory briefly to the location of Main.py
    os.chdir(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), 'NovaEngine'))
    subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", f"title Nova && python Main.py"])
    os.chdir(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), 'Configs'))

def Shutdown():
    subprocess.run('taskkill /fi "windowtitle eq Nova*"', shell=True)

def EditAPIkeys():
    #List all API keys and let the user change them
    
    confirm = input("Warning, this will expose your API keys. Continue? [y/n] ")

    if (confirm == "n"):
        print("Canceling...")
        return
    elif (confirm != "y"):
        print("Invalid. Canceling...")
        return
    
    for name, value in keys.items():
        key = prompt(name + " | Press enter to preserve value\n", default = value)

        if (key != ""):
            keys[name] = key
        else:
            keys[name] = value

    #Write the updated keys to the file
    try:
        ConfigInteraction.SetKeys(keys)
        print("Your keys have been saved")
    except Exception as e:
        print("Unable to save API keys\n" + e)

def Settings():
    for name, value in settings.items():
        setting = prompt(name + " | Press enter to preserve value\n", default = value)

        if (setting != ""):
            settings[name] = setting
        else:
            settings[name] = value

    #Write the updated keys to the file
    try:
        ConfigInteraction.SetSettings(settings)
        print("Your settings have been saved")
    except Exception as e:
        print("Unable to save settings\n" + e)

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

def Install():
    # Create a temporary PowerShell script
    script_content = """
    Set-ExecutionPolicy Bypass -Scope Process
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    choco install mpv
    """
    
    script_path = os.path.join(os.environ['TEMP'], 'install_choco_and_mpv.ps1')
    with open(script_path, 'w') as script_file:
        script_file.write(script_content)
    
    # Execute the temporary script with elevated privileges
    cmd = f"-ExecutionPolicy Bypass -File {script_path}"
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell", cmd, None, 1) # Run as admin

    #Now install all needed libaries
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Levenshtein"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "elevenlabs"])

    print("\nAll dependencies have been succesfully installed")

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
    elif (Input == "install"):
        print("Installing dependencies. This may take a few minutes...")
        Install()
    else:
        CheckForCloseCommand(Input)

    #To add: Run diagnostics
    
    ProcessInput() #Loop

def PrintHeader():
    print('Nova Interface (Version 0.1 (alpha)). Developed by Julian. Type "help" to see a list of all available commands\n')

PrintHeader()
ProcessInput()
