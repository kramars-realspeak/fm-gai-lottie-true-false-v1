"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains a function that generates an image based on a given sentence and target vocabulary and grammar.

Requirements:
    - openai # pip install openai / python -m pip install openai

Validate package installation by running the following commands:
    - python -c "import openai"
    - python -m openai validate
"""

import openai
import requests
import os
# from datetime import datetime
from openai import OpenAI


class ImageGenerator:
    def __init__(self, activity_data):
        self.activity_data = activity_data
        self.image_size = "1024x1024"

    def craft_prompt(self):
        """Crafts a prompt for DALL-E based on the input data structure."""
        print("Crafting prompt...")
        print(f"Activity data: {self.activity_data}")
        sentence = self.activity_data.get("sentence")
        target_vocabulary = self.activity_data.get("target_vocabulary", [])
        target_grammar = self.activity_data.get("target_grammar", [])
        style = self.activity_data['media'].get('style')
        action_phrase = sentence
        prompt = (
            f"An image showing a scene where a {', '.join(target_vocabulary)} are involved. "
            f"The scene should depict: {action_phrase}"
            f"Style: {style}."
        )
        print(f"Crafted prompt: {prompt}")
        return prompt

    def generate_image(self):
        try:
            print("Generating image...")
            key=""
            client = OpenAI(api_key=key)
            prompt = self.craft_prompt()
            response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=self.image_size,
            quality="standard",
            n=1,
            )
            image_url = response.data[0].url
            # timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            # image_filename = os.path.join(output_folder, f"{timestamp}.png")
            # img_data = requests.get(image_url).content
            # with open(image_filename, 'wb') as image_file:
            #     image_file.write(img_data)
            print(f"Image generated successfully: {image_url}")
            return image_url

        except Exception as e:
            print(f"Error generating image: {e}")
            return None