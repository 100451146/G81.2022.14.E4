import json

from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enum.enumerations import MessError


class JsonStore:
    class __JsonStore:
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

    __is_instance = None

    @staticmethod
    def load_json(input_file: str):
        if JsonStore.__is_instance is None:
            JsonStore.__is_instance = JsonStore.__JsonStore
        return JsonStore.__is_instance.load_json(input_file)

    @staticmethod
    def save_json_data(data, file_store: str) -> None:
        if JsonStore.__is_instance is None:
            JsonStore.__is_instance = JsonStore.__JsonStore
        return JsonStore.__is_instance.save_json_data(data, file_store)
