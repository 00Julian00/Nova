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

micIndex = int(ConfigInteraction.GetSetting("MicrophoneIndex"))
hotword = ConfigInteraction.GetSetting("Hotword")
language = ConfigInteraction.GetSetting("Language")
offlineMode = ConfigInteraction.GetSetting("OfflineMode")

if (offlineMode == "False"):
    client = Groq(api_key=GetKey("Groq"))
    model = "whisper-large-v3"
else:
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # Required for running on Windows
    fasterWhisperModel = WhisperModel("distil-large-v3", device="cuda", compute_type="float32")

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
    fulltext = ""
    segments, info = fasterWhisperModel.transcribe(temp_file, beam_size=5, language="en", condition_on_previous_text=False)
    for segment in segments:
        fulltext += segment.text
    return fulltext


def Listen():
    global is_recording, silence_start, audio_buffer, transcription
    audio_buffer = np.array([], dtype=np.int16)
    is_recording = False
    silence_start = None
    transcription = None

    def callback(indata, frames, time_info, status):
        global audio_buffer, is_recording, silence_start, transcription
        audio = np.frombuffer(indata, dtype=np.int16)
        normalized_audio = audio.astype(np.float32) / 32768.0
        rms = np.sqrt(np.mean(normalized_audio**2))

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

                    #Check if the audio contains speech
                    if (len(get_speech_ts(read_audio(temp_file), vadModel)) > 0):
                        if (offlineMode == "False"):
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

    with sd.InputStream(callback=callback, dtype=np.int16, channels=1, samplerate=sample_rate, device=micIndex):
        while transcription is None: #Wait for the audio to be processed
            sd.sleep(1)

    return transcription

def DetectHotword():
    global hotword
    
    transcription = Listen()

    if hotword in transcription:
        return transcription
    else:
        return None