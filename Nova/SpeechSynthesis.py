from elevenlabs.client import ElevenLabs
from elevenlabs import stream, play, Voice, VoiceSettings
import ConfigInteraction
from KeyManager import GetKey
import os
from TTS.api import TTS
import simpleaudio
from Helpers import suppress_output_decorator, suppress_output

offlineMode = ConfigInteraction.GetSetting("OfflineMode")

voiceID = None
model = None
client = None
streamVoice = None
tts = None

@suppress_output_decorator
def Initialize():
    global voiceID
    global model
    global client
    global streamVoice
    global tts
    
    if (offlineMode == "False" or offlineMode == "Mixed"):
        voiceID = ConfigInteraction.GetSetting("ElevenlabsVoiceID")
        model = ConfigInteraction.GetSetting("ElevenlabsModel")
        client = ElevenLabs(api_key=GetKey("Elevenlabs"))
        streamVoice = ConfigInteraction.GetSetting("StreamVoice")
    else:
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")


def SpeakStream(generator):        
    audio_stream = client.generate(
        text = generator,
        voice=Voice(
            voice_id=voiceID,
            settings=VoiceSettings(stability=0.6, similarity_boost=1, style=0.2, use_speaker_boost=True)
        ),
        model = model,
        stream = True
    )

    if (streamVoice == "True"):
        stream(audio_stream)
    else:
        play(audio_stream)

def SpeakDirect(text):        
    audio = client.generate(
        text = text,
        voice=Voice(
            voice_id=voiceID,
            settings=VoiceSettings(stability=0.6, similarity_boost=1, style=0.2, use_speaker_boost=True)
        ),
        model = model,
        stream = False
    )

    play(audio)

@suppress_output_decorator
def SpeakOffline(text):
    tts.tts_to_file(text=text, file_path="output.wav")

    playObj = simpleaudio.WaveObject.from_wave_file("output.wav").play()
    playObj.wait_done()

    os.remove("output.wav")