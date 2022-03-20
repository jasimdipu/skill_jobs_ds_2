from PredictionRawDataValidation.prediction_data_validation import PredictionDataValidation
from application_loggin.logger import App_Logger
from DataTransformation_Prediction.DataTransformationPrediction import DataTransformPrediction
from Prediction_Database.db_operation import DBOperation


class pred_validation:

    def __init__(self, path):
        self.raw_data = PredictionDataValidation(path)
        self.dataTransformation = DataTransformPrediction()
        self.dbOparation = DBOperation()
        self.file_object = open("Prediction_Logs/Prediction_log.txt", "a+")
        self.log_writer = App_Logger()

