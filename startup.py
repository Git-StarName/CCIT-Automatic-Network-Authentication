import os
import sys
from pathlib import Path
import winreg as reg
from logger import logger

def add_to_startup():
    """添加程序到开机自启动"""
    try:
        # 获取程序路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe
            app_path = sys.executable
        else:
            # 如果是python脚本
            app_path = sys.argv[0]
        
        # 转换为绝对路径
        app_path = str(Path(app_path).resolve())
        
        # 打开注册表项
        key = reg.OpenKey(
            reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            reg.KEY_SET_VALUE
        )
        
        # 写入注册表
        reg.SetValueEx(key, "CampusNetwork", 0, reg.REG_SZ, f'"{app_path}"')
        reg.CloseKey(key)
        logger.info("已添加到开机自启动")
        return True
    except Exception as e:
        logger.error(f"添加开机自启动失败: {str(e)}")
        return False

def remove_from_startup():
    """从开机自启动中移除程序"""
    try:
        # 打开注册表项
        key = reg.OpenKey(
            reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            reg.KEY_SET_VALUE
        )
        
        # 删除注册表项
        reg.DeleteValue(key, "CampusNetwork")
        reg.CloseKey(key)
        logger.info("已从开机自启动移除")
        return True
    except Exception as e:
        logger.error(f"移除开机自启动失败: {str(e)}")
        return False

def check_startup():
    """检查程序是否在开机自启动中"""
    try:
        key = reg.OpenKey(
            reg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            reg.KEY_READ
        )
        try:
            reg.QueryValueEx(key, "CampusNetwork")
            reg.CloseKey(key)
            return True
        except:
            reg.CloseKey(key)
            return False
    except:
        return False 