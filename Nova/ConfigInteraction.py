#Allows for easy fetching and editing of files in 'Configs'
import os
import json

script_dir = os.path.dirname(os.path.realpath(__file__))

SettingsPath = os.path.join(script_dir, 'Configs', 'NovaSettings.config')
APIkeysPath = os.path.join(script_dir, 'Configs', 'APIkeys.json')
InterfaceCommandsPath = os.path.join(script_dir, 'Configs', 'InterfaceCommands.json')
ModuleListPath = os.path.join(script_dir, 'Configs', 'ModuleList.json')
FunctionsPath = os.path.join(script_dir, 'Configs', 'Functions.json')
ModuleInitializationPath = os.path.join(script_dir, 'Configs', 'HasModuleBeenInitialized.json')


def GetKey(key):
    try:
        with open(APIkeysPath, 'r') as file:
            keys = json.load(file)
            return(keys[key])
    except Exception as e:
        print("Failed to fetch API keys\n" + e)

def GetKeys():
    try:
        with open(APIkeysPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch API keys\n" + e)

def GetSetting(setting):
    try:
        with open(SettingsPath, 'r') as file:
            settings = json.load(file)
            return(settings[setting])
    except Exception as e:
        print("Failed to fetch settings\n" + e)

def GetSettings():
    try:
        with open(SettingsPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch settings\n" + e)

def GetInterfaceCommands():
    try:
        with open(InterfaceCommandsPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch interface commands\n" + e)

def SetKeys(keys):
    with open(APIkeysPath, 'w') as file:
        file.write(json.dumps(keys, indent=4))

def SetSettings(settings):
    with open(SettingsPath, 'w') as file:
        file.write(json.dumps(settings, indent=4))

def GetModuleList():
    try:
        with open(ModuleListPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch module list\n" + e)

def SetModuleList(moduleList):
    with open(ModuleListPath, 'w') as file:
        file.write(json.dumps(moduleList, indent=4))

def GetFunctions():
    try:
        with open(FunctionsPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch functions\n" + e)

def SetFunctions(functions):
    with open(FunctionsPath, 'w') as file:
        file.write(json.dumps(functions, indent=4))

def GetModuleInitialization():
    try:
        with open(ModuleInitializationPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to list of initialized Modules\n" + e)

def SetModuleInitialization(value):
    with open(ModuleInitializationPath, 'w') as file:
        file.write(json.dumps(value, indent=4))
#Allows for easy fetching and editing of files in 'Configs'
import os
import json

script_dir = os.path.dirname(os.path.realpath(__file__))

SettingsPath = os.path.join(script_dir, 'Configs', 'NovaSettings.config')
APIkeysPath = os.path.join(script_dir, 'Configs', 'APIkeys.json')
InterfaceCommandsPath = os.path.join(script_dir, 'Configs', 'InterfaceCommands.json')
ModuleListPath = os.path.join(script_dir, 'Configs', 'ModuleList.json')
FunctionsPath = os.path.join(script_dir, 'Configs', 'Functions.json')
ModuleInitializationPath = os.path.join(script_dir, 'Configs', 'HasModuleBeenInitialized.json')


def GetKey(key):
    try:
        with open(APIkeysPath, 'r') as file:
            keys = json.load(file)
            return(keys[key])
    except Exception as e:
        print("Failed to fetch API keys\n" + e)

def GetKeys():
    try:
        with open(APIkeysPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch API keys\n" + e)

def GetSetting(setting):
    try:
        with open(SettingsPath, 'r') as file:
            settings = json.load(file)
            return(settings[setting])
    except Exception as e:
        print("Failed to fetch settings\n" + e)

def GetSettings():
    try:
        with open(SettingsPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch settings\n" + e)

def GetInterfaceCommands():
    try:
        with open(InterfaceCommandsPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch interface commands\n" + e)

def SetKeys(keys):
    with open(APIkeysPath, 'w') as file:
        file.write(json.dumps(keys, indent=4))

def SetSettings(settings):
    with open(SettingsPath, 'w') as file:
        file.write(json.dumps(settings, indent=4))

def GetModuleList():
    try:
        with open(ModuleListPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch module list\n" + e)

def SetModuleList(moduleList):
    with open(ModuleListPath, 'w') as file:
        file.write(json.dumps(moduleList, indent=4))

def GetFunctions():
    try:
        with open(FunctionsPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch functions\n" + e)

def SetFunctions(functions):
    with open(FunctionsPath, 'w') as file:
        file.write(json.dumps(functions, indent=4))

def GetModuleInitialization():
    try:
        with open(ModuleInitializationPath, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to list of initialized Modules\n" + e)

def SetModuleInitialization(value):
    with open(ModuleInitializationPath, 'w') as file:
        file.write(json.dumps(value, indent=4))