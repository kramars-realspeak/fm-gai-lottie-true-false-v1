"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains a function that generates an image based on a given sentence and target vocabulary and grammar.
"""

import io
import requests
import os
from openai import OpenAI
from .helpers import upload_image_to_s3, get_secret_value


class ImageGenerator:
    def __init__(self, activity_data):
        self.activity_data = activity_data
        self.image_size = "1792x1024"
         
    def craft_prompt(self):
        """Crafts a prompt for DALL-E based on the input data structure."""
        print("Crafting prompt...")
        print(f"Activity data: {self.activity_data}")
        sentence = self.activity_data.get("sentence")
        target_vocabulary = self.activity_data.get("target_vocabulary", [])
        # target_grammar = self.activity_data.get("target_grammar", [])
        style = self.activity_data['media'].get('style')
        action_phrase = sentence
        prompt = (
            f"An image showing a scene where a {', '.join(target_vocabulary)} are involved. "
            f"The scene should depict: {action_phrase}"
            f"Style: {style}."
        )
        print(f"Crafted prompt: {prompt}")
        return prompt

    def generate_image(self, image_id):
        try:
            print("Generating image...")
            key= get_secret_value('openai_key')['openai_key']
            client = OpenAI(api_key=key)
            prompt = self.craft_prompt()
            response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=self.image_size,
            quality="hd",
            n=1,
            )
            image_url = response.data[0].url
            print(f"image_id: {image_id}")
            image_filename = os.path.join(f"{image_id}.jpg") # add activity ID as image name;
            img_data = requests.get(image_url).content

                    # Use an in-memory bytes buffer to avoid saving to disk
            image_file = io.BytesIO(img_data)
            image_file.name = f"{image_id}.jpg"
            print(f"Image generated successfully: ")
            upload_image_to_s3(image_file, image_id)
            print(f"Image uploaded successfully to S3 bucket.")
            image_url = 'https://s3.eu-central-1.amazonaws.com/jskramar.materials/' + image_id
            return image_url

        except Exception as e:
            print(f"Error generating image: {e}")
            return None