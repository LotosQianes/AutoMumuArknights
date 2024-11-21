import cv2
import time
import numpy as np
import os
import logging
from src.mumu_adb import MuMuADB
from src.monitoring import MuMuMonitor
from models.ocr import OCR

class ReceptionOperationOCR:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
        self.adb_path, self.adb_port = adb_path, adb_port
        self.logger = logging.getLogger()
        self._setup_logging()
        self.monitoring = MuMuMonitor(adb_path=self.adb_path, adb_port=self.adb_port,
                                      model_path="E:\\python_work\\expand_time\\adb\\project_root\\models\\cnn_model\\cnn_model.h5")
        self.ocr = OCR(use_gpu=False, lang='ch')  # 初始化OCR（中文）
        self.whether_clue_gathering = 0

    def _setup_logging(self):
        log_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'debug')
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        debug_log_path = os.path.join(log_directory, "debug.log")
        error_log_path = os.path.join(log_directory, "error.log")

        # 清除所有现有日志处理器，避免控制台输出
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

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
        """ 使用OCR检测并点击文字 '会客室' """
        print("尝试检测文字 '会客室'")
        self.monitoring.start_monitoring()  # 启动监控

        while self.whether_clue_gathering < 5:  # 限制最大尝试次数
            # 检查是否有新的屏幕截图
            if self.monitoring.img is not None:
                # 使用OCR进行文字识别
                results = self.ocr.recognize(self.monitoring.img)
                for text, box, confidence in self.ocr.get_texts_and_boxes(results):
                    if text == "会客室" and confidence >= 0.8:  # 置信度阈值为0.8
                        print(f"检测到 '会客室', 位置: {box}, 置信度: {confidence}")
                        self.logger.info(f"检测到 '会客室', 位置: {box}, 置信度: {confidence}")
                        
                        # 计算中心点坐标
                        top_left = tuple(box[0])
                        bottom_right = tuple(box[2])
                        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)

                        # 模拟点击
                        mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
                        mumu_adb.click(center[0], center[1])
                        print(f"已点击 '会客室', 中心位置: {center}")
                        self.logger.info(f"已点击 '会客室', 中心位置: {center}")
                        
                        # 重置尝试次数，因为已经成功点击了
                        self.whether_clue_gathering = 0  
                        break

                # 如果未找到
                else:
                    self.whether_clue_gathering += 1
                    print(f"未找到 '会客室', 尝试次数 {self.whether_clue_gathering}")
                    self.logger.info(f"未找到 '会客室', 尝试次数 {self.whether_clue_gathering}")

            # 等待一段时间避免频繁轮询
            time.sleep(1)

        # 停止监控
        print("超过最大尝试次数，退出会客室点击流程。")
        self.logger.info("超过最大尝试次数，退出会客室点击流程。")
        self.monitoring.stop_monitoring()
        self.whether_clue_gathering = 0