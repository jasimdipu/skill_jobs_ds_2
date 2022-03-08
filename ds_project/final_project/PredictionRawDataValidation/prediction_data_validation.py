import json
import os
import shutil
from datetime import datetime

from application_loggin.logger import App_Logger


class PredictionDateValidation():
    """
    this file is used for handling all the validation done on the Raw prediction data
    """

    def __init__(self, path):
        self.BatchDirectory = path
        self.schemaPath = "schema_prediction.json"
        self.logger = App_Logger()

    def valuesFromSchema(self):
        try:
            with open(self.schemaPath, 'r') as f:
                dic = json.load(f)
                f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            columns_name = dic['ColName']
            NumberofColumns = dic['NumberofColumns']

            file = open("Training_Logs/valuesFromSchemaValidationLog.txt", "a+")
            message = "LengthOfDateStampInFile::%s" % LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile
            self.logger.log(file, message)
            file.close()

        except ValueError:
            file = open("Prediction_logs/valuesFromSchemaValidationLog.txt", "a+")
            self.logger.log(file, "ValueError: Value not found inside the schema file")
            file.close()
            raise ValueError

        except KeyError:
            file = open("Prediction_logs/valuesFromSchemaValidationLog.txt", "a+")
            self.logger.log(file, "KeyError: Key Value error incorrect key passing")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Prediction_logs/valuesFromSchemaValidationLog.txt", "a+")
            self.logger.log(file, str(e))
            file.close()
            raise KeyError

    def createGoodOrBadDataFolder(self):

        """
        this function is use for create good and bad raw data folder
        :return:
        """

        try:
            path = os.path.join("Predicted_Raw_Files_Validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Predicted_Raw_Files_Validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
        except OSError as e:
            file = open("Prediction_logs/General_Log.txt", "a+")
            self.logger.log(file, "Error while creating the directory")
            file.close()
            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):

        try:
            path = "Predicted_Raw_Files_Validated/"
            if os.path.isdir(path + "Good_Raw"):
                shutil.rmtree(path + "Good_Raw")
                file = open("Prediction_Logs/General_Log.txt", "a+")
                self.logger.log(file, "Error while creating the directory")
                file.close()
        except OSError as e:
            file = open("Prediction_logs/General_Log.txt", "a+")
            self.logger.log(file, "Error while creating the directory")
            file.close()
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):

        try:
            path = "Predicted_Raw_Files_Validated/"
            if os.path.isdir(path + "Bad_Raw"):
                shutil.rmtree(path + "Bad_Raw")
                file = open("Prediction_Logs/General_Log.txt", "a+")
                self.logger.log(file, "Error while creating the directory")
                file.close()
        except OSError as e:
            file = open("Prediction_logs/General_Log.txt", "a+")
            self.logger.log(file, "Error while creating the directory")
            file.close()
            raise OSError

    def moveBadFilesToArchiveBad(self):

        """
        bad raw data recycle bin
        :return:
        """

        now = datetime.now()
        date = now.date()
        time = now.strftime("%H:%M:%S")

        try:
            path = "PredictionArchiveBadData"
            if not os.path.isdir(path):
                os.makedirs(path)
            source = "Predicted_Raw_Files_Validated/Bad_Raw/"
            destination = "PredictionArchiveBadData/Bad_Data_" + str(date) + "_" + str(time)
            if not os.path.isdir(destination):
                os.makedirs(destination)
            files = os.listdir(source)
            for f in files:
                if f not in os.listdir(destination):
                    shutil.move(source + f, destination)
            file = open("Prediction_logs/General_Log.txt", "a+")
            self.logger.log(file, "Bad files move to the archive")

            path = "Predicted_Raw_Files_Validated/"
            if os.path.isdir(path + "Bad_Raw"):
                shutil.rmtree(path + "Bad_Raw")
                file = open("Prediction_Logs/General_Log.txt", "a+")
                self.logger.log(file, "Bad Raw folder detected successfully")
                file.close()

        except OSError as e:
            file = open("Prediction_Logs/General_Log.txt", "a+")
            self.logger.log(file, "Error while moving the bad raw files to archive:: %s" % e)
            file.close()
            raise OSError

        except Exception as e:
            file = open("Prediction_Logs/General_Log.txt", "a+")
            self.logger.log(file, "Error while moving the bad raw files to archive:: %s" % e)
            file.close()
