#This script checks wether a setting the user entered is valid. Return True if valid and an error message that can be printed to the console if not valid
from langcodes import Language
from elevenlabs.client import ElevenLabs
import ConfigInteraction
from KeyManager import GetKey

langFile = ConfigInteraction.GetLanguageFile()

client = ElevenLabs(api_key=GetKey("Elevenlabs"))

def CheckForValidInput(setting, input):
    if (setting == "Language"):
        try:
            Language.get(input)
            return True
        except:
            return langFile["Errors"][7]

    if (setting == "Hotword"):
        return True
    
    if (setting == "GroqModel"):
        return True

    if (setting == "ElevenlabsModel"):
        return True

    if (setting == "ElevenlabsVoiceID"):
        try:
            if (GetKey("Elevenlabs") != ""):
                client.voices.get(input)
            return True
        except:
            return langFile["Errors"][7]

    if (setting == "OfflineMode"):
        if (input == "True" or input == "False"):
            return True
        else:
            return langFile["Errors"][8]

    if (setting == "StreamVoice"):
        if (input == "True" or input == "False"):
            return True
        else:
            return langFile["Errors"][8]

    if (setting == "MicrophoneIndex"):
        try:
            int(input)
            return True
        except:
            return langFile["Errors"][9]

    if (setting == "Behaviour"):
        return True
    
    if (setting == "Name"):
        return True