from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QColorDialog, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import random
import string

class AddPasswordDialog(QDialog):
    def __init__(self, veritabani):
        self.veritabani = veritabani
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

        # Göz simgesi/göster-gizle butonu
        self.toggle_password_button = QPushButton("👁")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setFixedWidth(30)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        # Şifre alanı ve göz butonunu yatayda hizala
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)

        # Rastgele Şifre Üret Butonu
        self.generate_password_button = QPushButton("Rastgele Şifre Üret")
        self.generate_password_button.clicked.connect(self.generate_password)

        self.color_button = QPushButton("Renk Seç")
        self.color_button.clicked.connect(self.select_color)
        # Rastgele renk oluştur
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.selected_color = QColor(r, g, b)  # Varsayılan rastgele renk

        # Kaydet ve İptal Butonları
        self.save_button = QPushButton("Kaydet")  # `save_button` burada tanımlanıyor
        self.save_button.clicked.connect(self.accept)  # Kaydet'e basınca diyalogu kapat
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.clicked.connect(self.reject)

        
        # Renk göstergesi
        self.color_label = QLabel()
        self.color_label.setFixedSize(40, 20)
        self.color_label.setStyleSheet(f"background-color: {self.selected_color.name()}; border: 1px solid #333;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.platform_label)
        layout.addWidget(self.platform_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addLayout(password_layout)
        layout.addWidget(self.password_input)
        layout.addWidget(self.generate_password_button)  # Rastgele şifre butonunu ekle
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

    def generate_password(self):
        """Güçlü rastgele şifre üret ve şifre alanına yaz."""
        length = 16
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_input.setText(password)

    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🙈")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁")

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.color_label.setStyleSheet(f"background-color: {self.selected_color.name()}; border: 1px solid #333;")
            self.update_save_button_color()

    def update_save_button_color(self):
        self.save_button.setStyleSheet(f"""
            background-color: {self.selected_color.name()};
            color: white;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
        """)

    def accept(self):

    
        platform_name = self.platform_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        color = self.selected_color.name()  # Seçilen rengin hex kodunu al
    
        # Alanların boş olup olmadığını kontrol et
        if not platform_name or not username or not password:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurmanız gerekiyor!")
            return
    
        # Veritabanına yeni platform ekle
        try:
            self.veritabani.platform_ekle(
                kullanici_id=1,  # Örnek kullanıcı ID'si, bunu dinamik hale getirebilirsiniz
                platform_adi=platform_name,
                kullanici_adi=username,
                sifre=password,
                platform_rengi=color
            )
            QMessageBox.information(self, "Başarılı", "Yeni platform başarıyla eklendi!")
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Platform eklenirken bir hata oluştu: {e}")

class EditPasswordDialog(QDialog):
    def __init__(self, veritabani, platform_id, mevcut_sifre):
        super().__init__()
        self.veritabani = veritabani
        self.platform_id = platform_id
        self.mevcut_sifre = mevcut_sifre  # Mevcut şifreyi sakla
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

        # Kaydet ve İptal Butonları
        self.save_button = QPushButton("Kaydet")
        self.save_button.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        """)
        self.save_button.clicked.connect(self.accept)

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

    def accept(self):
        """Şifre doğrula ve güncelle."""
        old_password = self.old_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_new_password_input.text()

        # Mevcut şifreyi doğrula
        if old_password != self.mevcut_sifre:
            QMessageBox.warning(self, "Hata", "Mevcut şifre yanlış!")
            return

        # Yeni şifrelerin eşleşip eşleşmediğini kontrol et
        if new_password != confirm_password:
            QMessageBox.warning(self, "Hata", "Yeni şifreler eşleşmiyor!")
            return

        # Yeni şifre boş olamaz
        if not new_password:
            QMessageBox.warning(self, "Hata", "Yeni şifre boş olamaz!")
            return

        # Şifreyi veritabanında güncelle
        self.veritabani.guncelle_sifre(self.platform_id, new_password)
        QMessageBox.information(self, "Başarılı", "Şifre başarıyla güncellendi!")
        super().accept()

    def edit_password(self):
        """Şifre düzenleme işlevi."""

        self.edit_dialog = EditPasswordDialog(self.veritabani, self.platform_id, self.password)
        if self.edit_dialog.exec_() == QDialog.Accepted:
            # Yeni şifreyi güncelle
            self.password = self.edit_dialog.new_password_input.text()  # Yeni şifreyi al
            self.password_label.setText("Şifre: ******")  # Şifreyi gizli olarak göster
            QMessageBox.information(self, "Başarılı", "Şifre başarıyla güncellendi!")