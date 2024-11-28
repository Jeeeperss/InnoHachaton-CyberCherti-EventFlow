import json
import time
import requests
import base64

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def save_image(self, image_base64, filename):
        image_data = base64.b64decode(image_base64)
        with open(filename, 'wb') as file:
            file.write(image_data)
        print(f'Image saved as {filename}')

async def generate(prompt: str):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'API', 'SECRET')
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images_base64 = api.check_generation(uuid)
    if images_base64:
        for idx, img_base64 in enumerate(images_base64):
            api.save_image(img_base64, f'images/image.png')
    else:
        print("Image generation failed.")
