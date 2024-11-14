import threading
import cv2
import numpy as np
import time
import subprocess
import logging
import os
from src.mumu_adb import MuMuADB
from models.inference import load_model, predict  # 引入预测功能

class MuMuMonitor:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384",
     model_path="E:\\python_work\\expand_time\\adb\\project_root\\models\\cnn_model\\cnn_model.h5"):
        self.adb_path = adb_path
        self.adb_port = adb_port
        self.model = load_model(model_path)  # 加载AI模型
        self.logger = logging.getLogger()
        self._setup_logging()
        self.predicted_class, self.img = None, None 
        self.lock = threading.Lock()  # 线程锁
        self.running = False  # 控制线程的运行状态
        self.thread = None  # 存储线程对象
        self.event = threading.Event()  # 用于线程间同步的事件

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

    def capture_screenshot(self, max_retries=3, retry_delay=5):
        mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
        
        if not mumu_adb.connect_to_mumu(max_retries, retry_delay):
            self.logger.error("无法连接到 MuMu 模拟器，截图失败！")
            return None
        
        retries = 0
        while retries < max_retries:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            # 将图像通过内存流直接捕获
            adb_cmd = f'"{self.adb_path}" -s 127.0.0.1:{self.adb_port} exec-out screencap -p'
            result = subprocess.run(adb_cmd, shell=True, capture_output=True)

            if result.returncode == 0:
                image_data = result.stdout
                img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                
                if img is None:
                    self.logger.error("无法解码图像数据")
                    return None
                return img
            else:
                self.logger.warning(f"截图失败: {result.stderr}. 重试 {retries + 1}/{max_retries}...")
                retries += 1
                time.sleep(retry_delay)

        self.logger.error(f"截图失败，已尝试 {max_retries} 次，停止重试。")
        return None

    def monitor_and_display(self, max_retries=3, retry_delay=5, display_interval=1):
        """ 实时监控模拟器屏幕并显示 """
        mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
        
        if not mumu_adb.connect_to_mumu(max_retries, retry_delay):
            self.logger.error("无法连接到 MuMu 模拟器，监控失败！")
            return
        
        # 初始化 OpenCV 显示窗口
        cv2.namedWindow("MuMu Monitor", cv2.WINDOW_NORMAL)
        
        self.running = True
        retries = 0
        while self.running:
            img = self.capture_screenshot(max_retries, retry_delay)
            
            if img is not None:
                cv2.imshow("MuMu Monitor", img)
                
                # 使用AI模型对图像进行分类预测
                self.predicted_class = predict(self.model, img)
                self.img = img
                self.event.set()  # 更新数据，通知其他线程/函数

                cv2.waitKey(display_interval * 1000)  # 控制显示间隔（单位为毫秒）

            retries = 0  # 重试次数重置

            # 按 'q' 键退出实时监控
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

    def start_monitoring(self):
        """ 启动线程来实时监控模拟器屏幕并更新 predicted_class 和 img """
        if not self.running:
            self.thread = threading.Thread(target=self.monitor_and_display, args=(3, 5, 1))
            self.thread.start()

    def stop_monitoring(self):
        """ 停止监控线程 """
        self.running = False
        if self.thread:
            self.thread.join()  # 等待线程结束