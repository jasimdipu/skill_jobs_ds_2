from os import listdir

import pandas as pd

from application_loggin.logger import App_Logger


class DataTransformPrediction():

    def __init__(self):
        self.goodDataPath = "Prediction_Raw_Files_Validation/Good_Raw"
        self.logger = App_Logger()

    def replaceMissingWithNull(self):

        try:
            log_file = open("Prediction_Logs/dataTransformLog.txt", "a+")
            onlyfiles = [f for f in listdir(self.goodDataPath)]
            for file in onlyfiles:
                csv = pd.read_csv(self.goodDataPath + "/" + file)
                csv.fillna("NULL", inplace=True)
                csv['wafer'] = csv['wafer'].str[6:]
                csv.to_csv(self.goodDataPath + "/" + file, index=None, header=True)
                self.logger.log(log_file, "%s: file transform successfully !!" % file)

        except Exception as e:
            self.logger.log(log_file, "%s: data transform failed because !!" % e)
            log_file.close()
            raise e
        log_file.close()
