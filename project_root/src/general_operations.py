import logging
import os
import time
from src.icon_operations import (
	ArknightsOperation,
	StartOperation,
	WakeOperation,
	MailOperation,
	ReceivingMailOperation,
	DeleteMailOperation,
	QuitMailOperation,
	InfrastructureOperation,
	InfrastructureTipsOperation,
	MaterialReceiptOperation,
	LmbReceiptOperation,
)
 
class GeneralOperations:
	def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
		self.adb_path = adb_path
		self.adb_port = adb_port
		self._setup_logging()

	def _setup_logging(self):

		log_dir = os.path.join(os.path.dirname(__file__), '..', 'debug')
		os.makedirs(log_dir, exist_ok=True)
		
		logger = logging.getLogger()
		logger.setLevel(logging.DEBUG)
		
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		
		debug_handler = logging.FileHandler(os.path.join(log_dir, "debug.log"))
		debug_handler.setLevel(logging.DEBUG)
		debug_handler.setFormatter(formatter)
		
		error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
		error_handler.setLevel(logging.ERROR)
		error_handler.setFormatter(formatter)
		
		logger.addHandler(debug_handler)
		logger.addHandler(error_handler)
		
		return logger

	def operations(self):

		operations = [
			ArknightsOperation,
			StartOperation,
			WakeOperation,
			MailOperation,
			ReceivingMailOperation,
			DeleteMailOperation,
			QuitMailOperation,
			InfrastructureOperation,
			InfrastructureTipsOperation,
			MaterialReceiptOperation,
			LmbReceiptOperation,
		]

		for OperationClass in operations:
			try:
				operation = OperationClass(adb_path=self.adb_path, adb_port=self.adb_port)
				operation.perform_action()
			except Exception as e:
				self.logger.error(f"Error performing action for {OperationClass.__name__}: {e}")