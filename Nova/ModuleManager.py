import os
import json

script_dir = os.path.dirname(os.path.realpath(__file__))
modulePath = os.path.join(os.path.dirname(script_dir), 'Modules')

def GetModuleFolders():
    entries = os.listdir(modulePath)

    directories = [entry for entry in entries if os.path.isdir(os.path.join(modulePath, entry))]

    return directories

def CheckModuleValidity(folder):
    EntryScript = ""
    EntryFunction = ""
    
    if os.path.exists(os.path.join(modulePath, folder, "manifest.json")):
        with open(os.path.join(modulePath, folder, "manifest.json"), 'r') as file:
            manifest = json.load(file)
            EntryScript = manifest["EntryScript"]
            EntryFunction = manifest["EntryFunction"]

            if (EntryScript == "" or EntryFunction == ""):
                return False
            
        if os.path.exists(os.path.join(modulePath, folder, EntryScript)):
            with open(os.path.join(modulePath, folder, EntryScript), 'r') as file:
                script = file.read()
                
                if EntryFunction in script:
                    return True

    
        return False

for folder in GetModuleFolders():
    print(folder + ": " + str(CheckModuleValidity(folder)))
