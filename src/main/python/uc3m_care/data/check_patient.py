from freezegun import freeze_time
from datetime import datetime
from uc3m_care.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.enum.enumerations import Dict_Data, Mess_Error
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

class Check_Patient():
    def check_patient_data(patient_from_input: dict, patient_from_storage: dict) -> str:
        guid = patient_from_storage[Dict_Data.KEY_LABEL_VACCINE_PATIENT_ID.value]
        name = patient_from_storage[Dict_Data.KEY_LABEL_VACCINE_NAME.value]
        reg_type = patient_from_storage[Dict_Data.KEY_LABEL_VACCINE_REG_TYPE.value]
        phone = patient_from_storage[Dict_Data.KEY_LABEL_VACCINE_PATIENT_PHONE.value]
        patient_timestamp = patient_from_storage[Dict_Data.KEY_LABEL_TIME.value]
        age = patient_from_storage[Dict_Data.KEY_LABEL_AGE.value]
        # set the date when the patient was registered for checking the md5
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
        freezer.stop()
        if patient.patient_system_id != patient_from_input[Dict_Data.KEY_LABEL_PATIENT_SYS_ID.value]:
            raise VaccineManagementException(Mess_Error.ERR_MESS_PATIENT_DATA_MANIPULATED.value)
        return guid