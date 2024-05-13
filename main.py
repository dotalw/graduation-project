import cv2
from google.cloud import vision
from google.oauth2 import service_account
import pyttsx3
import os
import time
import threading

# Specify the path to the service account key JSON file
service_account_key_path = os.path.join(os.path.dirname(__file__), 'yourkey.json')

# Initialize Google Cloud Vision client with service account key
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
client = vision.ImageAnnotatorClient(credentials=credentials)


# Function to perform OCR on image using Google Cloud Vision API
def ocr_image(image):
    try:
        _, encoded_image = cv2.imencode('.jpg', image)
        content = encoded_image.tobytes()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            return texts[0].description
        else:
            return "No text detected"
    except Exception as e:
        print("Error in OCR:", e)
        return "Error"


# Function to convert text to speech and play it directly
def text_to_speech(text, lang='en'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if len(voice.languages) > 0 and voice.languages[0] == lang:
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1.0)
    engine.setProperty('pitch', 0.5)
    engine.say(text)
    engine.runAndWait()


# Function to detect language from text
def detect_language(text):
    if 'ar' in text.lower():
        return 'ar'
    elif 'fr' in text.lower():
        return 'fr'
    else:
        return 'en'


# Function to read video frames and perform OCR
def process_video():
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # Allow the camera to initialize and focus
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't capture frame")
            break
        text = ocr_image(frame)
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Video', frame)
        if text != "No text detected" and text != "Error":
            lang = detect_language(text)
            threading.Thread(target=text_to_speech, args=(text, lang)).start()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


# Main function to start video processing
if __name__ == '__main__':
    process_video()
