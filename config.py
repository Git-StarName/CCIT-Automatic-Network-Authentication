import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from logger import logger

class Config:
    def __init__(self):
        # 配置文件路径
        self.config_dir = Path.home() / '.campus_network'
        self.config_file = self.config_dir / 'config.json'
        self.key_file = self.config_dir / 'key.key'
        
        # 创建配置目录
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
            
        # 初始化加密key
        self._init_encryption_key()
        
        # 加载配置
        self.config = self._load_config()
        
    def _init_encryption_key(self):
        """初始化或加载加密密钥"""
        if not self.key_file.exists():
            # 使用设备特定信息作为盐值
            salt = self._get_device_salt()
            
            # 使用PBKDF2生成密钥
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            # 使用设备信息生成密钥
            key = base64.urlsafe_b64encode(kdf.derive(self._get_device_info().encode()))
            
            # 保存密钥
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            # 加载已有密钥
            with open(self.key_file, 'rb') as f:
                key = f.read()
                
        self.cipher = Fernet(key)
        
    def _get_device_info(self):
        """获取设备特定信息"""
        try:
            import uuid
            return str(uuid.getnode())  # 使用MAC地址
        except:
            return "default_device_id"
            
    def _get_device_salt(self):
        """生成设备特定的盐值"""
        device_info = self._get_device_info()
        # 使用设备信息的哈希作为盐值
        salt = hashes.Hash(hashes.SHA256())
        salt.update(device_info.encode())
        return salt.finalize()[:16]  # 使用前16字节作为盐值
        
    def _load_config(self):
        """加载配置文件"""
        if not self.config_file.exists():
            default_config = {
                'remember_password': False,
                'username': '',
                'encrypted_password': '',
                'auto_login': True,  # 默认开启自动登录
                'auto_startup': False,  # 默认关闭开机自启
                'is_startup_launch': False  # 标记是否是开机启动
            }
            self._save_config(default_config)
            return default_config
            
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {
                'remember_password': False,
                'username': '',
                'encrypted_password': '',
                'auto_login': True,  # 默认开启自动登录
                'auto_startup': False,  # 默认关闭开机自启
                'is_startup_launch': False  # 标记是否是开机启动
            }
            
    def _save_config(self, config):
        """保存配置到文件"""
        import json
        # 使用更紧凑的JSON格式
        with open(self.config_file, 'w') as f:
            json.dump(config, f, separators=(',', ':'))
            
    def get_credentials(self):
        """获取保存的凭据"""
        username = self.config.get('username', '')
        encrypted_pwd = self.config.get('encrypted_password', '')
        remember = self.config.get('remember_password', False)
        
        logger.info(f"读取凭据 - 用户名: {username}, 记住密码: {remember}")
        
        password = ''
        if encrypted_pwd:
            try:
                password = self.cipher.decrypt(encrypted_pwd.encode()).decode()
                logger.info("密码解密成功")
            except Exception as e:
                logger.error(f"密码解密失败: {str(e)}")
                password = ''
                
        return username, password, remember
        
    def save_credentials(self, username, password, remember=True):
        """保存凭据"""
        logger.info(f"保存凭据 - 用户名: {username}, 记住密码: {remember}")
        
        if remember:
            try:
                encrypted_pwd = self.cipher.encrypt(password.encode()).decode()
                self.config.update({
                    'username': username,
                    'encrypted_password': encrypted_pwd,
                    'remember_password': True
                })
                logger.info("凭据加密保存成功")
            except Exception as e:
                logger.error(f"凭据加密保存失败: {str(e)}")
                self.config.update({
                    'username': '',
                    'encrypted_password': '',
                    'remember_password': False
                })
        else:
            self.config.update({
                'username': '',
                'encrypted_password': '',
                'remember_password': False
            })
            logger.info("清除保存的凭据")
            
        self._save_config(self.config)
        
    def clear_credentials(self):
        """清除保存的凭据"""
        self.config.update({
            'username': '',
            'encrypted_password': '',
            'remember_password': False
        })
        self._save_config(self.config)
        logger.info("凭据已清除")
        
    def get_auto_login(self):
        """获取自动登录设置"""
        return self.config.get('auto_login', True)
        
    def set_auto_login(self, enabled):
        """设置自动登录"""
        self.config['auto_login'] = enabled
        self._save_config(self.config)
        
    def get_auto_startup(self):
        """获取开机自启动设置"""
        return self.config.get('auto_startup', False)
        
    def set_auto_startup(self, enabled):
        """设置开机自启动"""
        self.config['auto_startup'] = enabled
        self._save_config(self.config)
        
    def set_startup_launch(self, is_startup):
        """设置是否是开机启动"""
        self.config['is_startup_launch'] = is_startup
        self._save_config(self.config)
        
    def is_startup_launch(self):
        """检查是否是开机启动"""
        return self.config.get('is_startup_launch', False)