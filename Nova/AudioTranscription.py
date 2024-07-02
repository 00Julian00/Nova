import os
import numpy as np
import sounddevice as sd
import time as time_module
from Levenshtein import distance
from groq import Groq
from scipy.io import wavfile

# Assuming ConfigInteraction is a custom module you're using
import ConfigInteraction

micIndex = int(ConfigInteraction.GetSetting("MicrophoneIndex"))
hotword = ConfigInteraction.GetSetting("Hotword")
language = ConfigInteraction.GetSetting("Language")

client = Groq(api_key=ConfigInteraction.GetKey("Groq"))
model = "whisper-large-v3"

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
    audio_buffer = np.array([], dtype=np.int16)
    is_recording = False
    silence_start = None
    transcription = None

    def callback(indata, frames, time_info, status):
        global audio_buffer, is_recording, silence_start, transcription
        audio = np.frombuffer(indata, dtype=np.int16)
        normalized_audio = normalize_audio(audio.astype(np.float32))
        rms = calculate_rms(normalized_audio)

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
                    
                    with open(temp_file, "rb") as file:
                        result = client.audio.transcriptions.create(
                            file=(temp_file, file.read()),
                            model=model,
                            response_format="json",
                            language=language
                        )
                    transcription = result.text
                    os.remove(temp_file)  # Clean up temporary file
                    
                    # Signal to stop the audio input stream
                    raise sd.CallbackStop

            else:
                silence_start = None  # Reset silence start time as there is ongoing noise

    with sd.InputStream(callback=callback, dtype=np.int16, channels=1, samplerate=sample_rate, device=micIndex):
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

# Main execution
if __name__ == "__main__":
    print("Listening for hotword...")
    result = DetectHotword()
    if result:
        print(f"Hotword detected! Transcription: {result}")
    else:
        print("No hotword detected.")