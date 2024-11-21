from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,QComboBox,
    QTabWidget, QCheckBox, QPushButton, QLabel, QGroupBox, QStatusBar, QGridLayout,QLineEdit
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

        # Main widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Tab widget for main navigation
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(self.tab_style())
        main_layout.addWidget(self.tab_widget)

        # Add tabs
        self.create_main_tabs()

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("准备就绪")

    def create_main_tabs(self):
        """Create and add main tabs"""
        # Tab 1: 一键长草
        tab1 = QWidget()
        self.tab_widget.addTab(tab1, "一键长草")
        self.setup_tab1(tab1)

        # Tab 2: 设置
        tab2 = QWidget()
        self.tab_widget.addTab(tab2, "设置")
        self.setup_tab2(tab2)

    def setup_tab1(self, tab):
        """Setup layout for the first tab"""
        layout = QVBoxLayout(tab)

        # Display current operation status
        self.status_label = QLabel("正在运行：无")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.status_label)

        # Functional checkboxes group
        self.feature_group = QGroupBox("功能选项")
        self.feature_group.setFont(QFont("Arial", 12))
        feature_layout = QVBoxLayout()

        # Checkboxes for features
        self.awaken_checkbox = QCheckBox("开始唤醒")
        self.mail_checkbox = QCheckBox("收取邮箱")
        self.infrastructure_checkbox = QCheckBox("基建材料及线索")

        # Apply compact style
        self.awaken_checkbox.setFont(QFont("Arial", 10))
        self.mail_checkbox.setFont(QFont("Arial", 10))
        self.infrastructure_checkbox.setFont(QFont("Arial", 10))

        feature_layout.addWidget(self.awaken_checkbox)
        feature_layout.addWidget(self.mail_checkbox)
        feature_layout.addWidget(self.infrastructure_checkbox)
        self.feature_group.setLayout(feature_layout)
        layout.addWidget(self.feature_group)

        # "Link Start!" button
        self.start_button = QPushButton("Link Start!")
        self.start_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.start_button.setStyleSheet(self.start_button_style())
        self.start_button.clicked.connect(self.start_operations)
        layout.addWidget(self.start_button)

    def setup_tab2(self, tab):
        """Setup layout for the second tab"""
        layout = QGridLayout(tab)

        # General settings
        general_settings = QGroupBox("常规设置")
        general_layout = QVBoxLayout()

        label1 = QLabel("用户名:")
        label1.setFont(QFont("Arial", 11))
        user_input = QLineEdit()
        general_layout.addWidget(label1)
        general_layout.addWidget(user_input)

        label2 = QLabel("背景颜色:")
        label2.setFont(QFont("Arial", 11))
        bg_dropdown = QComboBox()
        bg_dropdown.addItems(["白色", "深色", "蓝色"])
        general_layout.addWidget(label2)
        general_layout.addWidget(bg_dropdown)

        general_settings.setLayout(general_layout)
        layout.addWidget(general_settings, 0, 0)

        # Advanced settings
        advanced_settings = QGroupBox("高级设置")
        advanced_layout = QVBoxLayout()

        checkboxes = ["启用高级功能", "调试模式", "显示详细日志"]
        for checkbox_label in checkboxes:
            checkbox = QCheckBox(checkbox_label)
            checkbox.setFont(QFont("Arial", 11))
            advanced_layout.addWidget(checkbox)

        advanced_settings.setLayout(advanced_layout)
        layout.addWidget(advanced_settings, 0, 1)

    def start_operations(self):
        """Start selected operations based on user choices"""
        running_features = []

        # Check the selected features and run corresponding operations
        if self.awaken_checkbox.isChecked():
            self.operations.start_awaken()
            running_features.append("开始唤醒")

        if self.mail_checkbox.isChecked():
            self.operations.collect_mail()
            running_features.append("收取邮箱")

        if self.infrastructure_checkbox.isChecked():
            self.operations.collect_infrastructure_and_clues()
            running_features.append("基建材料及线索")

        # Update the status label
        if running_features:
            self.status_label.setText(f"正在运行：{', '.join(running_features)}")
        else:
            self.status_label.setText("正在运行：无")

    def tab_style(self):
        """Set tab widget style"""
        return """
        QTabWidget::pane { border: 1px solid #cccccc; }
        QTabBar::tab { background: #e6e6e6; padding: 10px; margin: 2px; border-radius: 4px; }
        QTabBar::tab:selected { background: #4CAF50; color: white; }
        """

    def start_button_style(self):
        """Set the style for the start button"""
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

    def clear_right_panel(self):
        """Clear all widgets from the right layout"""
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()


def start_ui():
    import sys
    app = QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec())
