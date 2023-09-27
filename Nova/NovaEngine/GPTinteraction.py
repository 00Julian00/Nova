import openai
import json
import os
import ConfigInteraction

conversation = []

#Change the working directory to the same directory the script sits in. This allows it to interact with files that are located in the same directory, no matter where the file is on the computer
os.chdir(os.path.dirname(os.path.realpath(__file__)))

FunctionsDirectory = os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)), 'Configs', 'Functions.json')

openai.api_key = ConfigInteraction.GetKey("OpenAI")

model = ConfigInteraction.GetSetting("GPTmodel")

#Load the GPT functions
try:
    with open(FunctionsDirectory) as f:
        Functions = json.load(f)
except Exception as e:
    print("Error when loading functions:\n" + e)


def CallGPT(Input):
    response = openai.ChatCompletion.create(
        model=model,
        messages=Input,
        functions=Functions,
        function_call="auto",
        stream=True
    )

    return(response)

def ExtractArguments(response):
    arguments = ""

    for event in response:
        if ("function_call" in event['choices'][0]['delta']): #Checks if the data is text or a function call
            arguments += event['choices'][0]['delta']['function_call']['arguments']
    
    try:
        arguments = json.loads(arguments['information'])  # Needs to process arguments once after the streaming process to get clean data
    except:
        pass  # If this cleanup fails, then that means that GPT has not called a function, or there were no arguments
    
    return(arguments)