from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox,QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class LoginPage(QDialog):
    def __init__(self, veritabani):
        super().__init__()
        self.veritabani = veritabani  # Veritabanı nesnesini sınıfa ekle
        self.setWindowTitle("Kullanıcı Girişi")
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            background-color: #f4f4f9;
            border-radius: 10px;
        """)

        # Kullanıcı Adı
        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_label.setFont(QFont("Arial", 12))
        self.username_label.setStyleSheet("color: #333333;")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.username_input.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        """)

        # Şifre
        self.password_label = QLabel("Şifre:")
        self.password_label.setFont(QFont("Arial", 12))
        self.password_label.setStyleSheet("color: #333333;")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 10px;
            font-size: 14px;
            border: 2px solid #4CAF50;
            border-radius: 5px;
        """)

         # Göz simgesi/göster-gizle butonu
        self.toggle_password_button = QPushButton("👁")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setFixedWidth(30)
        self.toggle_password_button.setFixedHeight(self.password_input.sizeHint().height())
        self.toggle_password_button.setStyleSheet("""
            border: none;
            background: transparent;
            font-size: 18px;
        """)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        # Şifre alanı ve göz butonunu yatayda hizala
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)


        # Giriş Butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        """)
        self.login_button.clicked.connect(self.login)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addLayout(password_layout)
        layout.addWidget(self.login_button)
        layout.setSpacing(15)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁")

    def login(self):
        """Kullanıcı giriş işlemi."""
        kullanici_adi = self.username_input.text()
        sifre = self.password_input.text()

        # Veritabanından kullanıcıyı al ve doğrula
        cursor = self.veritabani.conn.cursor()
        cursor.execute("SELECT sifre_hash FROM kullanicilar WHERE kullanici_adi = ?", (kullanici_adi,))
        result = cursor.fetchone()
        if result and self.veritabani.sifre_dogrula(sifre, result[0]):
            QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            self.accept()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")
