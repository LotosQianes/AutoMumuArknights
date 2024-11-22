import threading # 启动多线程
from src.mumu_adb import MuMuADB
from src.monitoring import MuMuMonitor
from src.general_operations import GeneralOperations
from src.console import start_console
from src.ui import start_ui

def start_monitoring():
    """ 管理屏幕截图，监控 """
    # 实例化 MuMuMonitor 类
    monitoring = MuMuMonitor(adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384")

    # 测试对 MuMu 模拟器进行截图
    monitoring.capture_screenshot(max_retries=3, retry_delay=5)

def start_general_operations():
    """ 用于总控神经网络结果后的操作 """
    # 实例化 GeneralOperations 类
    general_operations = GeneralOperations(adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384")

def start_ui_thread():
    """运行 UI 的线程入口"""
    start_ui()

def main():
    # 实例化 MuMuADB 类，指定ADB路径和端口
    mumu_adb = MuMuADB(adb_path="D:\\Program Files\\Netease\\MuMuPlayer-12.0\\shell\\adb.exe", adb_port="16384")
    
    # 测试连接到 MuMu 模拟器
    mumu_adb.connect_to_mumu(max_retries=3, retry_delay=5)

    # 启动控制台线程
    console_thread = threading.Thread(target=start_console, daemon=True)
    console_thread.start()

    # 启动监控线程
    monitoring_thread = threading.Thread(target=start_monitoring,)
    monitoring_thread.start()
 
    # 启动操作总控线程
    operations_thread = threading.Thread(target=start_general_operations)
    operations_thread.start()

    # 启动 UI 线程
    ui_thread = threading.Thread(target=start_ui_thread, daemon=True)
    ui_thread.start()

    # 等待所有线程完成
    monitoring_thread.join()
    operations_thread.join()
    console_thread.join()
    ui_thread.join()


if __name__ == "__main__":
    main()