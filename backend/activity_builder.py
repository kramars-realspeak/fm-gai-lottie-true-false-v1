"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains the builder class for fm-gai-lottie-true-false-v1 activity objects.
"""


import uuid
from backend.helpers import import_activity_data
from backend.image_generator import ImageGenerator


class FMGAILottieTrueFalseActivityBuilder:
    def __init__(self, activity):
        self.activity = activity
        self.data = import_activity_data()

    def set_id(self):
        self.activity.id = str(uuid.uuid4())
        return self

    def set_media(self):
        self.activity.media = {
            "style": self.data['media'].get("style"),
            "image_src": None
        }
        return self
    
    def set_image_src(self):
        "Generates an image based on the activity style."
        image_generator = ImageGenerator(self.data)
        image_url = image_generator.generate_image()
        self.activity.media['image_src'] = image_url
        return self
    
    def set_sentence(self):
        self.activity.sentence = self.data["sentence"]
        return self

    def set_correct_answer(self):
        self.activity.correct_answer = self.data["correct_answer"]
        return self
    
    def set_cefr_level(self):
        self.activity.cefr_level = self.data["cefr_level"]
        return self
    
    def set_target_vocabulary(self):
        self.activity.target_vocabulary = self.data["target_vocabulary"]
        return self
    
    def set_target_grammar(self):
        self.activity.target_grammar = self.data["target_grammar"]
        return self
    
    def set_submitted(self):
        self.activity.submitted = False
        return self
    
    def set_metadata(self):
        self.activity.metadata = {
            "model_alias": self.data["metadata"].get("model_alias"),
            "model_version": self.data["metadata"].get("model_version")
        }
        return self
    
    def build(self):
        return self.activity