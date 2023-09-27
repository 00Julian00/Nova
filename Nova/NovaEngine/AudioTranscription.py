import speech_recognition as sr
from Levenshtein import distance #Used to check if a word is "close enough" to the hotword
import ConfigInteraction

#Constants
hotword = ConfigInteraction.GetSetting("Hotword")
language = ConfigInteraction.GetSetting("Language")
micIndex = int(ConfigInteraction.GetSetting("MicrophoneIndex"))
max_distance = 3

r = sr.Recognizer()
def DetectHotword(transcription, hotword, max_distance):
    #Check how much every word in the description deviates from the hotword. If it is close enough, it will be counted
    words = transcription.lower().split()
    hotword = hotword.lower()
    for i, word in enumerate(words):
        if distance(word, hotword) <= max_distance:
            words[i] = hotword  # replace with the actual hotword
    return ' '.join(words)  # join the words back into a string


def Listen():
    print("Listening for Hotword...")
    while True:
        # open the microphone and start listening
        with sr.Microphone(device_index=micIndex) as source:
            audio = r.listen(source)

        # use Google's Speech-to-Text API to recognize the speech
        try:
            transcription = r.recognize_google(audio, language= language.lower() + "-" + language.upper())
            print(transcription)

            transcription = DetectHotword(transcription, hotword, max_distance)

            if (hotword.lower() in transcription):
                #Send to main code that the hotword has been detected and also pass the transcript
                print("Hotword detected")
                return transcription

        except sr.UnknownValueError:
            pass
            #print("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))