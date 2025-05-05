from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QColorDialog, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class AddPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Şifre Ekle")
        self.setMinimumSize(400, 300)

        # Platform Adı
        self.platform_label = QLabel("Platform Adı:")
        self.platform_input = QLineEdit()

        # Kullanıcı Adı
        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()

        # Şifre
        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Şifre gizleme

        # Renk Seçme Butonu
        self.color_button = QPushButton("Renk Seç")
        self.color_button.clicked.connect(self.select_color)
        self.selected_color = QColor("white")  # Varsayılan renk

        # Kaydet ve İptal Butonları
        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.accept)  # Kaydet'e basınca diyalogu kapat
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.clicked.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.platform_label)
        layout.addWidget(self.platform_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.color_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        # Stil Sayfası
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()};")


class EditPasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifre Düzenle")
        self.setMinimumSize(400, 300)
        self.setStyleSheet("""
            background-color: #f4f4f9;
            border-radius: 10px;
        """)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Mevcut Şifre
        self.old_password_label = QLabel("Mevcut Şifre:")
        self.old_password_label.setStyleSheet("font-size: 14px; color: #333333;")
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        """)

        # Yeni Şifre
        self.new_password_label = QLabel("Yeni Şifre:")
        self.new_password_label.setStyleSheet("font-size: 14px; color: #333333;")
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        """)

        # Yeni Şifreyi Tekrar Girin
        self.confirm_new_password_label = QLabel("Yeni Şifreyi Tekrar Girin:")
        self.confirm_new_password_label.setStyleSheet("font-size: 14px; color: #333333;")
        self.confirm_new_password_input = QLineEdit()
        self.confirm_new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_new_password_input.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        """)

        # Butonlar
        self.save_button = QPushButton("Kaydet")
        self.save_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        """)
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setStyleSheet("""
            background-color: #f44336;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        """)
        self.cancel_button.clicked.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.old_password_label)
        layout.addWidget(self.old_password_input)
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_new_password_label)
        layout.addWidget(self.confirm_new_password_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        layout.setSpacing(15)  # Elemanlar arası boşluk

        self.setLayout(layout)