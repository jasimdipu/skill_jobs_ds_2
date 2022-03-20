import csv
import os
import shutil
import sqlite3
from os import listdir

from application_loggin.logger import App_Logger


class DBOperation:
    """
    This class created for handling all the perdiction data using sql
    """

    def __init__(self):
        self.path = "Prediction_Database/"
        self.good_path = "Prediction_Raw_Files/Good_Raw"
        self.bad_path = "Prediction_Raw_Files/Bad_Raw"
        self.logger = App_Logger()

    def database_connection(self, DatabaseName):

        try:
            conn = sqlite3.connect(self.path + DatabaseName + '.db')
            file = open("Prediction_Logs/DatabaseConnectionLog.txt", "a+")
            self.logger.log(file, "Opened %s database successfully " % DatabaseName)
            file.close()
        except ConnectionError as e:
            file = open("Prediction_Logs/DatabaseConnectionLog.txt", "a+")
            self.logger.log(file, "Error while connecting the database: %s" % ConnectionError)
            file.close()
            raise ConnectionError

    def createDbTable(self, DatabaseName, column_names):

        """
        create data table into database
        :param DatabaseName:
        :param column_names:
        :return:
        """

        try:
            conn = self.database_connection(DatabaseName)
            conn.execute("DROP TABLE IF EXISTS Good_Raw_Data")

            for key in column_names.keys():
                type = column_names[key]

                try:
                    conn.execute(
                        'ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,
                                                                                                 dataType=type))
                except:
                    conn.execute(
                        'CREATE TABLE Good_Raw_Data ({column_name} {dataType}'.format(column_name=key, dataType=type))
            conn.close()
            file = open("Prediction_Logs/dbTableCreateLog.txt", "a+")
            self.logger.log(file, "Create table successfully")
            file.close()

            file = open("Prediction_Logs/DatabaseCreateLog.txt", "a+")
            self.logger.log(file, "Closed %s successfully " % DatabaseName)
            file.close()
        except Exception as e:
            file = open("Prediction_Logs/dbTableCreateLog.txt", "a+")
            self.logger.log(file, "Error while creating table" % e)
            file.close()
            conn.close()

            file = open("Prediction_Logs/DatabaseCreateLog.txt", "a+")
            self.logger.log(file, "Closed %s successfully" % DatabaseName)
            file.close()
            raise e

    def inserGoodDatatIntoDb(self, DatabaseName):
        """
        insert good data into Good_Raw_Data table
        :param DatabaseName:
        :return:
        """
        conn = self.database_connection(DatabaseName)
        goodFilePath = self.good_path
        badFilePath = self.bad_path

        onlyFiles = [f for f in listdir(goodFilePath)]

        log_file = open("Prediction_Logs/DBInsertLog.txt", "a+")

        for file in onlyFiles:
            try:
                with open(goodFilePath + '/' + file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute("INSERT INTO Good_Ras_Data VALUES({values}".format(values=list_))
                                self.logger.log(log_file, "%s : File loaded successfully" % file)
                                conn.commit()
                            except Exception as e:
                                raise e
            except Exception as e:
                conn.rollback()
                self.logger.log(log_file, "%s : Error while loaded data into database" % e)
                shutil.move(goodFilePath + '/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()
                raise e
        conn.close()
        log_file.close()

    def selectingDataFromTableIntoCSV(self, DatabaseName):
        """
        export data from table into csv format file
        :param DatabaseName:
        :return:
        """

        self.fileFromDb = "Prediction_FileFromDB/"
        self.fileName = "InputFile.csv"
        log_file = open("Predition_Logs/ExportToCsv.txt", "a+")

        try:
            conn = self.database_connection(DatabaseName)
            sql = "SELECT * FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sql)

            res = cursor.fetchall()

            headers = [i[0] for i in cursor.description]

            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            csvFile = csv.writer(open(self.fileFromDb + self.fileFromDb + self.fileName, "w", newline=""),
                                 delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_ALL, escapechar='\\')

            csvFile.writerow(headers)
            csvFile.writerows(res)

            self.logger.log(log_file, "File exported successfully")

        except Exception as e:
            self.logger.log(log_file, "File exporting failed : %s" % e)
            raise e
