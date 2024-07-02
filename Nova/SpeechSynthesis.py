from elevenlabs.client import ElevenLabs
from elevenlabs import stream, play, Voice, VoiceSettings
import ConfigInteraction

voiceID = ConfigInteraction.GetSetting("ElevenlabsVoiceID")

model = ConfigInteraction.GetSetting("ElevenlabsModel")

client = ElevenLabs(api_key=ConfigInteraction.GetKey("Elevenlabs"))

streamVoice = ConfigInteraction.GetSetting("StreamVoice")

Textfull = ""

def Generator(response):
    global Textfull
    
    for event in response:
        if (event.choices[0].delta.content != None):
            Textfull += event.choices[0].delta.content
            yield(event.choices[0].delta.content)
        else:
            yield("")

def TTS(response):        
    global Textfull
    Textfull = ""
    
    generator = Generator(response)
    
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

    print("Response: " + Textfull + "\n")

    return(Textfull)
from elevenlabs.client import ElevenLabs
from elevenlabs import stream, play, Voice, VoiceSettings
import ConfigInteraction

voiceID = ConfigInteraction.GetSetting("ElevenlabsVoiceID")

model = ConfigInteraction.GetSetting("ElevenlabsModel")

client = ElevenLabs(api_key=ConfigInteraction.GetKey("Elevenlabs"))

streamVoice = ConfigInteraction.GetSetting("StreamVoice")

Textfull = ""

def Generator(response):
    global Textfull
    
    for event in response:
        if (event.choices[0].delta.content != None):
            Textfull += event.choices[0].delta.content
            yield(event.choices[0].delta.content)
        else:
            yield("")

def TTS(response):        
    global Textfull
    Textfull = ""
    
    generator = Generator(response)
    
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

    print("Response: " + Textfull + "\n")

    return(Textfull)