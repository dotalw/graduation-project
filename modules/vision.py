import cv2
from google.cloud import vision
from google.oauth2 import service_account


class Vision:
    def __init__(self, config):
        # Initialize Google Cloud Vision client with service account key
        credentials = service_account.Credentials.from_service_account_file(config.get('GCLOUD_KEY'))
        self.client = vision.ImageAnnotatorClient(credentials=credentials)

    def get_ocr(self, frame):
        try:
            _, encoded_image = cv2.imencode('.jpg', frame)
            content = encoded_image.tobytes()
            image = vision.Image(content=content)
            response = self.client.text_detection(image=image)
            texts = response.text_annotations
            if texts:
                return texts[0].description
            else:
                return "No text detected"
        except Exception as e:
            print("Error in OCR:", e)
            return "Error"
