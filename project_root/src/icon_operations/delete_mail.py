import cv2
import time
import numpy as np
import os
import logging
import time
from src.mumu_adb import MuMuADB
from src.monitoring import MuMuMonitor

class DeleteMailOperation:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
        self.adb_path, self.adb_port = adb_path, adb_port
        self.logger = logging.getLogger()
        self._setup_logging()
        self.target_img_path = os.path.join(os.path.dirname(__file__),'..', '..', 'screenshots', 'raw_screenshots', 'delete_mail.png')
        self.target_img_path = os.path.abspath(self.target_img_path)
        self.monitoring = MuMuMonitor(adb_path=self.adb_path, adb_port=self.adb_port,
         model_path="E:\\python_work\\expand_time\\adb\\project_root\\models\\cnn_model\\cnn_model.h5")
        self.whether_delete_mail = 0

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
        """ 进行与 Start 游戏图标的相关操作 """
        # 启动共享监控线程
        print("正在删除邮件。")
        self.monitoring.start_monitoring()
 
        # 等待直到游戏加载完成（这里使用轮询的方式）
        while True:
            # 检查是否有新的屏幕截图可用
            if self.monitoring.img is not None:
                # 执行模板匹配
                target_img = cv2.imread(self.target_img_path, cv2.IMREAD_COLOR)
                if target_img is None:
                    self.logger.error(f"无法读取目标图像: {self.target_img_path}")
                    continue
 
                target_img_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
                img_gray = cv2.cvtColor(self.monitoring.img, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(img_gray, target_img_gray, cv2.TM_CCOEFF_NORMED)
                threshold = 0.8  # 匹配阈值
                loc = np.where(res >= threshold)
 
                # 如果找到了匹配项，就点击它并退出循环
                if loc[0].size > 0:
                    top_left = (loc[1].min(), loc[0].min())  # 获取匹配区域的一个点（左上角）
                    # 获取目标图像的宽度和高度
                    h, w = target_img_gray.shape
                    # 修改 top_left 为中心点
                    center = (top_left[0] + w // 2, top_left[1] + h // 2)
                    # 模拟点击
                    mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
                    print(f"找到删除邮件图标，位置: {center}")
                    self.logger.info(f"找到删除邮件图像，位置: {center}")
                    mumu_adb.click(center[0], center[1])
                    print(f"您已删除邮件，中心位置位置在{center}")
                    break  # 退出循环
                # 如果未找到，重复尝试5次后退出循环
                else:
                    self.whether_delete_mail += 1
                    print(f"目前未找到删除邮件图标，尝试次数 {self.whether_delete_mail}")
                    if self.whether_delete_mail >= 5:
                        break

            # 如果没有找到匹配项，就等待一段时间再检查（避免过于频繁地轮询）
            time.sleep(1)  # 等待1秒再检查

        # 退出监控进程
        self.monitoring.stop_monitoring()
        self.whether_delete_mail = 0