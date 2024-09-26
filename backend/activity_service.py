"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains the service class for the fm-gai-lottie-true-false-v1 activity.
"""


from backend.activity import Activity
from backend.activity_builder import FMGAILottieTrueFalseActivityBuilder
from backend.text_analyzer import TextAnalyzer
from backend.helpers import export_activity_data


class ActivityService:
    def __init__(self):
        self.builder = FMGAILottieTrueFalseActivityBuilder(Activity())

    def analyze_activity(self):
        sentence = self.builder.data.get("sentence")
        print(f"Analyzing sentence: {sentence}")
        text_analyzer = TextAnalyzer(sentence)
        text_analyzer.assess_sentence_language_level_cefrpy()

    def build_activity(self):
        activity = (
            self.builder.set_id()
                        .set_media()
                        .set_image_src()
                        .set_sentence()
                        .set_correct_answer()
                        .set_cefr_level()
                        .set_target_vocabulary()
                        .set_target_grammar()
                        .set_submitted()
                        .set_metadata()
                        .build()
        )
        print(f"Activity built: {activity}")
        activity_dict = activity.to_dict()
        print(f"Activity dict: {activity_dict}")
        export_activity_data(activity_dict)
        return {
        "id": activity.id,
        "status": "success",
        "message": "Activity built successfully. Exported to data/output.json."
    }
