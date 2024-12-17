import PyInstaller.__main__
import os
from pathlib import Path
from icon import create_heart_icon
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
import sys

# 初始化 QApplication
app = QApplication(sys.argv)

# 生成图标文件
icon = create_heart_icon()
icon_path = Path('icon.ico')
pixmap = icon.pixmap(256, 256)
pixmap.save('icon.ico')

# 打包参数
params = [
    'main.py',  # 主程序文件
    '--name=CCIT自动网络认证',  # 程序名称
    '--icon=icon.ico',  # 图标
    '--noconsole',  # 不显示控制台
    '--version-file=version.txt',  # 版本信息文件
    '--onefile',  # 打包成单个文件
    '--clean',  # 清理临时文件
    '--windowed',  # Windows下不显示控制台
    '--hidden-import=PyQt6',
    '--hidden-import=PyQt6.QtCore',
    '--hidden-import=PyQt6.QtGui',
    '--hidden-import=PyQt6.QtWidgets',
    '--hidden-import=qfluentwidgets',
    '--optimize=2',
    '--noupx',
]

# 创建版本信息文件
version_info = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'080404b0',
          [StringStruct(u'CompanyName', u''),
           StringStruct(u'FileDescription', u'CCIT自动网络认证'),
           StringStruct(u'FileVersion', u'1.0.0.0'),
           StringStruct(u'InternalName', u'CCIT自动网络认证'),
           StringStruct(u'LegalCopyright', u''),
           StringStruct(u'OriginalFilename', u'CCIT自动网络认证.exe'),
           StringStruct(u'ProductName', u'CCIT自动网络认证'),
           StringStruct(u'ProductVersion', u'1.0.0.0')])
      ])
  ]
)
'''

# 写入版本信息
with open('version.txt', 'w', encoding='utf-8') as f:
    f.write(version_info)

# 执行打包
PyInstaller.__main__.run(params)

# 清理临时文件
if icon_path.exists():
    icon_path.unlink()
if Path('version.txt').exists():
    Path('version.txt').unlink() 