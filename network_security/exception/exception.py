import sys
from network_security.logging import logger


class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        _, _, exec_traceback = error_details.exc_info()

        self.lineno = exec_traceback.tb_lineno
        self.filename = exec_traceback.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python file: {0} at line number: {1} with error message: {2}".format(
            self.filename, self.lineno, self.error_message
        )
