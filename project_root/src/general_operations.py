import logging
import os
from src.icon_operations.arknights import ArknightsOperation

class GeneralOperations:
	def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
		self.adb_path = adb_path
		self.adb_port = adb_port
		self.logger = logging.getLogger()
		self._setup_logging()

	def _setup_logging(self):
		log_directory = os.path.join(os.path.dirname(__file__), '..', 'debug')
		if not os.path.exists(log_directory):
			os.makedirs(log_directory)
		
		debug_log_path = os.path.join(log_directory, "debug.log")
		error_log_path = os.path.join(log_directory, "error.log")
		
		debug_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

		debug_handler = logging.FileHandler(debug_log_path)
		debug_handler.setLevel(logging.DEBUG)
		debug_handler.setFormatter(debug_formatter)

		error_handler = logging.FileHandler(error_log_path)
		error_handler.setLevel(logging.ERROR)
		error_handler.setFormatter(error_formatter)

		self.logger.addHandler(debug_handler)
		self.logger.addHandler(error_handler)
		self.logger.setLevel(logging.DEBUG)

	def arknights(self):
		start_arknights = ArknightsOperation(adb_path=self.adb_path, adb_port=self.adb_port)
		start_arknights.perform_action()
