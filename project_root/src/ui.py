from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox,
    QPushButton, QLabel, QGroupBox, QLineEdit, QGridLayout, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.general_operations import GeneralOperations  # 导入 general_operations 中的类


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("功能界面")
        self.setGeometry(100, 100, 1000, 700)

        # 初始化 GeneralOperations 实例
        self.operations = GeneralOperations()

        # 功能名称到方法的映射
        self.feature_to_method = {
            "开始唤醒": self.operations.start_awaken,
            "收取邮箱": self.operations.collect_mail,
            "收集基建材料": self.operations.gather_infrastructure_mats,
            "收集基建线索": self.operations.gather_infrastructure_hint
        }

        # 主布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 设置主要区域
        self.setup_main_layout(main_layout)

    def setup_main_layout(self, layout):
        """设置主界面的布局"""
        # 顶部布局
        self.status_label = QLabel("正在运行：无")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.status_label)

        # 中部功能布局
        content_layout = QHBoxLayout()

        # 左侧：功能选项
        self.left_group = QGroupBox("功能选项")
        self.left_group.setFont(QFont("Arial", 12))
        self.left_layout = QVBoxLayout()
        self.left_group.setLayout(self.left_layout)

        # 添加功能选项
        self.add_feature_option("开始唤醒", self.show_awaken_settings)
        self.add_feature_option("收取邮箱", self.show_mail_settings)
        self.add_feature_option("收集基建材料", self.show_material_settings)
        self.add_feature_option("收集基建线索", self.show_clue_settings)

        content_layout.addWidget(self.left_group)

        # 右侧：参数设置
        self.right_group = QGroupBox("参数设置")
        self.right_layout = QVBoxLayout()
        self.right_group.setLayout(self.right_layout)
        content_layout.addWidget(self.right_group)

        layout.addLayout(content_layout)

        # 底部：启动按钮
        self.start_button = QPushButton("Link Start!")
        self.start_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.start_button.setStyleSheet(self.start_button_style())
        self.start_button.clicked.connect(self.start_operations)
        layout.addWidget(self.start_button)

    def add_feature_option(self, feature_name, settings_handler):
        """添加功能选项和齿轮按钮"""
        feature_layout = QHBoxLayout()

        checkbox = QCheckBox(feature_name)
        checkbox.setFont(QFont("Arial", 10))
        checkbox.setChecked(False)  # 默认不勾选
        feature_layout.addWidget(checkbox)

        gear_button = QPushButton("⚙")
        gear_button.setFixedSize(25, 25)
        gear_button.setStyleSheet(self.gear_button_style())
        gear_button.clicked.connect(lambda: self.safe_handler(settings_handler, feature_name))
        feature_layout.addWidget(gear_button)

        self.left_layout.addLayout(feature_layout)

    def safe_handler(self, handler, feature_name):
        """包装参数设置的处理程序，确保无异常"""
        try:
            handler()
        except Exception as e:
            print(f"Error handling {feature_name}: {e}")

    def show_awaken_settings(self):
        """显示‘开始唤醒’的参数设置"""
        self.update_right_panel([
            ("ADB路径（相对/绝对）：", QLineEdit()),
            ("连接地址：", QLineEdit()),
            ("账号设置：", QLineEdit()),
            ("客户端类型：", self.create_combobox(["官服", "B服", "日服", "韩服", "繁中服", "国际服"]))
        ])

    def show_mail_settings(self):
        """显示‘收取邮箱’的参数设置"""
        self.update_right_panel([
            ("邮箱服务器地址：", QLineEdit()),
            ("邮箱账号：", QLineEdit()),
            ("邮箱密码：", QLineEdit())
        ])

    def show_material_settings(self):
        """显示‘收集基建材料’的参数设置"""
        self.update_right_panel([
            ("选择基建材料类型：", self.create_checkbox_group(["作战记录", "赤金", "源石碎片"]))
        ])

    def show_clue_settings(self):
        """显示‘收集基建线索’的参数设置"""
        self.update_right_panel([
            ("选择线索类型：", self.create_checkbox_group(["会客室线索", "好友线索"]))
        ])

    def create_combobox(self, items):
        """创建带有选项的 QComboBox"""
        combobox = QComboBox()
        combobox.addItems(items)  # 确保 addItems 的调用是正确的
        return combobox

    def create_checkbox_group(self, items):
        """创建复选框组"""
        group = QGroupBox()
        layout = QVBoxLayout()
        for item in items:
            checkbox = QCheckBox(item)
            checkbox.setFont(QFont("Arial", 10))
            layout.addWidget(checkbox)
        group.setLayout(layout)
        return group

    def update_right_panel(self, widgets):
        """清除并更新右侧参数设置区域"""
        self.clear_right_panel()
        for label_text, widget in widgets:
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 11))
            self.right_layout.addWidget(label)
            self.right_layout.addWidget(widget)

    def start_operations(self):
        """开始运行选中的功能"""
        self.status_label.setText("正在运行：...")
        print("开始运行功能")

        # 遍历所有功能选项的复选框
        for i in range(self.left_layout.count()):
            item = self.left_layout.itemAt(i)
            if isinstance(item, QHBoxLayout):  # 确保我们处理的是功能选项布局
                checkbox = item.itemAt(0).widget()  # 获取复选框
                if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                    feature_name = checkbox.text()
                    if feature_name in self.feature_to_method:
                        try:
                            self.status_label.setText(f"正在运行：{feature_name}")  # 更新状态标签
                            self.feature_to_method[feature_name]()
                            print(f"功能 {feature_name} 已启动")
                        except Exception as e:
                            print(f"执行功能 {feature_name} 时出错: {e}")
        self.status_label.setText("运行完成")

    def clear_right_panel(self):
        """清除右侧的所有控件"""
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def gear_button_style(self):
        """设置齿轮按钮的样式"""
        return """
        QPushButton {
            background-color: #e6e6e6;
            border: 1px solid #cccccc;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #d6d6d6;
        }
        """

    def start_button_style(self):
        """设置启动按钮的样式"""
        return """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
        }
        """


def start_ui():
    import sys
    app = QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec())
