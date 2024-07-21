import os
import numpy as np
import sounddevice as sd
import time as time_module
from groq import Groq
from scipy.io import wavfile
import ConfigInteraction
from KeyManager import GetKey
from faster_whisper import WhisperModel
import torch
import torchaudio
from Helpers import suppress_output, suppress_output_decorator

from whisper_cpp_python import Whisper
import re
import subprocess

from lightning_whisper_mlx import LightningWhisperMLX

whisper = LightningWhisperMLX(model="distil-large-v3", batch_size=12, quant=None)

micIndex = int(ConfigInteraction.GetSetting("MicrophoneIndex"))
hotword = ConfigInteraction.GetSetting("Hotword")
language = ConfigInteraction.GetSetting("Language")
offlineMode = ConfigInteraction.GetSetting("OfflineMode")

client = None
model = None
get_speech_ts = None
read_audio = None
vadModel = None

@suppress_output_decorator
def Initialize():
    global client
    global model
    global get_speech_ts
    global read_audio
    global vadModel

    if (offlineMode == "False" or offlineMode == "Mixed"):
        client = Groq(api_key=GetKey("Groq"))
        model = "whisper-large-v3"
    else:
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # Required for running on Windows

    vadModel, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', trust_repo=True)
    (get_speech_ts, _, read_audio, VADIterator, collect_chunks) = utils

# Audio settings
sample_rate = 16000  # Sample rate in Hz
silence_duration_threshold = 1  # Seconds of silence before processing
start_threshold = 0.003
end_threshold = 0.003 


def ProcessAPI(temp_file):
    with open(temp_file, "rb") as file:
        result = client.audio.transcriptions.create(
            file=(temp_file, file.read()),
            model=model,
            response_format="json",
            language=language
        )

    return result.text

def ProcessLocal(temp_file):
    text = whisper.transcribe(audio_path=temp_file)['text']
    print("Transcription: " + text)

    return text

def extract_text_from_output(output):
    # Use regex to extract only the text part from the output
    lines = output.splitlines()
    text = ""
    for line in lines:
        match = re.search(r']\s+(.*)', line)
        if match:
            text += match.group(1) + " "
    return text.strip()

def Listen():
    global is_recording, silence_start, audio_buffer, transcription
    audio_buffer = np.array([], dtype=np.int16)
    is_recording = False
    silence_start = None
    transcription = None
    startTime = time_module.time()

    def callback(indata, frames, time_info, status):
        global audio_buffer, is_recording, silence_start, transcription
        audio = np.frombuffer(indata, dtype=np.int16)
        normalized_audio = audio.astype(np.float32) / 32768.0
        rms = np.sqrt(np.mean(normalized_audio**2))

        if not is_recording and time_module.time() - startTime > 1:  # Timeout after 1 second
            transcription = ""

        # Start recording when the audio level exceeds the start threshold
        if not is_recording and rms > start_threshold:
            is_recording = True
            silence_start = None

        if is_recording:
            audio_buffer = np.concatenate((audio_buffer, audio))

            # Check if the audio level falls below the end threshold
            if rms < end_threshold:
                current_time = time_module.time()
                if silence_start is None:
                    silence_start = current_time  # Mark the start of silence
                elif current_time - silence_start >= silence_duration_threshold:
                    # Process the accumulated audio
                    temp_file = "temp_audio.wav"
                    wavfile.write(temp_file, sample_rate, audio_buffer)

                    # Check if the audio contains speech
                    if len(get_speech_ts(read_audio(temp_file), vadModel)) > 0:
                        if offlineMode == "False" or offlineMode == "Mixed":
                            transcription = ProcessAPI(temp_file)
                        else:
                            transcription = ProcessLocal(temp_file)
                    else:
                        transcription = ""

                    os.remove(temp_file)  # Clean up temporary file
                    
                    # Signal to stop the audio input stream
                    raise sd.CallbackStop

            else:
                silence_start = None  # Reset silence start time as there is ongoing noise

    try:
        with sd.InputStream(callback=callback, dtype=np.int16, channels=1, samplerate=sample_rate, device=micIndex):
            while transcription is None:  # Wait for the audio to be processed
                sd.sleep(100)
    except Exception as e:
        print(f"Unexpected error: {e}")

    return transcription

def DetectHotword():
    global hotword
    
    transcription = Listen()

    if hotword in transcription:
        return transcription
    else:
        return None