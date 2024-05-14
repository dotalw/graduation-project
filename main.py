import argparse
import threading

import cv2
from dotenv import dotenv_values

from modules.camera import Camera
from modules.tts import TTS
from modules.tts2 import speak as tts2
from modules.vision import Vision

config = dotenv_values('.env')

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--preview', action='store_true', help='An optional argument for preview')
parser.add_argument('--gtts', action='store_true', help='Enable gTTS instead of pyttsx4')
parser.add_argument('--slow', action='store_true', help='Force gTTS to read slower')
parser.add_argument('--low-mem', action='store_true')
args = parser.parse_args()

if not args.gtts:
    tts = TTS(low_memory=args.low_mem)


def process_video():
    while True:
        frame = cam.capture_frame()
        text = vision.get_ocr(frame)
        if args.preview:
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Video', frame)
        if text != "No text detected" and text != "Error":
            if args.gtts:
                tts2(text, slow=args.slow, lm=args.low_mem)
            else:
                threading.Thread(target=tts.speak, args=(' '.join(text),)).start()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


# Main function to start video processing
if __name__ == '__main__':
    vision = Vision(config)
    cam = Camera()
    process_video()
