from ftlangdetect import detect


def detect_lang(text, lm=False):
    return detect(text=text, low_memory=lm)
