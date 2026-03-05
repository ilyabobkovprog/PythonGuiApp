#!/usr/bin/env python3
"""
Точка входа приложения
"""
import sys
from app.window import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    """Инициализация и запуск приложения"""
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
