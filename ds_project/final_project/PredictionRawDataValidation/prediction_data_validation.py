import json
import os
import re
import shutil
from datetime import datetime
from os import listdir

import pandas as pd

from application_loggin.logger import App_Logger


class PredictionDataValidation():
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
            column_names = dic['ColName']
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

    def manualRegexCreation(self):
        regex = "['wafer']+['\_'']+[\d_]+\.csv"
        return regex

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
                self.logger.log(file, "Good Raw directory Deleted successfully")
                file.close()
        except OSError as e:
            file = open("Prediction_logs/General_Log.txt", "a+")
            self.logger.log(file, "Error while deleting the directory")
            file.close()
            raise OSError

    def deleteExistingBadDataTrainingFolder(self):

        try:
            path = "Predicted_Raw_Files_Validated/"
            if os.path.isdir(path + "Bad_Raw"):
                shutil.rmtree(path + "Bad_Raw")
                file = open("Prediction_Logs/General_Log.txt", "a+")
                self.logger.log(file, "bad raw directory deleted successfully")
                file.close()
        except OSError as e:
            file = open("Prediction_logs/General_Log.txt", "a+")
            self.logger.log(file, "Error while deleting the directory")
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

            path = "Prediction_Raw_Files_Validation/"
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
            raise e

    def validationFileNameRaw(self, regex, lengthOfDateSampleFile, lengthOfTimeSamplefile):

        """
        this func validate the name of prediction csv file
        """

        self.deleteExistingBadDataTrainingFolder()
        self.deleteExistingGoodDataTrainingFolder()
        self.createGoodOrBadDataFolder()

        onlyfiles = [f for f in listdir(self.BatchDirectory)]

        try:
            f = open("Prediction_Logs/nameValidationLog.txt", "a+")
            for filename in onlyfiles:
                if re.match(regex, filename):
                    spliteAtDot = re.split(".csv", filename)
                    spliteAtDot = (re.split('_', spliteAtDot[0]))
                    if len(spliteAtDot[1] == lengthOfDateSampleFile):
                        if len(spliteAtDot[2] == lengthOfTimeSamplefile):
                            shutil.copy("Prediction_Batch_File/" + filename, "Prediction_Raw_Files_Validation/Good_Raw")
                            self.logger.log(f, "Valid File Name!! File moved to GoogRaw Folder :: %s" % filename)
                        else:
                            shutil.copy("Prediction_Batch_File/" + filename, "Prediction_Raw_Files_Validation/Bad_Raw")
                            self.logger.log(f, "InValid File Name!! File moved to BadRaw Folder :: %s" % filename)
                    else:
                        shutil.copy("Prediction_Batch_File/" + filename, "Prediction_Raw_Files_Validation/Good_Raw")
                        self.logger.log(f, "InValid File Name!! File moved to BadRaw Folder :: %s" % filename)
                else:
                    shutil.copy("Prediction_Batch_File/" + filename, "Prediction_Raw_Files_Validation/Good_Raw")
                    self.logger.log(f, "InValid File Name!! File moved to BadRaw Folder :: %s" % filename)
        except Exception as e:
            f = open("Prediction_Logs/nameValidationLog.txt", "a+")
            self.logger.log(f, "Error occured while validation filename ::%s" % e)
            f.close()
            raise e

    def validateColumnLength(self, numberofcolumns):

        """
        Validate the columns of dataset
        :param numberofcolumns: 
        :return: 
        """
        try:
            f = open("Prediction_Logs/columnValidationLog.txt", "a+")
            self.logger.log(f, "Column Length validation started!!")

            for file in listdir("Prediction_Raw_Files_Validation/Good_Raw/"):
                csv = pd.read_csv("Prediction_Raw_Files_Validation/Good_Raw/" + file)
                if csv.shape[1] == numberofcolumns:
                    csv.rename(columns={"Unnamed: 0:Wafer"}, inplace=True)
                    csv.to_csv("Prediction_Raw_Files_Validation/Goog_Raw/" + file, index=None, header=True)
                else:
                    shutil.move("Prediction_Raw_Files_Validation/Good_Raw/" + file,
                                "Prediction_Raw_Files_Validation/Bad_Raw")
                    self.logger.log(f, "InValid Column Length for the file!! File moved to BadRaw Folder :: %s" % file)

            self.logger.log(f, "Column Length Validation Completed")

        except OSError as e:
            f = open("Prediction_Logs/columnValidationLog.txt", "a+")
            self.logger.log(f, "Error Occurred while moving the file ::$s" % OSError)
            f.close()
            raise e
        except Exception as e:
            f = open("Prediction_Logs/columnValidationLog.txt", "a+")
            self.logger.log(f, "Error Occurred ::$s" % OSError)
            f.close()
            raise e
        f.close()

    def validateMissingValuesInWholeColumn(self):

        try:
            f = open("Prediction_Logs/missingValuesInColumn.txt", "a+")
            self.logger.log(f, "Missing values validation started")

            for file in listdir("Prediction_Raw_Files_Validation/Good_Raw"):
                csv = pd.read_csv("Prediction_Raw_Files_Validation/Good_Raw/" + file)
                count = 0

                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move("Prediction_Raw_Files_Validation/Good_Raw" + file,
                                    "Prediction_Raw_Files_Validation/Bad_Raw")
                        self.logger.log(f,
                                        "Invalid column length for the file!! File moved to bad raw folder :: %s" % file)
                        break
                if count == 0:
                    csv.rename(columns={"Unnamed: 0:Wafer"}, inplace=True)
                    csv.to_csv("Prediction_Raw_Files_Validation/Goog_Raw/" + file, index=None, header=True)

        except OSError as e:
            f = open("Prediction_Logs/columnValidationLog.txt", "a+")
            self.logger.log(f, "Error Occurred while moving the file ::$s" % OSError)
            f.close()
            raise e

        except Exception as e:
            f = open("Prediction_Logs/columnValidationLog.txt", "a+")
            self.logger.log(f, "Error Occurred ::$s" % OSError)
            f.close()
            raise e
        f.close()
