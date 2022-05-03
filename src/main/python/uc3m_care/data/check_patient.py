from datetime import datetime
from freezegun import freeze_time

from uc3m_care.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.enum.enumerations import DictData, MessError
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class CheckPatient:
    @staticmethod
    def check_patient_data(patient_from_input: dict, patient_from_storage: dict) -> str:
        guid = patient_from_storage[DictData.KEY_LABEL_VACCINE_PATIENT_ID.value]
        name = patient_from_storage[DictData.KEY_LABEL_VACCINE_NAME.value]
        reg_type = patient_from_storage[DictData.KEY_LABEL_VACCINE_REG_TYPE.value]
        phone = patient_from_storage[DictData.KEY_LABEL_VACCINE_PATIENT_PHONE.value]
        patient_timestamp = patient_from_storage[DictData.KEY_LABEL_TIME.value]
        age = patient_from_storage[DictData.KEY_LABEL_AGE.value]
        # set the date when the patient was registered for checking the md5
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
        freezer.stop()
        if patient.patient_system_id != patient_from_input[DictData.KEY_LABEL_PATIENT_SYS_ID.value]:
            raise VaccineManagementException(MessError.ERR_MESS_PATIENT_DATA_MANIPULATED.value)
        return guid
