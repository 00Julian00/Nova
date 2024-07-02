from elevenlabs.client import ElevenLabs
from elevenlabs import stream, play, Voice, VoiceSettings
import ConfigInteraction
from KeyManager import GetKey

voiceID = ConfigInteraction.GetSetting("ElevenlabsVoiceID")
model = ConfigInteraction.GetSetting("ElevenlabsModel")
client = ElevenLabs(api_key=GetKey("Elevenlabs"))
streamVoice = ConfigInteraction.GetSetting("StreamVoice")

def TTS(generator):        
    
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