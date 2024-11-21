import logging
import os
from src.icon_operations import (
    ArknightsOperation,
    StartOperation,
    WakeOperation,
    MailOperation,
    ReceivingMailOperation,
    CollectOperation,
    DeleteMailOperation,
    QuitMailOperation,
    InfrastructureOperation,
    InfrastructureTipsOperation,
    MaterialReceiptOperation,
    LmbReceiptOperation,
    OperatorsTrustOperation,
    ClueGatheringOperation,
    ReceptionOperationOCR,
    CollectingCluesOperation,
    ReceptionCluesOperation,
    GatherReceptionCluesOperation,
    ReturnOperation,
    ConfirmOperation,
)


class GeneralOperations:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
        self.adb_path = adb_path
        self.adb_port = adb_port
        self.logger = self._setup_logging()

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

    def start_awaken(self):
        """启动 '开始唤醒' 功能"""
        try:
            self.logger.info("开始唤醒功能启动")
            ArknightsOperation(self.adb_path, self.adb_port).perform_action()
            StartOperation(self.adb_path, self.adb_port).perform_action()
            WakeOperation(self.adb_path, self.adb_port).perform_action()
        except Exception as e:
            self.logger.error(f"开始唤醒功能发生错误: {e}")

    def collect_mail(self):
        """启动 '收取邮箱' 功能"""
        try:
            self.logger.info("收取邮箱功能启动")
            MailOperation(self.adb_path, self.adb_port).perform_action()
            ReceivingMailOperation(self.adb_path, self.adb_port).perform_action()
            CollectOperation(self.adb_path, self.adb_port).perform_action()
            DeleteMailOperation(self.adb_path, self.adb_port).perform_action()
            QuitMailOperation(self.adb_path, self.adb_port).perform_action()
        except Exception as e:
            self.logger.error(f"收取邮箱功能发生错误: {e}")

    def collect_infrastructure_and_clues(self):
        """启动 '基建材料及线索' 功能"""
        try:
            self.logger.info("基建材料及线索功能启动")
            InfrastructureOperation(self.adb_path, self.adb_port).perform_action()
            InfrastructureTipsOperation(self.adb_path, self.adb_port).perform_action()
            MaterialReceiptOperation(self.adb_path, self.adb_port).perform_action()
            LmbReceiptOperation(self.adb_path, self.adb_port).perform_action()
            OperatorsTrustOperation(self.adb_path, self.adb_port).perform_action()
            ClueGatheringOperation(self.adb_path, self.adb_port).perform_action()
            ReceptionOperationOCR(self.adb_path, self.adb_port).perform_action()
            CollectingCluesOperation(self.adb_path, self.adb_port).perform_action()
            ReceptionCluesOperation(self.adb_path, self.adb_port).perform_action()
            GatherReceptionCluesOperation(self.adb_path, self.adb_port).perform_action()
            ReturnOperation(self.adb_path, self.adb_port).perform_action()
            ConfirmOperation(self.adb_path, self.adb_port).perform_action()
        except Exception as e:
            self.logger.error(f"基建材料及线索功能发生错误: {e}")