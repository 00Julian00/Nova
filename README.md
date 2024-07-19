# Next-Generation Open-Source Virtual Assistant NOVA

**Version 1.5**

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
    - [Setup](#setup)
    - [Run](#run)
- [Main Menu Commands](#main-menu-commands)
- [Settings](#settings)
- [Version History](#version-history)

## Introduction
The Next-Generation Open-Source Virtual Assistant (or NOVA) is an easily expandable and modifyable virtual assistant. It uses the [Groq API](https://groq.com) for the text transcription, as well as the processing of the query, making it fast and responsive. NOVA uses the [Elevenlabs API](https://elevenlabs.io) for rich and natural speech. NOVA can be easily expanded, using Modules. Modules can add extra functionality to the system, are modular and can be easily developed. See [here](https://github.com/00Julian00/Nova-Devtools.git) for further resources on Module development. NOVA is still under development.

## Requirements

- [Groq API key](https://groq.com)
- [Elevenlabs API key](https://elevenlabs.io)
- [Python 3.11.x with PIP](https://www.python.org)
- [mpv](https://mpv.io)
- [ffmpeg](https://ffmpeg.org/download.html)
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/de/visual-cpp-build-tools/)
- [Cuda 12.1](https://developer.nvidia.com/cuda-12-1-0-download-archive)

## Installation

```bash
git clone https://github.com/00Julian00/Nova.git
cd Nova
pip3 install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
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
- **OfflineMode (True/False)**: Run all required AI models on local hardware. No internet connection is needed, apart from first downloading the models. Switch off Offline Mode for better response times and higher quality.
- **StreamVoice (True/False)**: Do you want to stream the voice? Streaming is generally a lot faster but can lead to buffering, especially if you are not using a turbo model.
- **MicrophoneIndex**: The ID of the microphone the system should use. Find a list of the IDs in the main menu under `micID`.
- **Behaviour**: How the assistant should behave.
- **Name**: How the assistant should call you, i.e. your name.


## Language Files
Language Files are used to translate Novas Interface into different languages. Per default, Nova comes with English and German, but you can create your own:

- ### Creating a Language File:
Go into LangFiles and copy en.json. Rename it to the language code you want to translate it into (For example: en, es, fr, de, etc.). Open the file in a text editor and translate the contents of the individual categories. Do not translate the names of the categories as they are used to find the correct text within the file. Do not change the structure of the file itself.

- ### Updating a Language File:
When a new update releases, it might come with new entries in the Language Files. To update your Language File, first look at the structure of en.json, as this Language File will always be up to date with the newest Version of Nova. If the structure has changed, or a category has new entries you will need to update your file as well. You need to copy the exact structure of en.json. Failing to do so might cause Nova to crash at any point. Finally you need to update the Version that is stored inside the Language File to match that of Nova.

## Version history

### Version 1.5

- **Release Date:** 19.07.2024
- **Changes:**
    - Expanded the capabilities of the Nova API.

### Version 1.4

- **Release Date:** 15.07.2024
- **Changes:**
    - Now using llama-cpp-python for LLM inference for improved speed and reliability. More offline improvements are in development.
    - Switched from Phi-3-mini-128k-instruct to Llama3-8b as the default offline LLM.
    - Added a 'Mixed' offline mode that uses Whisper (hosted on Groq) and Elevenlabs but runs Llama-3-8b on-device.

### Version 1.3

- **Release Date:** 13.07.2024
- **Changes:**
    - First implementation of the Nova API that allows other programs to access Novas features. See [here](https://github.com/00Julian00/Nova-Devtools.git) for a guide on how to use the API. The capabilities of the API will be expanded in the future.

### Version 1.2

- **Release Date:** 12.07.2024
- **Changes:**
    - Added Language file integrations. You can now translate Novas Interface into different languages. See [here](#creating-a-language-file) how to do that.

### Version 1.1.1

- **Release Date:** 12.07.2024
- **Changes:**
    - Security update: Nova now blocks Modules from using the following libaries: os, sys, subprocess, keyring, as these libaries can cause damage on your computer or steal sensitive information.

### Version 1.1

- **Release Date:** 11.07.2024
- **Changes:**
    - Added an Offline Mode which will run all AI models locally, eliminating the need for API keys or an internet connection. The Offline mode uses Faster-Whisper, Phi-3 128k and Coqui TTS.

### Version 1.0

- **Release Date:** 03.07.2024
- **Changes:**
    - Added 'Modules' to easily add more functionality to NOVA.
    - Created a [guide](https://github.com/00Julian00/Nova-Devtools.git) for Module development.

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

- **Release Date:** 27.09.2023
- **Changes:**
    - Inital release.
    - Basic vocal interaction using Google STT, OpenAIs Whisper, OpenAIs GPT 3.5 and Elevenlabs multilingual v1.
    - Basic modules.


## ⚠️SECURITY WARNING
### When using modules created by third parties, please exercise caution:

1. Always review the code: Thoroughly examine any third-party module before running it. This is crucial for ensuring its safety and understanding its functionality.
2. Limited protection: While Nova attempts to restrict access to sensitive libraries, this does not guarantee complete security. Determined actors may find ways to circumvent these restrictions.
3. Trust is key: Only use modules from sources you trust. Be especially cautious with modules that handle sensitive data or perform system operations.
4. Keep updated: Regularly update Nova to have the best possible protection against threats and bad actors.
5. Report suspicions: If you encounter a module that seems malicious or insecure, please report it to the Nova community.

### Remember: The safety of your system ultimately depends on your vigilance. Nova's security features are a supplement to, not a replacement for, your own careful review and judgment.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
