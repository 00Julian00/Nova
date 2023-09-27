import subprocess
import sys
import os
import importlib

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), 'NovaEngine'))

import ConfigInteraction

def AddAPIkey(keyName, value): #Add a new entry to the API key list. 'value' is optional
    keys = ConfigInteraction.GetKeys()
    keys[keyName] = value
    ConfigInteraction.SetKeys(keys)

def AddSetting(settingName, value): #Add a new entry to the settings. 'value' is optional
    settings = ConfigInteraction.GetSettings()
    settings[settingName] = value
    ConfigInteraction.SetSettings(settings)

def InstallModule(fileName, methodName, description, propertyList): #Needs to be called, before a module can be used. Call from Initialize() Adds the necessary information to: Functions.json, ModuleList.json, HasModuleBeeninitialized.json
    #Edit ModuleList.json
    moduleList = ConfigInteraction.GetModuleList()
    moduleList[methodName] = fileName
    ConfigInteraction.SetModuleList(moduleList)
    #Edit Functions.json
    functions = ConfigInteraction.GetFunctions()
    newEntry = {
        "name": methodName,
        "description": description,
        "parameters": {
        "type": "object",
        "properties": propertyList,
        "required": []
        }
    }
    functions.append(newEntry)
    ConfigInteraction.SetFunctions(functions)
    #Edit HasModuleBeeninitialized.json
    initializationList = ConfigInteraction.GetModuleInitialization()
    initializationList[methodName] = "True"
    ConfigInteraction.SetModuleInitialization(initializationList)


def InstallLibary(libName):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", libName])
        return(True)
    except Exception as e:
        print(f"Failed to install libary {libName}\n" + e)
        return(False)
    
def InitializeModules(): #Do not call from a module. Is called from Main.py on Nova startup. Calls the 'Initialize' method inside all methods that haven't been initialized
    moduleList = ConfigInteraction.GetModuleList()
    initializationList = ConfigInteraction.GetModuleInitialization()

    initializationCounter = 0

    for module, value in moduleList.items():
        if (initializationList.get(value, None) != "True"):
            #Module has to be initialized
            moduleImport = importlib.import_module(value)
            try:
                methodImport = getattr(moduleImport, "Initialize")
            except:
                print(f"Module {value} could not be initialized. Please make sure it has a method called 'Initialize()', otherwise it can not be used")
                continue

            if (callable(methodImport)):
                methodImport() #Call the 'Initialize()' method inside the Module
                initializationList[value] = "True"
                initializationCounter += 1
            else:
                print(f"Module {value} could not be initialized. Please make sure it has a method called 'Initialize()', otherwise it can not be used")

    ConfigInteraction.SetModuleInitialization(initializationList)
    print(f"{initializationCounter} modules were initialized")
