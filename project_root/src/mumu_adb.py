import subprocess
import time
import logging
import os

class MuMuADB:
    def __init__(self, adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384"):
        """ 初始化MuMuADB实例，指定ADB路径和连接地址 """
        self.adb_path = adb_path
        self.adb_port = adb_port
        
        # 配置日志记录器
        self._setup_logging()

    def _setup_logging(self):
        """ 设置日志记录配置，将日志分别写入debug.log和error.log """
        log_directory = os.path.join(os.path.dirname(__file__), '..', 'debug')  # 从src进入project_root，再进入debug
        
        # 确保debug文件夹存在
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        
        # 设置debug日志
        debug_log_path = os.path.join(log_directory, "debug.log")
        error_log_path = os.path.join(log_directory, "error.log")
        
        # 创建日志记录器
        self.logger = logging.getLogger()

        # 设置debug日志处理器，记录调试信息
        debug_handler = logging.FileHandler(debug_log_path)
        debug_handler.setLevel(logging.DEBUG)  # 记录DEBUG及以上级别的日志
        debug_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        debug_handler.setFormatter(debug_formatter)

        # 设置error日志处理器，记录错误信息
        error_handler = logging.FileHandler(error_log_path)
        error_handler.setLevel(logging.ERROR)  # 记录ERROR及以上级别的日志
        error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        error_handler.setFormatter(error_formatter)

        # 将处理器添加到日志记录器
        self.logger.addHandler(debug_handler)
        self.logger.addHandler(error_handler)

        # 设置日志输出级别为DEBUG，表示会捕捉所有日志级别
        self.logger.setLevel(logging.DEBUG)

    def connect_to_mumu(self, max_retries=3, retry_delay=5):
        """ 连接到 MuMu 模拟器的 ADB 服务，增加最大重试次数以防止无限重试 """
        retries = 0
        while retries < max_retries:
            adb_cmd = f'"{self.adb_path}" connect 127.0.0.1:{self.adb_port}'
            result = subprocess.run(adb_cmd, shell=True, capture_output=True, text=True)
            
            # 如果连接成功
            if "connected" in result.stdout:
                self.logger.debug(f"成功连接到 MuMu 模拟器（端口：{self.adb_port}）")
                return True
            else:
                self.logger.warning(f"连接 MuMu 模拟器失败: {result.stderr}. 重试 {retries + 1}/{max_retries}...")
                retries += 1
                time.sleep(retry_delay)
        
        # 如果连接失败
        self.logger.error(f"连接 MuMu 模拟器失败，已尝试 {max_retries} 次，停止重试。")
        return False

    def click(self, x, y):
        """ 模拟点击操作 """
        adb_cmd = f'"{self.adb_path}" -s 127.0.0.1:{self.adb_port} shell input tap {x} {y}'
        result = subprocess.run(adb_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            self.logger.info(f"成功模拟点击，坐标: ({x}, {y})")
        else:
            self.logger.error(f"点击失败，错误信息: {result.stderr}")

if __name__ == '__main__':
    mumu_adb = MuMuADB(adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384")
    mumu_adb.click(143, 94)