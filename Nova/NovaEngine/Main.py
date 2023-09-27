#Ths script connects all the different scripts in the Nova engine

import threading
from AudioTranscription import Listen
from SpeechSynthesis import TTS
from GPTinteraction import CallGPT, ExtractArguments
from ModuleHub import CallFunction, LoadModules
import ConfigInteraction
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), 'Modules'))
import ModuleAPI

#This is the array that stores the entire conversation
conversation = []

systemPrompt = ConfigInteraction.GetSetting("Behaviour")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def AddToConversation(type, content, functionName, callGPT):
    if(type == 0): #User
        conversation.append({"role": "user", "content": content})
    elif(type == 1): #AI
        conversation.append({"role": "assistant", "content": content})
    elif(type == 2): #Function
        conversation.append({"role": "function", "name": functionName, "content": content})
    elif(type == 3): #System
        conversation.append({"role": "system", "content": content})

    if(callGPT):
        InteractWithGPT()


def InteractWithGPT():
    #Call GPT. It is put into a try-except block to cath potential errors when calling the API.    
    try:
        GPTresponse = CallGPT(conversation)
    except Exception as e:
        print("An error occured when communicating with GPT:\n" + str(e))

    #Check, wether the response is text, or a function call
    event = next(GPTresponse)

    if ("function_call" in event['choices'][0]['delta']): #Checks if the data is text or a function call
        #If the GPT response is a function call, the data gets extracted in the GPTinteraction script and then the ModuleHub is beeing called. The response is added to the conversation and GPT is called again
        function_name = event["choices"][0]["delta"]["function_call"]["name"]
        arguments = ExtractArguments(GPTresponse)

        if (arguments == '{}'):
            arguments = None
            #Inform the user about the function call
            print("Nova is attempting to call the module " + function_name)
        else:
            #Inform the user about the function call
            print("Nova is attempting to call the module " + function_name + " with arguments: " + arguments)

        content = CallFunction(function_name, arguments)
        
        AddToConversation(2, content, function_name, True)
            
    elif('content' in event['choices'][0]['delta']): #First checks if 'content' exists, if so, the text is streamed to the elevenlabs API
        GPTaddToConvo = TTS(GPTresponse) #Sends the stream to the TTS, which also extracts the text which then get's added to the conversation

        AddToConversation(1, GPTaddToConvo, None, False)



def StartHotwordDetection():
    while True:
        try: #Start the hotword detection
            threading.Thread(target=AddToConversation, args=(0, Listen(), None, True)).start()

        except Exception as e:
            print("Error when attempting to start the hotword detection\n" + e)


def PrintHeader():
    print("Nova AI Assistant (Version Beta 1). Developed by Julian")
    print("")
    print("Loaded behaviour: " + systemPrompt)
    #Initialize the modules
    ModuleAPI.InitializeModules()
    #Load the modules
    print("Loaded modules: " + LoadModules() + "\n")

    print("Starting the Hotword detection...\n")
    

AddToConversation(3, systemPrompt, None, False)

PrintHeader()

StartHotwordDetection()