import cv2
import time
import numpy as np
import os
import logging
from src.mumu_adb import MuMuADB
from src.monitoring import MuMuMonitor

class ArknightsOperation:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
        self.adb_path, self.adb_port = adb_path, adb_port
        self.logger = logging.getLogger()
        self._setup_logging()
        self.target_img_path = os.path.join(os.path.dirname(__file__),'..', '..', 'screenshots', 'raw_screenshots', 'arknights.png')
        self.target_img_path = os.path.abspath(self.target_img_path)
        self.monitoring = MuMuMonitor(adb_path=self.adb_path, adb_port=self.adb_port,
         model_path="E:\\python_work\\expand_time\\adb\\project_root\\models\\cnn_model\\cnn_model.h5")

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
        """ 进行与 Arknights 游戏图标的相关操作 """
        # 启动共享监控线程
        self.monitoring.start_monitoring()

        # 通过事件等待数据更新
        self.monitoring.event.wait()  # 等待直到监控线程更新数据
        predicted_class = self.monitoring.predicted_class
        img = self.monitoring.img

        # 执行基于 predicted_class 的操作
        if predicted_class == 0:  # 假设预测类别为 0 需要点击某个图标
            self._click_on_target(img)  # 进行模拟点击

        # 停止监控线程
        self.monitoring.stop_monitoring()


    def _click_on_target(self, img):
        """ 模拟点击目标 """

        target_img = cv2.imread(self.target_img_path, cv2.IMREAD_COLOR)

        if target_img is None:
            self.logger.error(f"无法读取目标图像: {self.target_img_path}")
            return

        # 转换为灰度图像进行匹配
        target_img_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 在图像中寻找目标图片（模板匹配）
        res = cv2.matchTemplate(img, target_img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 设置匹配阈值，值越高，匹配越严格
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):  # (x, y)坐标
            self.logger.info(f"找到目标图像，位置: {pt}")
            # 模拟点击目标位置（使用adb）
            mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
            mumu_adb.click(pt[0], pt[1])