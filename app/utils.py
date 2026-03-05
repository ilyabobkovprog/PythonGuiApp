"""
Утилиты приложения
"""
from PyQt5.QtWidgets import QMessageBox


def show_info(parent, title, message):
    """Показать информационное сообщение"""
    QMessageBox.information(parent, title, message)


def show_warning(parent, title, message):
    """Показать предупреждение"""
    QMessageBox.warning(parent, title, message)


def show_error(parent, title, message):
    """Показать ошибку"""
    QMessageBox.critical(parent, title, message)


def show_question(parent, title, message):
    """Показать вопрос и вернуть результат"""
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.Yes | QMessageBox.No
    )
    return reply == QMessageBox.Yes
