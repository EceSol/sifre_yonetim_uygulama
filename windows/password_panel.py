from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from dialogs import EditPasswordDialog

class PasswordPanel(QDialog):
    def __init__(self, platform_name, username, password, color):
        super().__init__()
        self.setWindowTitle(f"{platform_name} Şifre Paneli")
        self.setMinimumSize(300, 200)

        # Etiketler
        self.username_label = QLabel(f"Kullanıcı Adı: {username}")
        self.username_label.setAlignment(Qt.AlignCenter)
        self.username_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: black;
            padding: 10px;
        """)

        self.password_label = QLabel("Şifre: ******")
        self.password_label.setAlignment(Qt.AlignCenter)
        self.password_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: black;
            padding: 10px;
        """)
        self.password = password  # Şifreyi sakla

        # Butonlar
        self.show_password_button = QPushButton("Şifreyi Göster")
        self.show_password_button.setStyleSheet("""
            background-color: lightgreen;
            border: 2px solid black;
            padding: 10px;
            font-size: 16px;
            color: black;
            border-radius: 5px;
        """)
        self.show_password_button.clicked.connect(self.show_password)

        self.edit_password_button = QPushButton("Şifreyi Düzenle")
        self.edit_password_button.setStyleSheet("""
            background-color: lightblue;
            border: 2px solid black;
            padding: 10px;
            font-size: 16px;
            color: black;
            border-radius: 5px;
        """)
        self.edit_password_button.clicked.connect(self.edit_password)

        self.delete_password_button = QPushButton("Şifreyi Sil")
        self.delete_password_button.setStyleSheet("""
            background-color: red;
            border: 2px solid darkred;
            padding: 10px;
            font-size: 16px;
            color: white;
            border-radius: 5px;
            font-weight: bold;
        """)
        self.delete_password_button.clicked.connect(self.delete_password)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.password_label)
        layout.addWidget(self.show_password_button)
        layout.addWidget(self.edit_password_button)
        layout.addWidget(self.delete_password_button)

        self.setLayout(layout)

    def show_password(self):
        # Şifreyi göster/gizle işlevi
        if self.password_label.text() == "Şifre: ******":
            self.password_label.setText(f"Şifre: {self.password}")
        else:
            self.password_label.setText("Şifre: ******")

    def edit_password(self):
        # Şifre düzenleme işlevi
        self.edit_dialog = EditPasswordDialog()
        if self.edit_dialog.exec_() == QDialog.Accepted:
            # Şifre güncelleme işlemleri burada yapılabilir
            pass

    def delete_password(self):
        # Şifre silme işlevi
        self.password_label.setText("Şifre: ******")
        self.username_label.setText("Kullanıcı Adı: ")