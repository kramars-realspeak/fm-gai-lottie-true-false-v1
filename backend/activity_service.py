"""
Author : Peter Kramar
Email : peter@ked.tech
This module contains the service class for the fm-gai-lottie-true-false-v1 activity.
"""


from backend.activity import Activity
from backend.activity_builder import FMGAILottieTrueFalseActivityBuilder
from backend.text_analyzer import TextAnalyzer
from backend.helpers import export_activity_data
from backend.helpers import append_activity_data_to_dataset
from backend.helpers import setup_logger
from backend.helpers import rename_log_file_to_activity_id
from backend.helpers import upload_log_file_to_s3
from backend.helpers import initialize_activity_data


class ActivityService:
    def __init__(self):
        self.builder = FMGAILottieTrueFalseActivityBuilder(Activity())
        self.logger = setup_logger()

    def analyze_activity(self):
        sentence = self.builder.data.get("sentence")
        self.logger.info(f"{self.__class__.__name__}: Invoking 'analyze_sentence' method for sentence: '{sentence}'")
        text_analyzer = TextAnalyzer(sentence)
        text_analyzer.assess_sentence_language_level_cefrpy()

    def build_activity_object(self, activity_data=None):
        if activity_data:
            self.builder.data = activity_data
        
        print("Activity data:")
        print(self.builder.data)

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
        
        activity_dict = activity.to_dict()

        print("Activity dict:")
        print(activity_dict)

        export_activity_data(activity_dict)
        append_activity_data_to_dataset(activity_dict)
        rename_log_file_to_activity_id(self.logger, activity.id)
        upload_log_file_to_s3(activity.id)
        return activity
    
    def generate_activity(self, level, vocabulary):
        self.logger.info(f"{self.__class__.__name__}: Invoking 'generate_activity' method")
        activity_data = initialize_activity_data(level, vocabulary)
        print("Activity data:")
        print(activity_data)
        activity = self.build_activity_object(activity_data=activity_data)
        return {
            "activity_id": activity.id,
            "status": "success",
            "message": "Activity generated successfully. Exported to data/output.json"
        }

    def build_activity(self):
        self.logger.info(f"{self.__class__.__name__}: Invoking 'build_activity' method")
        activity = self.build_activity_object()
        return {
        "id": activity.id,
        "status": "success",
        "message": "Activity built successfully. Exported to data/output.json."
    }
