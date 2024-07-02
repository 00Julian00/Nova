from groq import Groq
import json
import os
import ConfigInteraction
from KeyManager import GetKey

client = Groq(api_key=GetKey("Groq"))
model = ConfigInteraction.GetSetting("LanguageModel")

debugTools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                    },
                    "required": [],
                },
            },
        }
    ]


def PromptLanguageModel(Input):
    response = client.chat.completions.create(
    model=model,
    tools=debugTools,
    messages=Input,
    stream=True)

    return(response)

class LLMStreamProcessor:
    def __init__(self):
        self.response_text = ""
        self.function_calls = []

    def ExtractData(self, stream):
        self.response_text = ""
        self.function_calls = []

        for event in stream:
            # Check for function calls
            if event.choices[0].delta.tool_calls:
                self.function_calls.append(event.choices[0].delta.tool_calls[0])
                break  # Stop processing after detecting a function call

            if event.choices[0].delta.content is not None:
                content = event.choices[0].delta.content
                self.response_text += content
                yield content
            else:
                yield ""  # Yield empty string if content is None

    def GetData(self):
        return self.response_text, self.function_calls
