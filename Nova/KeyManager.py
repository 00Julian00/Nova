import os
import json
import keyring

script_dir = os.path.dirname(os.path.realpath(__file__))
KeyList = os.path.join(script_dir, 'Configs', 'KeyList.json')

def GetKey(name):
    return keyring.get_password("Nova", name)

def SetKey(name, value):
    keyring.set_password("Nova", name, value)

def GetKeyList():
    try:
        with open(KeyList, 'r') as file:
            return(json.load(file))
    except Exception as e:
        print("Failed to fetch key list\n" + e)