import os
from PyQt5.QtWidgets import QApplication, QDialog
from login import LoginPage
from main_app import MainApp
from veritabani import Veritabani


if __name__ == "__main__":
    app = QApplication([])

    # Veritabanı bağlantısı
    veritabani = Veritabani()

    # Örnek kullanıcı ekle (eğer yoksa)
    try:
        if not veritabani.kullanici_var_mi("123"):
            veritabani.kullanici_ekle("123", "123")
    except Exception as e:
        print(f"Kullanıcı ekleme hatası: {e}")

    # Giriş ekranını başlat
    login_page = LoginPage(veritabani)  # Veritabanı nesnesini geçiyoruz
    if login_page.exec_() == QDialog.Accepted:
        main_app = MainApp(veritabani)  # Veritabanı nesnesini geçiyoruz
        main_app.show()

    app.exec_()