import pyttsx4

from modules import ftl


class TTS:
    def __init__(self, low_memory=False):
        self.low_mem = low_memory
        self.engine = pyttsx4.init()
        self.voices = self.engine.getProperty('voices')
        self.default_voice = self.set_voice(lang='en')

    def set_voice(self, lang):
        for voice in self.voices:
            if len(voice.languages) > 0 and lang in voice.languages[0].decode('utf-8'):
                self.engine.setProperty('voice', voice.id)
                return voice.id
        return None

    def set_lang(self, text):
        detected_lang = ftl.detect_lang(text.replace('\n', ' '))['lang']
        if not self.set_voice(detected_lang):
            self.engine.setProperty('voice', self.default_voice)

    def speak(self, text):
        self.set_lang(text)
        self.engine.setProperty('rate', 120)
        self.engine.setProperty('volume', 1.0)
        self.engine.setProperty('pitch', 0.5)
        self.engine.say(text)
        self.engine.runAndWait()
