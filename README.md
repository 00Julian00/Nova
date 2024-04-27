Nova personal AI system version 0.2

Requirements:  
- Groq API key (https://groq.com)  
- Elevenlabs API key (https://elevenlabs.io)  
- Python (with pip)  
- mpv  
- CUDA compatible GPU (optional, highly recommended) (CUDA version 12.1+)  

Installation:  
git clone https://github.com/00Julian00/Nova.git  
cd Nova  
pip install -r requirements.txt  

Setup:  
- Run 'Start interface.bat'.  
- Type 'keys'.  
- Enter your Groq and Elevenlabs API keys.  
- Go back to the main menu.  
- Enter 'micID'  
- Find the correct microphone and remember its ID.  
- Enter 'settings'.  
- Chang the microphone ID to the correct ID.  
- Change other settings if necessary.  

Run:  
- In the main menu, type 'boot'.  
- A seperate Terminal will open. Wait until the boot process is complete and the Hotword detection starts.  
- You can now speak to the assistant.  



Main Menu:  
-help: Show a list of all available commands  
-boot: Start Nova  
-keys: Edit your API keys. Warning: Will expose your API keys  
-settings: Edit your settings  
-exit: Exit the Interface. Does not close any instances of Nova running  
-micID: Lists all your microphones and ther IDs. You can then set the correct Id in 'settings'  
-clear: Clear the console  


Settings:  
-Language: The language 'Nova' should use. Must be a valid language code. (For example: en, es, fr, de, etc.).  
-Hotword: Your input will only be processed if it includes this word.  
-LanguageModel: The LLM that should be used. Note that it is not possible to check wether your chosen model is valid, so choose a valid model. (https://console.groq.com/docs/models)  
-ElevenlabsModel: The voice model that should be used for the Text-To-Speech. Note that it is not possible to check wether your chosen model is valid, so choose a valid model. (https://elevenlabs.io/docs/speech-synthesis/models)  
-ElevenlabsVoiceID: The ID of the voice you want to use. You can find the IDs of the premade voices and your own voices on https://elevenlabs.io.  
-StreamVoice (True/False): Do you want to stream the voice? Streaming is generally a lot faster but can lead to buffering, especially if you are not using a turbo model.  
-MicrophoneIndex: The ID of the microphone the system should use. Find a list of the IDs in the main menu under 'micID'.  
-Behaviour: How the assistant should behave. This is essentially the system prompt. Note that the system prompt is expanded upon in the background for higher output quality. If you want to change that, look under ./Nova/Main.py hiddenSystenPrompt.  
-Adressation: How the assistant should adress you (for example 'Sir' or your name).  
  
  
Version 0.2:  
0.2 is a major rewrite of the core system because the code has become very messy, instable, hard to work with and expand. Also the code that was meant to make it easy to add new functionality to Nova ironically made everything more complicated then necessary. This is why for 0.2 modules were removed to focus on a good core. They will be reintroduced in 0.3 and they will be a lot easier to make and add to Nova.
