"""Module """

from .parser.appointment_parser import AppointmentParser
from .storage_mangement.appointments_storage import AppointmentsStore
from .storage_mangement.registry_storage import RegistryStore
from .storage_mangement.vaccinated_storage import VaccinationStorage
from .vaccine_patient_register import VaccinePatientRegister
from .vaccination_appoinment import VaccinationAppoinment
from uc3m_care.data.attribute_date import Date
from uc3m_care.data.hash_sha256 import SHA256
from uc3m_care.data.check_patient import CheckPatient
from uc3m_care.enum.enumerations import DictData


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=too-many-arguments
    @staticmethod
    def request_vaccination_id(patient_id: str,
                               name_surname: str,
                               registration_type: str,
                               phone_number: str,
                               age: str) -> str:
        my_patient = VaccinePatientRegister(patient_id,
                                            name_surname,
                                            registration_type,
                                            phone_number,
                                            age)

        RegistryStore.save_patient_in_storage(my_patient)

        return my_patient.patient_sys_id

    @staticmethod
    def get_vaccine_date(input_file: str) -> str:
        """Gets an appointment for a registered patient"""

        patient = AppointmentsStore.load_patient_file(input_file)

        AppointmentParser.validate_system_id_label(patient)
        AppointmentParser.validate_phone_label(patient)

        patient_found = RegistryStore.search_patient_on_storage(patient)

        patient_guid = CheckPatient.check_patient_data(patient, patient_found)
        my_sign = VaccinationAppoinment(patient_guid, patient[DictData.KEY_LABEL_PATIENT_SYS_ID.value],
                                        patient[DictData.KEY_LABEL_PHONE_NUMBER.value], 10)
        # save the date in store_date.json
        AppointmentsStore.save_vaccination_appointment(my_sign)
        return my_sign.date_signature

    @staticmethod
    def vaccine_patient(date_signature: str) -> True:
        """Register the vaccination of the patient"""

        SHA256(date_signature)
        vaccination_time = AppointmentsStore.search_date_appointment(date_signature)
        Date(vaccination_time)
        # JsonStore.save_vaccinated(date_signature)
        VaccinationStorage.save_vaccinated(date_signature)
        return True
