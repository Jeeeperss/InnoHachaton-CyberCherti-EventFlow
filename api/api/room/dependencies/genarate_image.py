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

    def check_generation(self, request_id, max_attempts=10, initial_delay=2):
        delay = initial_delay
        for attempt in range(max_attempts):
            response = requests.get(self.URL + f'key/api/v1/text2image/status/{request_id}', headers=self.AUTH_HEADERS)
            data = response.json()
            if data.get('status') == 'DONE':
                return data['images']
            time.sleep(delay)
            delay = min(delay * 2, 10)  # Увеличиваем задержку, но не более 10 секунд
        raise TimeoutError("Image generation timed out")


    def save_image(self, image_base64, filename):
        image_data = base64.b64decode(image_base64)
        with open(filename, 'wb') as file:
            file.write(image_data)
        print(f'Image saved as {filename}')

async def generate(prompt: str, room_id: int):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'api', 'secret')
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    images_base64 = api.check_generation(uuid)
    if images_base64:
        for idx, img_base64 in enumerate(images_base64):
            api.save_image(img_base64, f'../html/images/image_room_{room_id}.png')
    else:
        print("Image generation failed.")
