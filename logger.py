import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self):
        self._init_logger()
    
    def _init_logger(self):
        try:
            # 创建日志目录
            log_dir = Path.home() / '.campus_network' / 'logs'
            if not log_dir.exists():
                log_dir.mkdir(parents=True)
            
            # 配置日志
            self.logger = logging.getLogger('campus_network')
            self.logger.setLevel(logging.INFO)
            
            # 清除现有的处理器
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
            
            # 创建文件处理器 (5MB 大小，保留 3 个备份)
            log_file = log_dir / 'campus_network.log'
            self.file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3,  # 减少备份数量
                encoding='utf-8',
                delay=True  # 延迟创建文件
            )
            
            # 设置格式
            formatter = logging.Formatter(
                '%(asctime)s - %(message)s',
                datefmt='%m-%d %H:%M:%S'
            )
            self.file_handler.setFormatter(formatter)
            
            # 添加处理器
            self.logger.addHandler(self.file_handler)
            
        except Exception as e:
            print(f"日志系统初始化失败: {str(e)}")
            self.logger = logging.getLogger('dummy')
            self.logger.addHandler(logging.NullHandler())
    
    def close(self):
        """关闭日志处理器"""
        try:
            if hasattr(self, 'file_handler'):
                self.file_handler.close()
                self.logger.removeHandler(self.file_handler)
        except:
            pass
    
    def reinit(self):
        """重新初始化日志系统"""
        self._init_logger()
        self.info("日志系统已重新初始化")
    
    def info(self, message):
        """记录信息日志"""
        self.logger.info(message)
    
    def error(self, message):
        """记录错误日志"""
        self.logger.error(message)
    
    def warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)
    
    def debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)

# 创建全局日志实例
logger = Logger() 