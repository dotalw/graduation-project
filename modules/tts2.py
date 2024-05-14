from io import BytesIO

from ftlangdetect import detect
from gtts import gTTS, lang
from pygame import mixer

mixer.init()


def detect_lang(text, lm=False):
    return detect(text=text, low_memory=lm)


def set_lang(text, lm=False):
    return detect_lang(text.replace('\n', ' '), lm)['lang']


def speak(text, slow=False, lm=False):
    if not text:
        return
    dlang = set_lang(text, lm)
    if dlang not in lang.tts_langs():
        dlang = 'en'
    mp3_fp = BytesIO()
    gt = gTTS(text, lang=dlang, slow=slow)
    gt.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    mixer.music.load(mp3_fp, "mp3")
    mixer.music.play()
