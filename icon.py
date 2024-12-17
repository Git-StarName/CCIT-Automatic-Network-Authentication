from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt

def create_heart_icon():
    """创建像素风格的红心图标"""
    # 创建32x32的图标
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
    
    # 设置红色
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(255, 0, 0))
    
    # 像素爱心的点阵图案
    heart_pixels = [
        "  ****  ****  ",
        " ************ ",
        " ************ ",
        " ************ ",
        "  **********  ",
        "   ********   ",
        "    ******    ",
        "     ****     ",
        "      **      "
    ]
    
    # 计算起始位置使心形居中
    pixel_size = 2
    start_x = (32 - len(heart_pixels[0]) * pixel_size) // 2
    start_y = (32 - len(heart_pixels) * pixel_size) // 2
    
    # 绘制像素
    for y, row in enumerate(heart_pixels):
        for x, pixel in enumerate(row):
            if pixel == '*':
                painter.drawRect(
                    start_x + x * pixel_size,
                    start_y + y * pixel_size,
                    pixel_size,
                    pixel_size
                )
    
    painter.end()
    return QIcon(pixmap) 