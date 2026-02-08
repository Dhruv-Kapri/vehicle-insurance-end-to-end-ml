import logging
import types


def error_message_detail(error: Exception, error_detail: types.ModuleType) -> str:
    """
    Extracts file name, line number, and error message from traceback.
    """
    # Extract traceback details (exception information)
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is None:
        return str(error)

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in python script: "
        f"[{file_name}] at line number [{line_number}]: {str(error)}"
    )

    logging.error(error_message)
    return error_message


class MyException(Exception):
    """
    Custom exception class with detailed traceback information.
    """

    def __init__(self, error: Exception, error_detail: types.ModuleType):
        # Call the base class constructor with the error message
        super().__init__(str(error))

        # Format the detailed error message using the error_message_detail function
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self) -> str:
        return self.error_message
