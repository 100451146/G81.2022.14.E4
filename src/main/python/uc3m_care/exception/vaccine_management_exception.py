"""Exception for the access_management module"""

class VaccineManagementException(Exception):
    """Personalised exception for Vaccine Management"""
    def __init__(self, ex_message):
        self.__message = ex_message
        super().__init__(self.ex_message)

    @property
    def ex_message(self):
        """gets the message value"""
        return self.__message

    @ex_message.setter
    def ex_message(self, value):
        self.__message = value
