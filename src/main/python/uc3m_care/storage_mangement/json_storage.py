import json

from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import MessError


class JsonStore:

    @staticmethod
    def load_json(input_file: str):
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(MessError.ERR_MESS_WRONG_JSON_FORMAT.value) from exception
        return json_data

    @staticmethod
    def save_json_data(data, file_store: str) -> None:
        try:
            with open(file_store, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException(MessError.ERR_MESS_WRONG_FILE.value) from exception
