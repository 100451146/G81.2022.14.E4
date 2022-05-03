from enum import Enum


class MessError(Enum):
    # Class for VaccineManagementException's messages
    ERR_MESS_STORE_PATIENT_NOT_FOUND = "Store_patient not found"
    ERR_MESS_FILE_NOT_FOUND = "File is not found"
    ERR_MESS_STORE_DATE_NOT_FOUND = "Store_date not found"
    ERR_MESS_WRONG_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"
    ERR_MESS_WRONG_FILE = "Wrong file or file path"
    ERR_MESS_PATIENT_SYSID_NOT_FOUND = "patient_system_id is not found"
    ERR_MESS_DATE_NOT_FOUND = "date_signature is not found"
    ERR_MESS_PATIENT_REGISTERED = "patien_id is registered in store_patient"
    ERR_MESS_PATIENT_DATA_MANIPULATED = "Patient's data have been manipulated"


class DictData(Enum):
    # Class for dictionary keys
    KEY_LABEL_VACC_PATIENT_SYS_ID = "_VaccinePatientRegister__patient_sys_id"
    KEY_LABEL_PATIENT_SYS_ID = "PatientSystemID"
    KEY_LABEL_PHONE_NUMBER = "ContactPhoneNumber"
    KEY_LABEL_DATE_SIGNATURE = "_VaccinationAppoinment__date_signature"
    KEY_LABEL_DATE_APPOINTMENT_DATE = "_VaccinationAppoinment__appoinment_date"
    KEY_LABEL_VACCINE_PATIENT_ID = "_VaccinePatientRegister__patient_id"
    KEY_LABEL_VACCINE_REG_TYPE = "_VaccinePatientRegister__registration_type"
    KEY_LABEL_VACCINE_NAME = "_VaccinePatientRegister__full_name"
    KEY_LABEL_TIME = "_VaccinePatientRegister__time_stamp"
    KEY_LABEL_AGE = "_VaccinePatientRegister__age"
    KEY_LABEL_VACCINE_PATIENT_PHONE = "_VaccinePatientRegister__phone_number"


class MessAttr(Enum):
    # Class for Attributes messages
    MESS_NOT_DAY = "Today is not the date"
    MESS_AGE_INVALID = "age is not valid"
    MESS_NAME_INVALID = "name surname is not valid"
    MESS_PHONE_INVALID = "phone number is not valid"
    MESS_REGISTRATION_INVALID = "Registration type is nor valid"
    MESS_UUID_INVALID = "UUID invalid"
    MESS_NOT_UUID = "Id received is not a UUID"
    MESS_MD5_INVALID = "patient system id is not valid"
    MESS_SHA256_INVALID = "date_signature format is not valid"
    MESS_BAD_LABEL_PHONE = "Bad label contact phone"
    MESS_BAD_LABEL_PATIENT_ID = "Bad label patient_id"


class CorrectPattern(Enum):
    # Class for attribute pattern
    NAME_PATTERN = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    PHONE_PATTERN = r"^(\+)[0-9]{11}"
    REGISTRATION_PATTERN = r"(Regular|Family)"
    UUID_PATTERN = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]" \
                   r"{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
    MD5_PATTERN = r"[0-9a-fA-F]{32}$"
    SHA256_PATTERN = r"[0-9a-fA-F]{64}$"
