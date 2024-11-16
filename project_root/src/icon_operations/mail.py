import cv2
import time
import numpy as np
import os
import logging
import time
from src.mumu_adb import MuMuADB
from src.monitoring import MuMuMonitor

class MailOperation:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
        self.adb_path, self.adb_port = adb_path, adb_port
        self.logger = logging.getLogger()
        self._setup_logging()
        self.target_img_path1 = os.path.join(os.path.dirname(__file__), '..', '..', 'screenshots', 'raw_screenshots', 'mail.png')
        self.target_img_path2 = os.path.join(os.path.dirname(__file__), '..', '..', 'screenshots', 'raw_screenshots', 'mail1.png')
        self.target_img_path1 = os.path.abspath(self.target_img_path1)
        self.target_img_path2 = os.path.abspath(self.target_img_path2)
        self.monitoring = MuMuMonitor(adb_path=self.adb_path, adb_port=self.adb_port,
                                      model_path="E:\\python_work\\expand_time\\adb\\project_root\\models\\cnn_model\\cnn_model.h5")
        self.whether_mail = False
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
        """ 进行与邮件图标相关的操作 """
        print("已经开始邮件检查进程！")
        self.monitoring.start_monitoring()
 
        while True:
            if self.monitoring.img is not None:
                # 加载两张目标图片
                target_img1 = cv2.imread(self.target_img_path1, cv2.IMREAD_COLOR)
                target_img2 = cv2.imread(self.target_img_path2, cv2.IMREAD_COLOR)
 
                if target_img1 is None:
                    self.logger.error(f"无法读取目标图像: {self.target_img_path1}")
                if target_img2 is None:
                    self.logger.error(f"无法读取目标图像: {self.target_img_path2}")
 
                if target_img1 is not None and target_img2 is not None:
                    # 转换为灰度图
                    target_img1_gray = cv2.cvtColor(target_img1, cv2.COLOR_BGR2GRAY)
                    target_img2_gray = cv2.cvtColor(target_img2, cv2.COLOR_BGR2GRAY)
                    img_gray = cv2.cvtColor(self.monitoring.img, cv2.COLOR_BGR2GRAY)
 
                    # 执行模板匹配
                    res1 = cv2.matchTemplate(img_gray, target_img1_gray, cv2.TM_CCOEFF_NORMED)
                    res2 = cv2.matchTemplate(img_gray, target_img2_gray, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.8  # 匹配阈值
 
                    # 检查匹配结果
                    loc1 = np.where(res1 >= threshold)
                    loc2 = np.where(res2 >= threshold)
 
                    if loc1[0].size > 0 or loc2[0].size > 0:
                        # 获取匹配区域的一个点（左上角），这里选择第一个找到的匹配项
                        if loc1[0].size > 0:
                            pt = (loc1[1].min(), loc1[0].min())
                            self.logger.info(f"找到目标图像 mail.png，位置: {pt}")
                        else:
                            pt = (loc2[1].min(), loc2[0].min())
                            self.logger.info(f"找到目标图像 mail1.png，位置: {pt}")
 
                        mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
                        mumu_adb.click(pt[0], pt[1])
                        print(f"已点击邮件图标，位置在{pt}")
                        self.whether_mail = True
                        break  # 退出循环
 
            time.sleep(1)  # 等待1秒再检查
 
        self.monitoring.stop_monitoring()