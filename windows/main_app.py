from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QDialog, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from password_panel import PasswordPanel
from dialogs import AddPasswordDialog
from veritabani import Veritabani

class MainApp(QWidget):
    def __init__(self, veritabani):
        super().__init__()
        self.setWindowTitle("Şifre Yöneticisi")
        self.setMinimumSize(600, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Veritabanı bağlantısı
        self.veritabani = veritabani

        # Platformlar listesi (veritabanından yükleniyor)
        self.platforms = self.veritabani.platformlari_getir(1) or []

        # Layout
        self.layout = QGridLayout()

        # + butonunu tanımlayın
        self.add_platform_button = QPushButton("+")
        self.add_platform_button.setStyleSheet("""
            background-color: lightgreen;
            border: 2px solid black;
            padding: 20px;
            font-size: 24px;
            color: black;
            border-radius: 10px;
        """)
        self.add_platform_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.add_platform_button.clicked.connect(self.add_password)

        # Platformları ekleyin
        self.add_default_platforms()

        self.setLayout(self.layout)

    def add_default_platforms(self):
        # Grid'i temizle
        self.clear_layout()

        # Veritabanından platformları yükle

        for i, platform in enumerate(self.platforms):
            print(platform)  # Debugging için platform bilgilerini yazdır
            platform_name = platform['platform_adi']
            username = platform['kullanici_adi']
            password = platform['sifre']
            color = QColor(platform['platform_rengi'])
            platform_id = platform['platform_id']  # platform_id'yi alın
            self.add_platform_to_grid(platform_name, username, password, color, i // 2, i % 2, platform_id)

        # + butonunu en sona ekle
        row = len(self.platforms) // 2
        col = len(self.platforms) % 2
        self.layout.addWidget(self.add_platform_button, row, col)

    def add_platform_to_grid(self, platform_name, username, password, color, row, col, platform_id):
        """Platformu grid'e ekler."""
        label = QLabel(platform_name)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"""
            background-color: {color.name()};
            border: 2px solid black;
            padding: 20px;
            font-size: 16px;
            color: black;
            border-radius: 10px;
        """)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        label.mousePressEvent = lambda event: self.open_password_panel(platform_name, username, password, color, platform_id)
        self.layout.addWidget(label, row, col)

    def open_password_panel(self, platform_name, username, password, color, platform_id):
     """Platforma tıklandığında şifre panelini açar."""
     self.panel = PasswordPanel(self.veritabani, platform_id, platform_name, username, password, color, parent=self)
     self.panel.exec_()

    def add_password(self):
        # Yeni platform ekleme diyalogunu açar
        self.add_dialog = AddPasswordDialog(self.veritabani)
        if self.add_dialog.exec_() == QDialog.Accepted:
            platform_name = self.add_dialog.platform_input.text()
            username = self.add_dialog.username_input.text()
            password = self.add_dialog.password_input.text()
            color = self.add_dialog.selected_color.name()  # Kullanıcının seçtiği renk
    
            # Yeni platformu veritabanına ekle
            try:
                self.veritabani.platform_ekle(
                    kullanici_id=1,  # Örnek kullanıcı ID'si
                    platform_adi=platform_name,
                    kullanici_adi=username,
                    sifre=password,
                    platform_rengi=color
                )
    
                # Platformları yeniden yükle ve UI'yi güncelle
                self.platforms = self.veritabani.platformlari_getir(1)
                self.clear_layout()
                self.add_default_platforms()
    
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Platform eklenirken bir hata oluştu: {e}")
                
    def delete_platform(self, platform_name):
        # Platformu listeden ve grid'den siler
        for i, platform in enumerate(self.platforms):
            if platform['platform_adi'] == platform_name:
                # Platformu listeden sil
                self.platforms.pop(i)
                break
            
        # Grid'i temizle ve yeniden oluştur
        self.clear_layout()
        self.add_default_platforms()
    
        # + butonunu en sona ekle
        row = len(self.platforms) // 2
        col = len(self.platforms) % 2
        self.layout.addWidget(self.add_platform_button, row, col)
    
    def clear_layout(self):
        # Grid'deki tüm widget'ları temizler (+ butonu hariç)
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget and widget != self.add_platform_button:
                widget.deleteLater()