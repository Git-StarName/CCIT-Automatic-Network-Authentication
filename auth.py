import requests
import re
from urllib.parse import quote, parse_qs, urlparse
import time
from logger import logger

class Authenticator:
    def __init__(self):
        self.base_url = "http://10.10.10.52"
        self.login_url = f"{self.base_url}/eportal/InterFace.do?method=login"
        self.session = requests.session()
        # 设置更短的超时时间
        self.timeout = 3
        # 设置更紧凑的请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Accept': '*/*',
            'Connection': 'close'
        })
        
    def check_status(self):
        """检查当前认证状态"""
        try:
            status_url = f"{self.base_url}/eportal/InterFace.do?method=getOnlineUserInfo"
            r = self.session.get(status_url, timeout=self.timeout)
            r.close()  # 立即关闭连接
            status = r.json()
            return status.get('result') == 'success' and status.get('userIndex')
        except:
            return False

    def get_auth_params(self):
        """从当前URL中获取认证参数"""
        try:
            logger.info("开始获取认证参数")
            
            # 获取认证页面
            logger.info("获取认证页面")
            auth_url = f"{self.base_url}/eportal/index.jsp"
            response = self.session.get(auth_url, timeout=5)
            logger.info(f"访问URL: {response.url}")
            
            # 从URL中获取认证参数
            if '?' in response.url:
                return response.url
            
            # 如果没有参数，尝试获取重定向参数
            params = {
                'wlanuserip': '',
                'wlanacname': '',
                'ssid': '',
                'nasip': '',
                'mac': '',
                'url': '',
                't': 'wireless-v2'
            }
            response = self.session.get(auth_url, params=params, timeout=5)
            if '?' in response.url:
                return response.url
            
            logger.error("未获取到认证参数")
            return None
            
        except Exception as e:
            logger.error(f"获取认证参数时出错: {str(e)}")
            return None
        
    def login(self, username, password):
        try:
            # 检查认证状态
            try:
                status_url = f"{self.base_url}/eportal/InterFace.do?method=getOnlineUserInfo"
                r = self.session.get(status_url, timeout=5)
                status = r.json()
                if status.get('result') == 'success' and status.get('userIndex'):
                    logger.info("已经认证，无需重复登录")
                    return True
            except:
                pass

            # 获取登录页面
            auth_url = self.get_auth_params()
            if not auth_url:
                logger.error("未获取到认证参数")
                return False
            
            query_string = auth_url.split('?', 1)[1] if '?' in auth_url else ''
            if not query_string:
                logger.error("未获取到必要参数")
                return False
            
            logger.info(f"认证queryString: {query_string}")
            
            # 发送登录请求
            data = {
                "userId": username,
                "password": password,
                "service": "",
                "queryString": quote(query_string),
                "passwordEncrypt": "false"
            }
            
            logger.info(f"发送登录请求: {self.login_url}")
            
            response = self.session.post(self.login_url, data=data, headers=self.session.headers, timeout=5)
            response.encoding = 'utf-8'
            logger.info(f"登录响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                logger.error("登录请求失败")
                return False
            
            try:
                result = response.json()
                success = result.get("result") == "success"
                logger.info(f"登录结果: {'成功' if success else '失败'}")
                return success
            except:
                logger.error("解析登录响应失败")
                return False
            
        except Exception as e:
            logger.error(f"认证出错: {str(e)}")
            return False 