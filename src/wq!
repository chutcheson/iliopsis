import uuid
import argparse
from uuid import uuid4
from dataclasses import dataclass

import requests

from openai_client import client
from utilities import downsample_image

@dataclass
class ImageResult:
    prompt: str
    image: bytes
    uuid: str 
    path: str
    url: str

### GENERATE IMAGE

def generate_image(prompt):

    image_uuid = str(uuid.uuid4())
    image_path = f"../data/{image_uuid}.jpg"

    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      n=1,
      size="1024x1024"
    )

    image_url = response.data[0].url

    image = download_image(image_url, image_path)
    downsampled_image = downsample_image(image)

    return ImageResult(prompt, downsampled_image, str(uuid4()), image_path, image_url)

### DOWNLOAD IMAGE

def download_image(url, filename):
    response = requests.get(url)
    file = open(filename, "wb")
    file.write(response.content)
    file.close()
    return response.content

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('--prompt', type=str, help='A prompt for the script')
    args = parser.parse_args()
    prompt = args.prompt
    image_dict = generate_image(prompt)
    print(image_dict)

