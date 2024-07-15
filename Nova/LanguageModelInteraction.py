from groq import Groq
import json
import os
import ConfigInteraction
from KeyManager import GetKey
import ModuleManager
import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from Helpers import suppress_output_decorator, suppress_output
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
from pathlib import Path
from huggingface_hub import hf_hub_download

script_dir = os.path.dirname(os.path.realpath(__file__))

offlineMode = ConfigInteraction.GetSetting("OfflineMode")

langFile = ConfigInteraction.GetLanguageFile()

client = None
model = None

def Initialize():
    global client
    global model
    
    if (offlineMode == "False"):
        client = Groq(api_key=GetKey("Groq"))
        model = ConfigInteraction.GetSetting("GroqModel")
    else:
        #Check if the llama3 gguf already exists and download it if not
        if not Path(os.path.join(os.path.dirname(script_dir), "Models", "Llama3", "Meta-Llama-3-8B-Instruct-Q8_0.gguf")).is_file():
            os.makedirs(os.path.join(os.path.dirname(script_dir), "Models", "Llama3"), exist_ok=True)
            print(langFile["Status"][13])
            hf_hub_download(
                repo_id="bartowski/Meta-Llama-3-8B-Instruct-GGUF",
                filename="Meta-Llama-3-8B-Instruct-Q8_0.gguf",
                local_dir=os.path.join(os.path.dirname(script_dir), "Models", "Llama3")
            )

        llamaPath = os.path.join(os.path.dirname(script_dir), "Models", "Llama3", "Meta-Llama-3-8B-Instruct-Q8_0.gguf")

        model = Llama(
            model_path=llamaPath,
            #chat_handler=Llava15ChatHandler(clip_model_path=mmproj_path),
            chat_format="chatml",
            n_gpu_layers=-1,
            n_ctx=2048,
            verbose=False,
            logits_all = True
        ) 

def PromptLanguageModelAPI(Input):
    response = client.chat.completions.create(
    model=model,
    tools=ModuleManager.GetModules(),
    messages=Input,
    stream=True)

    return(response)

#@suppress_output_decorator
def PromptLanguageModelLocal(Input):
    response = model.create_chat_completion(Input)
    
    return(response) #response['choices'][0]['message']['content']

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