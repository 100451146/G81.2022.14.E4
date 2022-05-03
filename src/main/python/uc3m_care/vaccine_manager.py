"""Module """

from uc3m_care.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.data.attribute.attribute_date import Date
from uc3m_care.data.attribute.hash_sha256 import SHA256
from .storage_mangement.appointments_storage import AppointmentsStore
from .storage_mangement.registry_storage import RegistryStore
from .storage_mangement.vaccinated_storage import VaccinationStorage


class VaccineManager:

    class __VaccineManager:

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
            my_signature = VaccinationAppoinment(input_file)
            # save the date in store_date.json
            AppointmentsStore.save_vaccination_appointment(my_signature)
            return my_signature.date_signature

        @staticmethod
        def vaccine_patient(date_signature: str) -> True:
            """Register the vaccination of the patient"""

            SHA256(date_signature)
            vaccination_time = AppointmentsStore.search_date_appointment(date_signature)
            Date(vaccination_time)
            # JsonStore.save_vaccinated(date_signature)
            VaccinationStorage.save_vaccinated(date_signature)
            return True

    __instance = None

    def __new__(cls):
        if VaccineManager.__instance is None:
            VaccineManager.__instance = VaccineManager.__VaccineManager()
        return VaccineManager.__instance
