#This script checks wether a setting the user entered is valid. Return True if valid and an error message that can be printed to the console if not valid
from langcodes import Language
from elevenlabs.client import ElevenLabs
import ConfigInteraction
from KeyManager import GetKey

client = ElevenLabs(api_key=GetKey("Elevenlabs"))

def CheckForValidInput(setting, input):
    if (setting == "Language"):
        try:
            Language.get(input)
            return True
        except:
            return "Invalid input. Must be a valid language code. (For example: en, es, fr, de, etc.)"

    if (setting == "Hotword"):
        return True
    
    if (setting == "GroqModel"):
        return True

    if (setting == "ElevenlabsModel"):
        return True

    if (setting == "ElevenlabsVoiceID"):
        try:
            client.voices.get(input)
            return True
        except:
            return "Invalid input. Must be a valid voice ID. Visit https://elevenlabs.io to find a valid voice and its ID."

    if (setting == "OfflineMode"):
        if (input == "True" or input == "False"):
            return True
        else:
            return "Invalid input. Must be 'True' or 'False'"

    if (setting == "StreamVoice"):
        if (input == "True" or input == "False"):
            return True
        else:
            return "Invalid input. Must be 'True' or 'False'"

    if (setting == "MicrophoneIndex"):
        try:
            int(input)
            return True
        except:
            return "Invalid input. Must be an integer. Type 'micID' in the main menu to get the correct microphone ID."

    if (setting == "Behaviour"):
        return True
    
    if (setting == "Name"):
        return True