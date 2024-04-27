import ConfigInteraction
import whisper
import sounddevice as sd
import numpy as np
import torch
import time as time_module
from Levenshtein import distance

micIndex = int(ConfigInteraction.GetSetting("MicrophoneIndex"))
hotword = ConfigInteraction.GetSetting("Hotword")

device = None
accuracy = "medium"
model = None

def init():
    global model
    global device

    cudaAvailable = torch.cuda.is_available()

    if (cudaAvailable):
        device = "cuda"
    else:
        device = "cpu"
    
    if (device == "cpu"):
        print("> WARNING: Unable to use CUDA. Using CPU.")

    print(f"> Now loading Speech-To-Text model with accuracy: {accuracy}. Device: {device}.")

    try:
        model = whisper.load_model(accuracy, device=device)
    except:
        return False
    return True

def isRunningOnCpu():
    return device == "cpu"

# Audio settings
sample_rate = 16000  # Sample rate in Hz
silence_duration_threshold = 1  # Seconds of silence before processing

# Audio level thresholds
start_threshold = 0.003  # Threshold to start recording
end_threshold = 0.003  # Threshold to end recording

# Normalize audio data from int16 to range -1.0 to 1.0
def normalize_audio(audio):
    return audio / 32768.0

# For RMS calculation
def calculate_rms(audio):
    return np.sqrt(np.mean(audio**2))

def listen():
    global is_recording, silence_start, audio_buffer, transcription
    audio_buffer = np.array([], dtype=np.float32)
    is_recording = False
    silence_start = None
    transcription = None

    def callback(indata, frames, time_info, status):
        global audio_buffer, is_recording, silence_start, transcription
        audio = normalize_audio(np.frombuffer(indata, dtype=np.int16).astype(np.float32))
        rms = calculate_rms(audio)

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
                    audio_to_process = whisper.pad_or_trim(audio_buffer)
                    mel = whisper.log_mel_spectrogram(audio_to_process).to(model.device)
                    options = whisper.DecodingOptions()
                    result = whisper.decode(model, mel, options)
                    transcription = result.text
                    # Signal to stop the audio input stream
                    raise sd.CallbackStop

            else:
                silence_start = None  # Reset silence start time as there is ongoing noise

    with sd.InputStream(callback=callback, dtype='int16', channels=1, samplerate=16000, device=micIndex):
        while transcription is None:
            sd.sleep(100)  # Wait a short time and check again

    return transcription

max_distance = 2
def DetectHotword():
    global hotword, max_distance
    
    #Check how much every word in the description deviates from the hotword. If it is close enough, it will be counted
    transcription = listen()

    words = transcription.lower().split()
    hotword = hotword.lower()
    for i, word in enumerate(words):
        if distance(word, hotword) <= max_distance:
            words[i] = hotword  # replace with the actual hotword
    finalized = ' '.join(words)  # join the words back into a string

    if hotword in finalized:
        return finalized
    else:
        return None