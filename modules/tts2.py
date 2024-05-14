from io import BytesIO

from gtts import gTTS, lang
from pygame import mixer

from modules import ftl

mixer.init()


def set_lang(text, lm=False):
    return ftl.detect_lang(text.replace('\n', ' '), lm)['lang']


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
