import datetime

from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH, VACCINES_STORE
from uc3m_care.storage_mangement.json_storage import JsonStore
from uc3m_care.vaccine_log import VaccineLog


class VaccinationStorage(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"

    @staticmethod
    def save_vaccinated(date_signature: str) -> None:
        try:
            vaccinated_list = JsonStore.load_json(VaccinationStorage._FILE_PATH)
        except FileNotFoundError:
            vaccinated_list = []
        my_vaccine_log = VaccineLog(date_signature)
        # append the date
        vaccinated_list.append(my_vaccine_log.__dict__)

        JsonStore.save_json_data(vaccinated_list, VACCINES_STORE)
