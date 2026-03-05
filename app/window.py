"""
Главное окно приложения
"""
import sqlite3
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QMenuBar, QMenu,
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit,
    QCheckBox, QMessageBox, QFormLayout, QGroupBox
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont, QGuiApplication


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.db_connection = sqlite3.connect('persons.db')
        self.create_table()
        self.init_ui()
    
    def center_window(self):
        """Центрирование окна на экране"""
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_geometry.center())
        self.move(frame_geometry.topLeft())
    
    def create_table(self):
        """Создание таблицы в базе данных"""
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                surname TEXT NOT NULL,
                name TEXT NOT NULL,
                patronymic TEXT,
                birth_date TEXT,
                registration_date TEXT,
                criminal_record TEXT,
                address TEXT
            )
        ''')
        self.db_connection.commit()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        # Установка основных параметров окна
        self.setWindowTitle("Python GUI Application")
        self.setGeometry(100, 100, 1000, 700)
        self.center_window()
        
        # Создание меню
        self.create_menu_bar()
        
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        main_layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Управление данными персон")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Дата постановки', 'Судимость', 'Адрес'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_row_selected)
        main_layout.addWidget(self.table)
        
        # Форма редактирования
        form_group = QGroupBox("Редактирование")
        form_layout = QFormLayout()
        
        self.surname_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.patronymic_edit = QLineEdit()
        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setCalendarPopup(True)
        self.registration_date_edit = QDateEdit()
        self.registration_date_edit.setCalendarPopup(True)
        self.criminal_record_edit = QCheckBox("Есть судимость")
        self.address_edit = QLineEdit()
        
        form_layout.addRow("Фамилия:", self.surname_edit)
        form_layout.addRow("Имя:", self.name_edit)
        form_layout.addRow("Отчество:", self.patronymic_edit)
        form_layout.addRow("Дата рождения:", self.birth_date_edit)
        form_layout.addRow("Дата постановки:", self.registration_date_edit)
        form_layout.addRow("", self.criminal_record_edit)
        form_layout.addRow("Адрес:", self.address_edit)
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.on_add)
        button_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.on_edit)
        self.edit_btn.setEnabled(False)
        button_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.on_delete)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        self.clear_form_btn = QPushButton("Очистить форму")
        self.clear_form_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_form_btn)
        
        main_layout.addLayout(button_layout)
        
        # Установка макета для центрального виджета
        central_widget.setLayout(main_layout)
        
        # Загрузка данных
        self.load_data()
    
    def create_menu_bar(self):
        """Создание меню приложения"""
        menubar = self.menuBar()
        
        # Меню "Файл"
        file_menu = menubar.addMenu("&Файл")
        
        exit_action = file_menu.addAction("&Выход")
        exit_action.triggered.connect(self.close)
        
        # Меню "Справка"
        help_menu = menubar.addMenu("&Справка")
        
        about_action = help_menu.addAction("&О программе")
        about_action.triggered.connect(self.show_about)
    
    def load_data(self):
        """Загрузка данных из базы данных в таблицу"""
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM persons")
        rows = cursor.fetchall()
        
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row_idx, col_idx, item)
    
    def on_add(self):
        """Добавление новой записи"""
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        birth_date = self.birth_date_edit.date().toString("yyyy-MM-dd")
        registration_date = self.registration_date_edit.date().toString("yyyy-MM-dd")
        criminal_record = "Да" if self.criminal_record_edit.isChecked() else "Нет"
        address = self.address_edit.text().strip()
        
        if not surname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и имя обязательны!")
            return
        
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO persons (surname, name, patronymic, birth_date, registration_date, criminal_record, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (surname, name, patronymic, birth_date, registration_date, criminal_record, address))
        self.db_connection.commit()
        
        self.load_data()
        self.clear_form()
        QMessageBox.information(self, "Успех", "Запись добавлена!")
    
    def on_edit(self):
        """Редактирование выбранной записи"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        person_id = int(self.table.item(row, 0).text())
        
        surname = self.surname_edit.text().strip()
        name = self.name_edit.text().strip()
        patronymic = self.patronymic_edit.text().strip()
        birth_date = self.birth_date_edit.date().toString("yyyy-MM-dd")
        registration_date = self.registration_date_edit.date().toString("yyyy-MM-dd")
        criminal_record = "Да" if self.criminal_record_edit.isChecked() else "Нет"
        address = self.address_edit.text().strip()
        
        if not surname or not name:
            QMessageBox.warning(self, "Ошибка", "Фамилия и имя обязательны!")
            return
        
        cursor = self.db_connection.cursor()
        cursor.execute('''
            UPDATE persons SET surname=?, name=?, patronymic=?, birth_date=?, registration_date=?, criminal_record=?, address=?
            WHERE id=?
        ''', (surname, name, patronymic, birth_date, registration_date, criminal_record, address, person_id))
        self.db_connection.commit()
        
        self.load_data()
        self.clear_form()
        QMessageBox.information(self, "Успех", "Запись обновлена!")
    
    def on_delete(self):
        """Удаление выбранной записи"""
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        reply = QMessageBox.question(self, "Подтверждение", "Удалить выбранную запись?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        row = selected_rows[0].row()
        person_id = int(self.table.item(row, 0).text())
        
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM persons WHERE id=?", (person_id,))
        self.db_connection.commit()
        
        self.load_data()
        self.clear_form()
        QMessageBox.information(self, "Успех", "Запись удалена!")
    
    def on_row_selected(self):
        """Обработчик выбора строки в таблице"""
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            self.surname_edit.setText(self.table.item(row, 1).text())
            self.name_edit.setText(self.table.item(row, 2).text())
            self.patronymic_edit.setText(self.table.item(row, 3).text() or "")
            birth_date = QDate.fromString(self.table.item(row, 4).text(), "yyyy-MM-dd")
            self.birth_date_edit.setDate(birth_date)
            reg_date = QDate.fromString(self.table.item(row, 5).text(), "yyyy-MM-dd")
            self.registration_date_edit.setDate(reg_date)
            self.criminal_record_edit.setChecked(self.table.item(row, 6).text() == "Да")
            self.address_edit.setText(self.table.item(row, 7).text() or "")
            
            self.edit_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        else:
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
    
    def clear_form(self):
        """Очистка формы"""
        self.surname_edit.clear()
        self.name_edit.clear()
        self.patronymic_edit.clear()
        self.birth_date_edit.setDate(QDate.currentDate())
        self.registration_date_edit.setDate(QDate.currentDate())
        self.criminal_record_edit.setChecked(False)
        self.address_edit.clear()
        self.table.clearSelection()
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
    
    def show_about(self):
        """Отображение информации о программе"""
        QMessageBox.about(self, "О программе", "Управление данными персон\nВерсия 0.1.0\nСоздано с использованием PyQt5")
