from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from dialogs import EditPasswordDialog
from PyQt5.QtWidgets import QMessageBox

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
        """Şifreyi göster/gizle işlevi."""
        QMessageBox.information(self, "Bilgi", "Şifreler hashlenmiş olduğu için gösterilemez.")

    def edit_password(self):
        # Şifre düzenleme işlevi
        self.edit_dialog = EditPasswordDialog()
        if self.edit_dialog.exec_() == QDialog.Accepted:
            # Şifre güncelleme işlemleri burada yapılabilir
            pass

    def delete_password(self):
      confirm = QMessageBox.question(self, "Onay", "Bu platformu silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
      if confirm == QMessageBox.Yes:
        # Veritabanından silme işlemi
        self.veritabani.platform_sil(self.platform_id)  # self.platform_id platformun ID'si olmalı
        QMessageBox.information(self, "Başarılı", "Platform başarıyla silindi.")
        self.accept()