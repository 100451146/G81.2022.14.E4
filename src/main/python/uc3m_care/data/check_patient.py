from freezegun import freeze_time
from datetime import datetime
from uc3m_care.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.enum.enumerations import Dict_Data
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class Check_Patient():
    def check_patient_data(patient_from_input: dict, patient_from_storage: dict) -> str:
        guid = patient_from_storage["_VaccinePatientRegister__patient_id"]
        name = patient_from_storage["_VaccinePatientRegister__full_name"]
        reg_type = patient_from_storage["_VaccinePatientRegister__registration_type"]
        phone = patient_from_storage["_VaccinePatientRegister__phone_number"]
        patient_timestamp = patient_from_storage["_VaccinePatientRegister__time_stamp"]
        age = patient_from_storage["_VaccinePatientRegister__age"]
        # set the date when the patient was registered for checking the md5
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
        freezer.stop()
        if patient.patient_system_id != patient_from_input[Dict_Data.KEY_LABEL_PATIENT_SYS_ID.value]:
            raise VaccineManagementException("Patient's data have been manipulated")
        return guid