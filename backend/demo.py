# # below code is to check the logging config
# from src.logger import logger

# logger.debug("This is a debug message.")
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")

# # --------------------------------------------------------------------------------

# # below code is to check the exception config
# import sys

# from src.exception import MyException
# from src.logger import logger

# try:
#     a = 1 + "Z"
# except Exception as e:
#     logger.info(e)
#     raise MyException(e, sys) from e

# # --------------------------------------------------------------------------------
