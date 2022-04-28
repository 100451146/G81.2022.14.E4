"""Global constants for finding the path"""
from pathlib import Path
JSON_FILES_PATH = str(Path.home()) + "/PycharmProjects/G81.2022.14.E4/src/JsonFiles/"
JSON_FILES_RF2_PATH = JSON_FILES_PATH + "/RF2/"

PATIENTS_STORE = JSON_FILES_PATH + "store_patient.json"
APPOINTMENTS_STORE = JSON_FILES_PATH + "store_date.json"
VACCINES_STORE = JSON_FILES_PATH + "store_vaccine.json"
