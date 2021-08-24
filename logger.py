"""Module responsible for managing all the application log creation."""
import logging
import logging.config
import os


class Logger:
    """Class for managing all the logging facilities
    for the application.
    """
    def __init__(self):
        try:
            self.__load_config_file()
        except FileNotFoundError:
            self.__create_log_dir()
            self.__load_config_file()
        finally:
            self.logger = self.__get_logger()
            self.logger.info("Initializing log")

        self.LOG = {
            'd': self.logger.debug,
            'i': self.logger.info,
            'w': self.logger.warning,
            'e': self.logger.error
        }

    @staticmethod
    def __create_log_dir() -> None:
        """Create the log directory if does not
        exists.

        :return:
        """
        if not os.path.exists(f"{os.getcwd()}/logs"):
            os.mkdir(f"{os.getcwd()}/logs")

    @staticmethod
    def __load_config_file() -> None:
        """Load the logger config file.
        """
        logging.config.fileConfig(f"{os.getcwd()}/resources/logging.conf")
    
    @staticmethod
    def __get_logger() -> logging.Logger:
        """Returns the logger object.

        :return: a logging object.
        """
        return logging.getLogger('faceDetect')

    def log(self, message: str, level : str = "i") -> None:
        """Logs a given message for a given log level.

        :param message: string to be logged.
        :param level: log level.

        :return:
        """
        self.LOG[level](message)