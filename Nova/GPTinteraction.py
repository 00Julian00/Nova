from groq import Groq
import json
import os
import ConfigInteraction

client = Groq(api_key=ConfigInteraction.GetKey("Groq"))

model = ConfigInteraction.GetSetting("LanguageModel")

conversation = []

def CallGPT(Input):
    response = client.chat.completions.create(
    model=model,
    messages=Input,
    stream=True)

    return(response)

def ExtractArguments(response):
    arguments = ""

    for event in response:
        if ("function_call" in event.choices[0].delta): #Checks if the data is text or a function call
            arguments += event.choices[0].delta.function_call.arguments
    
    try:
        arguments = json.loads(arguments['information'])  # Needs to process arguments once after the streaming process to get clean data
    except:
        pass  # If this cleanup fails, then that means that GPT has not called a function, or there were no arguments
    
    return(arguments)