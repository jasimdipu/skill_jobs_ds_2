class pred_validation:

    def __init__(self, path):
        self.raw_data = Prediction_Data_Validation(path)
        self.dataTransformation = dataTransformationPredict()
        self.dbOparation = dbOperation()
        self.file_object = open("Prediction_Logs/Prediction_log.txt", "a+")
        self.log_writer = logger.App_Logger()