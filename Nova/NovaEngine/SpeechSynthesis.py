from elevenlabs import generate, stream
import ConfigInteraction

apiKey = ConfigInteraction.GetKey("Elevenlabs")

voice = ConfigInteraction.GetSetting("ElevenlabsVoice")

model = ConfigInteraction.GetSetting("ElevenlabsModel")

language = ConfigInteraction.GetSetting("Language")

Textfull = ""

def Generator(response):
    global Textfull
    
    for event in response:
        try: #try-except block, because not all events contain 'content'
            text = event['choices'][0]['delta']['content']
        except:
            pass
            
        Textfull += text

        yield(text)

def TTS(response):        
    generator = Generator(response)
    
    audio_stream = generate(
        text = generator,
        api_key = apiKey,
        voice = voice,
        model = model,
        stream = True
    )

    stream(audio_stream)

    return(Textfull)