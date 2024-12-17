from qfluentwidgets import Theme, setTheme, isDarkTheme
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication

MAIN_STYLE = """
/* 标题栏样式 */
TitleBar {
    background-color: transparent;
    border: none;
    margin: 0;
    padding: 0;
}

TitleBar > QLabel {
    color: black;
    font-family: 'Microsoft YaHei';
}

TitleBar #titleLabel {
    background: transparent;
    font-size: 13px;
    padding: 0 4px;
    margin-left: 4px;
}

/* 标题栏按钮样式 */
MinimizeButton, MaximizeButton, CloseButton {
    width: 46px;
    height: 32px;
    border: none;
    margin: 0;
    padding: 0;
    background-color: transparent;
    border-radius: 0;
}

MinimizeButton:hover, MaximizeButton:hover {
    background-color: rgba(0, 0, 0, 0.1);
}

CloseButton:hover {
    background-color: #e81123;
}

/* 标题栏图标样式 */
TitleBar > QLabel#windowIcon {
    padding: 0 10px;
}

/* 导航栏样式 */
NavigationInterface {
    background-color: rgb(249, 249, 249);
    border: none;
    padding: 0;
}

NavigationInterface NavigationPanel {
    background-color: transparent;
    border: none;
}

/* 导航栏展开面板样式 */
NavigationPanel > QFrame {
    background-color: rgb(249, 249, 249);
    border: none;
    border-radius: 10px;
}

NavigationInterface NavigationPanel NavigationItemButton {
    padding: 15px 20px;
    margin: 5px 10px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 8px;
    color: rgb(51, 51, 51);
}

NavigationInterface NavigationPanel NavigationItemButton:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

NavigationInterface NavigationPanel NavigationItemButton:checked {
    background-color: rgba(0, 0, 0, 0.08);
    color: rgb(0, 120, 212);
}

/* 伸缩页面样式 */
StackedWidget {
    background-color: rgb(249, 249, 249);
    border: none;
}

/* 导航栏展开按钮样式 */
ToolButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    margin: 4px 8px;
    padding: 4px;
}

ToolButton:hover {
    background-color: rgba(0, 0, 0, 0.05);
}

ToolButton:pressed {
    background-color: rgba(0, 0, 0, 0.08);
}

/* 主界面和设置界面样式 */
QFrame#mainInterface, QFrame#settingsInterface {
    background-color: rgb(249, 249, 249);
    border: none;
    border-radius: 10px;
}

QFrame#mainContainer, QFrame#settingsContainer {
    background-color: rgb(249, 249, 249);
    border: none;
}

/* 滚动��域样式 */
SmoothScrollArea {
    background-color: transparent;
    border: none;
}

QScrollArea {
    background-color: transparent;
    border: none;
}

QWidget#scrollAreaWidgetContents {
    background-color: transparent;
    border: none;
}

/* 输入框样式 */
LineEdit {
    border: 1px solid rgb(200, 200, 200);
    border-radius: 5px;
    padding: 5px 10px;
    background: rgba(255, 255, 255, 0.9);
    font-size: 14px;
}

LineEdit:focus {
    border: 2px solid rgb(0, 120, 212);
    background-color: rgba(255, 255, 255, 0.95);
}

/* 复选框样式 */
CheckBox {
    font-size: 14px;
    color: rgba(51, 51, 51, 0.9);
}

/* 按钮样式 */
PushButton {
    border: none;
    border-radius: 5px;
    padding: 8px 16px;
    background-color: rgba(0, 120, 212, 0.9);
    color: white;
    font-size: 16px;
    font-weight: bold;
}

PushButton:hover {
    background-color: rgba(0, 102, 180, 0.9);
}

PushButton:pressed {
    background-color: rgba(0, 90, 158, 0.9);
}

/* 危险按钮样式 */
PushButton[danger=true] {
    background-color: rgb(232, 17, 35);
}

PushButton[danger=true]:hover {
    background-color: rgb(200, 15, 30);
}

PushButton[danger=true]:pressed {
    background-color: rgb(170, 13, 26);
}

/* 禁用状态样式 */
PushButton:disabled {
    background-color: rgb(180, 180, 180);
    color: rgb(240, 240, 240);
}

/* 标题样式 */
TitleLabel {
    font-size: 24px;
    font-weight: bold;
    color: rgba(51, 51, 51, 0.9);
    margin-bottom: 20px;
}
"""

def apply_style(window):
    """应用自定义样式"""
    # 强制使用亮色主题
    setTheme(Theme.LIGHT)
    
    # 应用固定的亮色样式
    window.setStyleSheet("""
    /* 主界面和设置界面样式 */
    QFrame#mainInterface, QFrame#settingsInterface {
        background-color: rgb(249, 249, 249);
        border: none;
        border-radius: 10px;
    }

    QFrame#mainContainer, QFrame#settingsContainer {
        background-color: rgb(255, 255, 255);
        border: 1px solid rgb(200, 200, 200);
        border-radius: 10px;
    }

    /* 导航栏样式 */
    NavigationInterface {
        background-color: rgb(249, 249, 249);
        border: none;
        padding: 0;
    }

    /* 标题和文本样式 */
    TitleLabel, SubtitleLabel {
        color: rgb(51, 51, 51);
    }

    /* 输入框样式 */
    LineEdit {
        background-color: rgb(255, 255, 255);
        border: 1px solid rgb(200, 200, 200);
        color: rgb(51, 51, 51);
    }

    LineEdit:focus {
        border: 2px solid rgb(0, 120, 212);
    }

    /* 复选框样式 */
    CheckBox {
        color: rgb(51, 51, 51);
    }

    /* 其他样式保持不变 */
    """ + MAIN_STYLE)