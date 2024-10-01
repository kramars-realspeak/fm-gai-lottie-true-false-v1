"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains the builder class for fm-gai-lottie-true-false-v1 activity objects.
"""


import uuid
from backend.helpers import import_activity_data
from backend.image_generator import ImageGenerator
from backend.helpers import setup_logger


class FMGAILottieTrueFalseActivityBuilder:
    def __init__(self, activity):
        self.activity = activity
        self.data = import_activity_data()
        self.logger = setup_logger()

    def set_id(self):
        self.activity.id = str(uuid.uuid4())
        self.logger.info(f"{self.__class__.__name__}: 'set_activity_id' method invoked - Activity ID set to: {self.activity.id}")
        return self

    def set_media(self):
        self.activity.media = {
            "style": self.data['media'].get("style"),
            "image_src": None
        }
        self.logger.info(f"{self.__class__.__name__}: 'set_media' method invoked - Media set to: {self.activity.media}")
        return self
    
    def set_image_src(self):
        "Generates an image based on the activity style."
        image_generator = ImageGenerator(self.data)
        image_url = image_generator.generate_image(image_id=self.activity.id)
        self.activity.media['image_src'] = image_url
        self.logger.info(f"{self.__class__.__name__}: 'set_image_src' method invoked - Image URL set to: {image_url}")
        return self
    
    def set_sentence(self):
        self.activity.sentence = self.data["sentence"]
        self.logger.info(f"{self.__class__.__name__}: 'set_sentence' method invoked - Sentence set to: {self.activity.sentence}")
        return self

    def set_correct_answer(self):
        self.activity.correct_answer = self.data["correct_answer"]
        self.logger.info(f"{self.__class__.__name__}: 'set_correct_answer' method invoked - Correct answer set to: {self.activity.correct_answer}")
        return self
    
    def set_cefr_level(self):
        self.activity.cefr_level = self.data["cefr_level"]
        self.logger.info(f"{self.__class__.__name__}: 'set_cefr_level' method invoked - CEFR level set to: {self.activity.cefr_level}")
        return self
    
    def set_target_vocabulary(self):
        self.activity.target_vocabulary = self.data["target_vocabulary"]
        self.logger.info(f"{self.__class__.__name__}: 'set_target_vocabulary' method invoked - Target vocabulary set to: {self.activity.target_vocabulary}")
        return self
    
    def set_target_grammar(self):
        self.activity.target_grammar = self.data["target_grammar"]
        self.logger.info(f"{self.__class__.__name__}: 'set_target_grammar' method invoked - Target grammar set to: {self.activity.target_grammar}")
        return self
    
    def set_submitted(self):
        self.activity.submitted = False
        self.logger.info(f"{self.__class__.__name__}: 'set_submitted' method invoked - Submitted set to: {self.activity.submitted}")
        return self
    
    def set_metadata(self):
        self.activity.metadata = {
            "model_alias": self.data["metadata"].get("model_alias"),
            "model_version": self.data["metadata"].get("model_version")
        }
        self.logger.info(f"{self.__class__.__name__}: 'set_metadata' method invoked - Metadata set to: {self.activity.metadata}")
        return self
    
    def build(self):
        return self.activity