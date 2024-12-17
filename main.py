from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
from gui import MainWindow
from logger import logger
import win32event
import win32api
import winerror
import os

def main():
    # 创建互斥锁
    mutex = win32event.CreateMutex(None, False, "CCIT_Network_Auth_Mutex")
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        # 如果互斥锁已存在，说明程序已经在运行
        QMessageBox.warning(
            None,
            "提示",
            "程序已经在运行中\n请查看系统托盘",
            QMessageBox.StandardButton.Ok
        )
        return

    # 初始化日志
    logger.info("程序启动")
    
    # 检查是否是开机启动
    is_startup = len(sys.argv) > 1 and sys.argv[1] == '--startup'
    if is_startup:
        logger.info("通过开机自启动启动程序")
    
    app = QApplication(sys.argv)
    # 设置应用程序不会在最后一个窗口关闭时退出
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    # 不显示主窗口，程序启动后直接在系统托盘运行
    
    # 记录窗口创建
    logger.info("主窗口已创建")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
#作者：Chara