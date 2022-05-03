import datetime

from uc3m_care import VaccinePatientRegister
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH, PATIENTS_STORE, VACCINES_STORE
from uc3m_care.enum.enumerations import Mess_Error, Dict_Data
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage_mangement.json_storage import JsonStore


class VaccinationStorage(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"

    @staticmethod
    def save_vaccinated(date_signature: str) -> None:
        try:
            vaccinated_list = JsonStore.load_json(VACCINES_STORE)
        except FileNotFoundError as exception:
            vaccinated_list = []
        # append the date
        vaccinated_list.extend({date_signature.__str__(), datetime.datetime.utcnow().__str__()})

        JsonStore.save_json_data(vaccinated_list, VACCINES_STORE)
