"""
الملف الرئيسي لتشغيل التطبيق
"""
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """تشغيل التطبيق"""
    app = QApplication(sys.argv)
    
    # تعيين الخط الافتراضي - Sajjala Majala
    from PyQt6.QtGui import QFont
    font = QFont("Sajjala Majala", 14)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

