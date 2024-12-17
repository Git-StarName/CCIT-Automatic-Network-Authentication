from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
from gui import MainWindow
from logger import logger
import win32event
import win32api
import winerror

def main():
    # 检查启动参数
    is_startup = '--startup' in sys.argv
    
    # 创建互斥锁
    mutex = win32event.CreateMutex(None, False, "CCIT_Network_Auth_Mutex")
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        # 如果互斥锁已存在，说明程序已经在运行
        if not is_startup:  # 只在非自启动时显示提示
            QMessageBox.warning(
                None,
                "提示",
                "程序已经在运行中\n请查看系统托盘",
                QMessageBox.StandardButton.Ok
            )
        return

    # 初始化日志
    if is_startup:
        logger.info("通过开机自启动启动程序")
    else:
        logger.info("程序启动")
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    logger.info("主窗口已创建")
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
#作者：Chara