from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QVBoxLayout, QFrame, QApplication, QLineEdit,
                           QSystemTrayIcon, QMenu)
from PyQt6.QtGui import QColor, QPalette
from qfluentwidgets import (FluentWindow, LineEdit, MessageBox, InfoBar, 
                          InfoBarPosition, TitleLabel, PrimaryPushButton,
                          SubtitleLabel, SmoothScrollArea, SwitchButton,
                          PushButton)
from qfluentwidgets import FluentIcon as FIF
from auth import Authenticator
from config import Config
from style import apply_style
from icon import create_heart_icon
from startup import add_to_startup, remove_from_startup, check_startup
import weakref
import time
import sys

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        # 检查启动参数
        self.is_startup = '--startup' in sys.argv
        self.is_minimized = '--minimized' in sys.argv
        
        # 初始化基本组件
        self._init_basic_components()
        
        # 初始化其他组件
        self._init_delayed_components()
        
        # 根据启动方式决定显示状态
        if self.is_startup:
            # 开机自启动时隐藏窗口，尝试自动登录
            self.hide()
            self._try_auto_login()
        else:
            # 用户手动启动时显示窗口
            self.show()

    def _init_basic_components(self):
        """初始化基本组件"""
        # 初始化认证器和配置
        self.auth = Authenticator()
        self.config = Config()
        
        # 初始化系统托盘
        self._init_tray()
        
        # 设置窗口基本属性
        self.setWindowTitle("校园网认证")
        self.resize(1000, 600)
        self.setFixedSize(1000, 600)

    def _init_delayed_components(self):
        """延迟初始化的组件"""
        # 初始化界面
        self._init_ui()
        self._load_saved_credentials()
        self._init_settings()
        
        # 设置导航栏宽度
        self.navigationInterface.setFixedWidth(220)
        
        # 应用样式
        apply_style(self)
        
        # 根据启动方式决定是否显示窗口
        if self.is_startup:
            self.hide()
            self._try_auto_login()
        else:
            self.show()
            if self.config.get_auto_login():
                self._try_auto_login()

    def _init_ui(self):
        # 创建主界面
        main_widget = SmoothScrollArea()
        main_container = QFrame()
        main_widget.setObjectName("mainInterface")
        main_container.setObjectName("mainContainer")
        main_container.setContentsMargins(50, 20, 50, 50)
        
        # 设置滚动区域
        main_widget.setWidget(main_container)
        main_widget.setViewportMargins(0, 10, 0, 0)
        main_widget.setWidgetResizable(True)
        
        # 添加到导航栏
        self.addSubInterface(
            interface=main_widget,
            icon=FIF.HOME_FILL,
            text="校园网认证",
            position=0,
        )
        
        # 创建垂直布局
        layout = QVBoxLayout(main_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # 创建控件
        # 添加标题
        title = TitleLabel('校园网认证', self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.username_edit = LineEdit(self)
        self.username_edit.setPlaceholderText("用户名")
        self.username_edit.setFixedWidth(400)
        self.username_edit.setFixedHeight(40)
        
        self.password_edit = LineEdit(self)
        self.password_edit.setPlaceholderText("密码")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFixedWidth(400)
        self.password_edit.setFixedHeight(40)
        # 添加车键登录支持
        self.password_edit.returnPressed.connect(self._on_login)
        
        # 添加记住密码复选框
        from qfluentwidgets import CheckBox
        self.remember_checkbox = CheckBox('记住密码', self)
        self.remember_checkbox.setFixedWidth(400)
        self.remember_checkbox.setFixedHeight(40)
        
        self.login_btn = PushButton("登录", self)
        self.login_btn.setIcon(FIF.LINK)
        self.login_btn.setFixedWidth(400)
        self.login_btn.setFixedHeight(50)
        self.login_btn.clicked.connect(self._on_login)
        
        # 添加控件布
        layout.addWidget(title)
        layout.addSpacing(30)  # 添加间距
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.remember_checkbox)
        layout.addWidget(self.login_btn)
        
    def _load_saved_credentials(self):
        # 加载保存的凭据
        username, password, remember = self.config.get_credentials()
        if username:
            self.username_edit.setText(username)
        if password:
            self.password_edit.setText(password)
        self.remember_checkbox.setChecked(remember)
        
    def _on_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        
        # 禁用登录按钮，显示加载状态
        self.login_btn.setEnabled(False)
        self.login_btn.setText("登录中...")
        QApplication.processEvents()  # 确保UI更新
        
        # 检查认证状态
        if self.auth.check_status():
            InfoBar.success(
                title="提示",
                content="您已经认证，无需重复登录",
                position=InfoBarPosition.TOP,
                parent=self
            )
            # 恢复按钮状态
            self.login_btn.setEnabled(True)
            self.login_btn.setText("登录")
            return
        
        if not username or not password:
            MessageBox("提示", "请输入用户名和密码", self).exec()
            # 恢复按钮状态
            self.login_btn.setEnabled(True)
            self.login_btn.setText("登录")
            return
            
        # 尝试认证
        success = self.auth.login(username, password)
        
        # 恢复按钮状态
        self.login_btn.setEnabled(True)
        self.login_btn.setText("登录")
        
        if success:
            # 保存凭据
            self.config.save_credentials(
                username,
                password,
                self.remember_checkbox.isChecked()
            )
            
            InfoBar.success(
                title="成功",
                content="网络认证成功",
                position=InfoBarPosition.TOP,
                parent=self
            )
            
            # 如果是开机启动且登录成功，3秒后自动关闭
            if self.is_startup:
                QTimer.singleShot(3000, self.quit_app)
        else:
            InfoBar.error(
                title="错误",
                content="认证失败,请检查用户名密码",
                position=InfoBarPosition.TOP,
                parent=self
            ) 

    def _init_settings(self):
        """初始化设置界面"""
        settings_widget = SmoothScrollArea()
        settings_container = QFrame()
        settings_widget.setObjectName("settingsInterface")
        settings_container.setObjectName("settingsContainer")
        settings_container.setStyleSheet("background-color: transparent; border: none;")
        settings_container.setContentsMargins(0, 0, 0, 0)
        
        # 设置滚动区域
        settings_widget.setWidget(settings_container)
        settings_widget.setViewportMargins(0, 0, 0, 0)
        settings_widget.setWidgetResizable(True)
        
        # 创建垂直布局
        layout = QVBoxLayout(settings_container)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)  # 小控件间距
        layout.setContentsMargins(50, 50, 50, 30)
        
        # 添加标题
        title = TitleLabel('设置', self)
        title.setFixedHeight(40)
        layout.addWidget(title)
        
        # 添加分隔
        layout.addSpacing(5)  # 减小分隔距离
        
        # 添加自动登录标题
        login_title = SubtitleLabel('自动登录', self)
        login_title.setFixedHeight(25)  # 减小标题高度
        layout.addWidget(login_title)
        
        # 添加自动登录开关
        from qfluentwidgets import SwitchButton
        auto_login_switch = SwitchButton('开启', self)
        auto_login_switch.setChecked(self.config.get_auto_login())
        auto_login_switch.checkedChanged.connect(self._on_auto_login_changed)
        auto_login_switch.setText('开启' if auto_login_switch.isChecked() else '关闭')
        auto_login_switch.checkedChanged.connect(
            lambda checked: auto_login_switch.setText('开启' if checked else '关闭')
        )
        auto_login_switch.setFixedWidth(400)
        auto_login_switch.setFixedHeight(35)  # 减小开关高度
        layout.addWidget(auto_login_switch)
        
        # 添加分隔
        layout.addSpacing(5)
        
        # 添加开机自启动标题
        startup_title = SubtitleLabel('开机自启动', self)
        startup_title.setFixedHeight(25)
        layout.addWidget(startup_title)
        
        # 添加开机自启动开关
        startup_switch = SwitchButton('开启', self)
        startup_switch.setChecked(check_startup())
        startup_switch.checkedChanged.connect(self._on_startup_changed)
        startup_switch.setText('开启' if startup_switch.isChecked() else '关闭')
        startup_switch.checkedChanged.connect(
            lambda checked: startup_switch.setText('开启' if checked else '关闭')
        )
        startup_switch.setFixedWidth(400)
        startup_switch.setFixedHeight(35)
        layout.addWidget(startup_switch)
        
        # 添加分隔
        layout.addSpacing(5)
        
        # 添加账号管理标题
        account_title = SubtitleLabel('账号管理', self)
        account_title.setFixedHeight(25)
        layout.addWidget(account_title)
        
        # 添加删除凭据按钮
        delete_btn = PrimaryPushButton('删除保存的账号密码', self)
        delete_btn.setIcon(FIF.DELETE)
        delete_btn.clicked.connect(self._on_delete_credentials)
        delete_btn.setFixedWidth(400)
        delete_btn.setFixedHeight(35)
        delete_btn.setProperty('danger', True)
        self.delete_btn = delete_btn
        layout.addWidget(delete_btn)
        
        # 添加分隔
        layout.addSpacing(5)
        
        # 添加日志管理标题
        log_title = SubtitleLabel('日志管理', self)
        log_title.setFixedHeight(25)
        layout.addWidget(log_title)
        
        # 打开日志文件按钮
        open_log_btn = PrimaryPushButton('打开日志文件', self)
        open_log_btn.setIcon(FIF.DOCUMENT)
        open_log_btn.clicked.connect(self._on_open_log)
        open_log_btn.setFixedWidth(400)
        open_log_btn.setFixedHeight(35)
        layout.addWidget(open_log_btn)
        
        # 清除日志文件按钮
        clear_log_btn = PrimaryPushButton('清除日志文件', self)
        clear_log_btn.setIcon(FIF.DELETE)
        clear_log_btn.clicked.connect(self._on_clear_log)
        clear_log_btn.setFixedWidth(400)
        clear_log_btn.setFixedHeight(35)
        layout.addWidget(clear_log_btn)
        
        # 添加到导航栏
        self.addSubInterface(
            interface=settings_widget,
            icon=FIF.SETTING,
            text='设置',
            position=1,
        )
        
    def _on_delete_credentials(self):
        """处理删除凭据事件"""
        # 显示确认对话框
        msg = MessageBox(
            '确认删除',
            '确定要删除保存的账号密码吗？此操作不可恢复。',
            self
        )
        msg.yesButton.setText('确定')
        msg.cancelButton.setText('取消')
        
        if msg.exec():
            # 用户确认删除
            self.config.clear_credentials()
            
            # 清空输入框
            self.username_edit.clear()
            self.password_edit.clear()
            self.remember_checkbox.setChecked(False)
            
            # 显示成功提示
            InfoBar.success(
                title='成功',
                content='账号密码已删除',
                position=InfoBarPosition.TOP,
                parent=self
            ) 

    def _on_open_log(self):
        """打开日志文件"""
        from pathlib import Path
        import os
        import platform
        
        log_file = Path.home() / '.campus_network' / 'logs' / 'campus_network.log'
        
        if not log_file.exists():
            InfoBar.warning(
                title='提示',
                content='日志文件不存在',
                position=InfoBarPosition.TOP,
                parent=self
            )
            return
        
        # 根据操作系统使用不同的命令打开文件
        system = platform.system()
        try:
            if system == 'Windows':
                os.startfile(str(log_file))
            elif system == 'Darwin':  # macOS
                os.system(f'open "{str(log_file)}"')
            else:  # Linux
                os.system(f'xdg-open "{str(log_file)}"')
                
            InfoBar.success(
                title='成功',
                content='已打开日志文件',
                position=InfoBarPosition.TOP,
                parent=self
            )
        except Exception as e:
            InfoBar.error(
                title='错误',
                content=f'打开日志文件失败: {str(e)}',
                position=InfoBarPosition.TOP,
                parent=self
            )

    def _on_clear_log(self):
        """清除日志文件"""
        msg = MessageBox(
            '确认清除',
            '确定要清除日志文件吗？操作不可恢复。',
            self
        )
        msg.yesButton.setText('确定')
        msg.cancelButton.setText('取消')
        
        if msg.exec():
            from pathlib import Path
            from logger import logger
            log_file = Path.home() / '.campus_network' / 'logs' / 'campus_network.log'
            
            try:
                # 关闭现有日志处理器
                logger.close()
                
                # 删除文件
                if log_file.exists():
                    log_file.unlink()
                
                # 重新初始化日志系统
                logger.reinit()
                
                InfoBar.success(
                    title='成功',
                    content='日志文件已清除',
                    position=InfoBarPosition.TOP,
                    parent=self
                )
            except Exception as e:
                InfoBar.error(
                    title='错误',
                    content=f'清除日志文件失败: {str(e)}',
                    position=InfoBarPosition.TOP,
                    parent=self
                ) 

    def _init_tray(self):
        """初始化系统托盘"""
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        icon = create_heart_icon()
        self._icon_ref = weakref.ref(icon)  # 使用弱引用
        self.tray_icon.setIcon(icon)
        
        # 使用轻量级菜单
        tray_menu = QMenu()
        tray_menu.setStyleSheet("QMenu { menu-scrollable: 0; }")
        
        # 添加菜单项
        show_action = tray_menu.addAction('显示主窗口')
        show_action.triggered.connect(self.show_window)
        
        check_action = tray_menu.addAction('检查认证状态')
        check_action.triggered.connect(self._check_auth_status)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction('退出')
        quit_action.triggered.connect(self.quit_app)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)
        
        # 添加托盘图标点击事件
        self.tray_icon.activated.connect(self._on_tray_activated)
        
        # 显示托盘图标
        self.tray_icon.show()
        
    def _on_tray_activated(self, reason):
        """处理托盘图标点击事件"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            # 如果窗口隐藏，则显示并激活
            if not self.isVisible():
                self.show()
                self.activateWindow()
            # 如果窗口已显示，则将其置顶
            else:
                self.activateWindow()
        
    def show_window(self):
        """显示主窗口"""
        self.show()
        self.activateWindow()
        
    def _check_auth_status(self):
        """检查认证状态"""
        # 避免频繁创建消息
        if not hasattr(self, '_last_check_time'):
            self._last_check_time = 0
        
        current_time = time.time()
        if current_time - self._last_check_time < 2:  # 限制检查频率
            return
        
        self._last_check_time = current_time
        
        if self.auth.check_status():
            self.tray_icon.showMessage(
                '认证状态',
                '网络已认证',
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            self.tray_icon.showMessage(
                '认证状态',
                '网络未认证',
                QSystemTrayIcon.MessageIcon.Warning,
                2000
            )
            
    def quit_app(self):
        """退出应用"""
        # 记录程序退出
        from logger import logger
        logger.info("程序退出")
        
        # 清理系统托盘并退出
        self.tray_icon.hide()
        QApplication.quit()
        
    def closeEvent(self, event):
        """重写关闭事件，直接退出程序"""
        self.quit_app()

    def _try_auto_login(self):
        """尝试自动登录"""
        username, password, remember = self.config.get_credentials()
        
        if username and password and remember:
            # 有保存的凭据
            if self.config.get_auto_login():
                # 尝试认证
                success = self.auth.login(username, password)
                
                if success:
                    self.tray_icon.showMessage(
                        '校园网认证',
                        '自动登录成功',
                        QSystemTrayIcon.MessageIcon.Information,
                        2000
                    )
                    # 如果是开机启动且登录成功，3秒后自动关闭
                    if self.is_startup:
                        QTimer.singleShot(3000, self.quit_app)
                else:
                    self.tray_icon.showMessage(
                        '校园网认证',
                        '自动登录失败，请手动登录',
                        QSystemTrayIcon.MessageIcon.Warning,
                        2000
                    )
                    # 登录失败时显示主窗口
                    self.show()
        else:
            # 没有保存的凭据，显示主窗口
            self.show()

    def _on_auto_login_changed(self, checked):
        """处理自动登录开关状态改变"""
        self.config.set_auto_login(checked)
        InfoBar.success(
            title='成功',
            content='已' + ('开启' if checked else '关闭') + '自动登录功能',
            position=InfoBarPosition.TOP,
            parent=self
        )

    def _on_startup_changed(self, checked):
        """处理开机自启动开关状态改变"""
        if checked:
            success = add_to_startup()
        else:
            success = remove_from_startup()
            
        if success:
            self.config.set_auto_startup(checked)
            InfoBar.success(
                title='成功',
                content='已' + ('开启' if checked else '关闭') + '开机自启动',
                position=InfoBarPosition.TOP,
                parent=self
            )
        else:
            InfoBar.error(
                title='错误',
                content='设置开机自启动失败',
                position=InfoBarPosition.TOP,
                parent=self
            )