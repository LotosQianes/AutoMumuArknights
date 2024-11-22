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
        """捕获模拟器屏幕截图"""
        mumu_adb = MuMuADB(adb_path=self.adb_path, adb_port=self.adb_port)
        
        if not mumu_adb.connect_to_mumu(max_retries, retry_delay):
            self.logger.error("无法连接到 MuMu 模拟器，截图失败！")
            return None

        retries = 0
        while retries < max_retries and self.running:
            try:
                adb_cmd = f'"{self.adb_path}" -s 127.0.0.1:{self.adb_port} exec-out screencap -p'
                result = subprocess.run(adb_cmd, shell=True, capture_output=True, timeout=10)

                if result.returncode == 0:
                    img = cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)
                    if img is not None:
                        return img
                    else:
                        self.logger.error("无法解码图像数据")
                else:
                    self.logger.warning(f"截图失败: {result.stderr}. 重试 {retries + 1}/{max_retries}...")
                    retries += 1
                    time.sleep(retry_delay)
            except subprocess.TimeoutExpired:
                self.logger.error("截图命令超时，停止尝试")
                break

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
        while self.running:
            try:
                if not self.running:
                    break

                img = self.capture_screenshot(max_retries, retry_delay)
                if img is not None:
                    cv2.imshow("MuMu Monitor", img)
                    self.predicted_class = predict(self.model, img)
                    self.img = img
                    self.event.set()

                if cv2.waitKey(display_interval * 1000) & 0xFF == ord('q'):
                    break
            except Exception as e:
                self.logger.error(f"监控线程出错: {e}")
                break

        cv2.destroyAllWindows()
        self.logger.info("监控线程已退出")

    def start_monitoring(self):
        """启动监控线程"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.monitor_and_display, args=(3, 5, 1), daemon=True)
            self.thread.start()

    def stop_monitoring(self, timeout=5):
        """停止监控线程"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=timeout)  # 等待线程结束
            if self.thread.is_alive():
                self.logger.warning("监控线程未能正常结束，强制释放资源")
                self.force_terminate()

    def force_terminate(self):
        """强制终止监控线程"""
        self.running = False
        cv2.destroyAllWindows()  # 确保关闭所有OpenCV窗口
        self.logger.info("已强制终止监控线程，释放资源")