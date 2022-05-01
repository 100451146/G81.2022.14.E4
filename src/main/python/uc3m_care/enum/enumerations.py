from enum import Enum

class Mess_Error(Enum):
    #Class for messages on VaccineManagementException
    ERR_MESS_STORE_PATIENT_NOT_FOUND = "Store_patient not found"
    ERR_MESS_FILE_NOT_FOUND = "File is not found"
    ERR_MESS_STORE_DATE_NOT_FOUND = "Store_date not found"
    ERR_MESS_WRONG_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"
    ERR_MESS_WRONG_FILE = "Wrong file or file path"
    ERR_MESS_PATIENT_SYSID_NOT_FOUND = "patient_system_id is not found"
    ERR_MESS_DATE_NOT_FOUND = "date_signature is not found"
    ERR_MESS_PATIENT_REGISTERED = "patien_id is registered in store_patient"
    ERR_MESS_PATIENT_DATA_MANIPULATED = "Patient's data have been manipulated"

class Dict_Data(Enum):
    KEY_LABEL_VACC_PATIENT_SYS_ID = "_VaccinePatientRegister__patient_sys_id"
    KEY_LABEL_PATIENT_SYS_ID = "PatientSystemID"
    KEY_LABEL_DATE_SIGNATURE = "_VaccinationAppoinment__date_signature"
    KEY_LABEL_DATE_APPOINTMENT_DATE = "_VaccinationAppoinment__appoinment_date"
    KEY_LABEL_VACCINE_PATIENT_ID = "_VaccinePatientRegister__patient_id"
    KEY_LABEL_VACCINE_REG_TYPE = "_VaccinePatientRegister__registration_type"
    KEY_LABEL_VACCINE_NAME = "_VaccinePatientRegister__full_name"

