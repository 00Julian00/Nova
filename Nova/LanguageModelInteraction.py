from groq import Groq
import json
import os
import ConfigInteraction

client = Groq(api_key=ConfigInteraction.GetKey("Groq"))

model = ConfigInteraction.GetSetting("LanguageModel")

def PromptLanguageModel(Input):
    response = client.chat.completions.create(
    model=model,
    messages=Input,
    stream=True)

    return(response)