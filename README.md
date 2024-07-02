# Next-Generation Open-Source Virtual Assistant NOVA

**Version 0.2.2**

## Requirements

- [Groq API key](https://groq.com)
- [Elevenlabs API key](https://elevenlabs.io)
- [Python](https://www.python.org)
- [mpv](https://mpv.io)

## Installation

```bash
git clone https://github.com/00Julian00/Nova.git
cd Nova
pip install -r requirements.txt --upgrade
```

## Setup

1. Run `Start interface.bat`.
2. Type `keys`.
3. Enter your Groq and Elevenlabs API keys.
4. Go back to the main menu.
5. Enter `micID`.
6. Find the correct microphone and remember its ID.
7. Enter `settings`.
8. Change the microphone ID to the correct ID.
9. Change other settings if necessary.

## Run

1. In the main menu, type `boot`.
2. A separate terminal will open. Wait until the boot process is complete and the Hotword detection starts.
3. You can now speak to the assistant.
4. Make sure to say the specified hotword (default is "Nova") at some point during your prompt, or it will be ignored.

## Main Menu Commands

- `help`: Show a list of all available commands
- `boot`: Start Nova
- `keys`: Edit your API keys. **Warning:** Will expose your API keys
- `settings`: Edit your settings
- `exit`: Exit the interface. Does not close any instances of Nova running
- `micID`: Lists all your microphones and their IDs. You can then set the correct ID in `settings`
- `clear`: Clear the console

## Settings

- **Language**: The language 'Nova' should use. Must be a valid language code (e.g., en, es, fr, de, etc.).
- **Hotword**: Your input will only be processed if it includes this word.
- **LanguageModel**: The LLM that should be used. Note that it is not possible to check whether your chosen model is valid, so choose a valid model. [Groq Models](https://console.groq.com/docs/models)
- **ElevenlabsModel**: The voice model that should be used for the Text-To-Speech. Note that it is not possible to check whether your chosen model is valid, so choose a valid model. [Elevenlabs Models](https://elevenlabs.io/docs/speech-synthesis/models)
- **ElevenlabsVoiceID**: The ID of the voice you want to use. You can find the IDs of the premade voices and your own voices on [Elevenlabs](https://elevenlabs.io).
- **StreamVoice (True/False)**: Do you want to stream the voice? Streaming is generally a lot faster but can lead to buffering, especially if you are not using a turbo model.
- **MicrophoneIndex**: The ID of the microphone the system should use. Find a list of the IDs in the main menu under `micID`.
- **Behaviour**: How the assistant should behave. This is essentially the system prompt. Note that the system prompt is expanded upon in the background for higher output quality. If you want to change that, look under `./Nova/Main.py hiddenSystemPrompt`.
- **Adressation**: How the assistant should address you (e.g., 'Sir' or your name).


## Version history

### Version 0.2.2

- **Release Date:** 02.07.2024
- **Changes:**
    - Changed how the API keys are stored to the "keyring" libary. It is no more possible to find the API keys in the source files.


### Version 0.2.1

- **Release Date:** 02.07.2024
- **Changes:**
    - Moved the hotword detection to the Groq API.


### Version 0.2

- **Release Date:** 27.04.2024
- **Changes:**
    - Removed modules for rework.
    - Reworked internal file structure.
    - Switched from the OpenAI API to the Groq API.
    - General changes and improvements.

### Version 0.1

- **Release Date:** 27.09.2024
- **Changes:**
    - Inital release.
    - Basic vocal interaction using Google STT, OpenAIs Whisper, OpenAIs GPT 3.5 and Elevenlabs multilingual v1.
    - Basic modules.


## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
