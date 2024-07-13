from groq import Groq
import json
import os
import ConfigInteraction
from KeyManager import GetKey
import ModuleManager
import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from Helpers import suppress_output_decorator, suppress_output

offlineMode = ConfigInteraction.GetSetting("OfflineMode")

client = 0
model = 0
pipe = 0
generation_args = 0

@suppress_output_decorator
def Initialize():
    global client
    global model
    global pipe
    global generation_args
    
    if (offlineMode == "False"):
        client = Groq(api_key=GetKey("Groq"))
        model = ConfigInteraction.GetSetting("GroqModel")
    else:
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = 'True'
        torch.random.manual_seed(0) 
        model = AutoModelForCausalLM.from_pretrained( 
            "microsoft/Phi-3-mini-128k-instruct",  
            device_map="cuda",  
            torch_dtype="auto",  
            trust_remote_code=True,  
        )

        pipe = pipeline( 
            "text-generation", 
            model=model, 
            tokenizer=AutoTokenizer.from_pretrained("failspy/Phi-3-mini-128k-instruct-abliterated-v3"), 
        ) 

        generation_args = { 
            "max_new_tokens": 512, 
            "return_full_text": False, 
            "temperature": 0.0, 
            "do_sample": False, 
        }

def PromptLanguageModelAPI(Input):
    response = client.chat.completions.create(
    model=model,
    tools=ModuleManager.GetModules(),
    messages=Input,
    stream=True)

    return(response)

@suppress_output_decorator
def PromptLanguageModelLocal(Input):
    output = pipe(Input, **generation_args) 
    
    return(output)

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