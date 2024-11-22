import cv2
import time
import numpy as np
import os
import logging
from src.mumu_adb import MuMuADB
from src.monitoring import MuMuMonitor

class ClueGatheringOperation:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
        self.adb_path, self.adb_port = adb_path, adb_port
        self.logger = logging.getLogger()
        self._setup_logging()
        self.target_img_path = os.path.join(os.path.dirname(__file__),'..', '..', 'screenshots', 'raw_screenshots', 'clue_gathering.png')
        self.target_img_path = os.path.abspath(self.target_img_path)
        self.monitoring = MuMuMonitor(adb_path=self.adb_path, adb_port=self.adb_port,
         model_path="E:\\python_work\\expand_time\\adb\\project_root\\models\\cnn_model\\cnn_model.h5")
        self.whether_clue_gathering = 0

    def _setup_logging(self):
        log_directory = os.path.join(os.path.dirname(__file__),'..', '..', 'debug')
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

    def perform_action(self):
        """ 进行与线索收集相关的操作 """
        print("发现有线索待收集。")
        self.monitoring.start_monitoring()

        try:
            while self.whether_clue_gathering < 5:
                if self.monitoring.img is not None:
                    target_img = cv2.imread(self.target_img_path, cv2.IMREAD_COLOR)
                    if target_img is None:
                        self.logger.error(f"无法读取目标图像: {self.target_img_path}")
                        continue

                    target_img_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
                    img_gray = cv2.cvtColor(self.monitoring.img, cv2.COLOR_BGR2GRAY)
                    res = cv2.matchTemplate(img_gray, target_img_gray, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.8
                    loc = np.where(res >= threshold)

                    if loc[0].size > 0:
                        top_left = (loc[1].min(), loc[0].min())
                        h, w = target_img_gray.shape
                        center = (top_left[0] + w // 2, top_left[1] + h // 2)

                        mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
                        print(f"发现线索收集，位置: {center}，准备进入会客室")
                        self.logger.info(f"找到信赖收取图标，位置: {center}")
                        return True

                    else:
                        self.whether_clue_gathering += 1
                        print(f"并没有线索等待收集，尝试次数 {self.whether_clue_gathering}")
                        if self.whether_clue_gathering >= 5:
                            return False

                time.sleep(1)

        finally:
            # 确保监控停止
            self.monitoring.stop_monitoring()
            self.whether_clue_gathering = 0