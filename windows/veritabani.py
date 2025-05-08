import sqlite3
from sqlite3 import Error
import hashlib
import os

class Veritabani:
    def __init__(self, db_file="sifreler.db"):
        self.conn = self.baglanti_olustur(db_file)
        self.tablolari_olustur()

    def baglanti_olustur(self, db_file):
        """Veritabanı bağlantısı oluşturur."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(f"Veritabanı bağlantı hatası: {e}")
        return conn

    def tablolari_olustur(self):
        """Gerekli tabloları oluşturur."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kullanicilar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kullanici_adi TEXT NOT NULL UNIQUE,
                    sifre_hash BLOB NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS platformlar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kullanici_id INTEGER NOT NULL,
                    platform_adi TEXT NOT NULL,
                    platform_rengi TEXT NOT NULL,
                    kullanici_adi TEXT NOT NULL,
                    sifre_hash BLOB NOT NULL,
                    sifre_duz TEXT,  -- Düz metin şifre sütunu
                    FOREIGN KEY (kullanici_id) REFERENCES kullanicilar (id) ON DELETE CASCADE
                )
            """)
            self.conn.commit()
        except Error as e:
            print(f"Tablo oluşturma hatası: {e}")
    
    def sifre_hashle(self, sifre):
        """Bir şifreyi hashler."""
        salt = os.urandom(16)  # Rastgele bir salt oluştur
        hash_obj = hashlib.pbkdf2_hmac('sha256', sifre.encode(), salt, 100000)
        return salt + hash_obj  # Salt ve hash birleştirilir

    def sifre_dogrula(self, sifre, hashlenmis_sifre):
        """Bir şifreyi hashlenmiş şifre ile doğrular."""
        salt = hashlenmis_sifre[:16]  # İlk 16 bayt salt
        hash_obj = hashlenmis_sifre[16:]  # Geri kalan kısmı hash
        yeni_hash = hashlib.pbkdf2_hmac('sha256', sifre.encode(), salt, 100000)
        return yeni_hash == hash_obj  # Hashler eşleşirse True döner

    def kullanici_ekle(self, kullanici_adi, sifre):
        """Yeni bir kullanıcı ekler."""
        try:
            cursor = self.conn.cursor()
            sifre_hash = self.sifre_hashle(sifre)
            cursor.execute("""
                INSERT INTO kullanicilar (kullanici_adi, sifre_hash)
                VALUES (?, ?)
            """, (kullanici_adi, sifre_hash))
            self.conn.commit()
        except Error as e:
            print(f"Kullanıcı ekleme hatası: {e}")

    def kullanici_var_mi(self, kullanici_adi):
        """Belirtilen kullanıcı adının veritabanında olup olmadığını kontrol eder."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1 FROM kullanicilar WHERE kullanici_adi = ?", (kullanici_adi,))
            return cursor.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
            return False

    def guncelle_sifre(self, platform_id, yeni_sifre):
        """Platformun şifresini günceller."""
        try:
            cursor = self.conn.cursor()
            sifre_hash = self.sifre_hashle(yeni_sifre)  # Şifreyi hashle
            cursor.execute("""
                UPDATE platformlar
                SET sifre_hash = ?, sifre_duz = ?
                WHERE id = ?
            """, (sifre_hash, yeni_sifre, platform_id))
            self.conn.commit()
            print("Şifre başarıyla güncellendi.")
        except Error as e:
            print(f"Şifre güncelleme hatası: {e}")

    def platformlari_getir(self, kullanici_id):
        """Kullanıcıya ait platformları getirir."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, platform_adi, platform_rengi, kullanici_adi, sifre_duz
                FROM platformlar WHERE kullanici_id = ?
            """, (kullanici_id,))
            rows = cursor.fetchall()
            return [
                {
                    'platform_id': row[0],
                    'platform_adi': row[1],
                    'platform_rengi': row[2],
                    'kullanici_adi': row[3],
                    'sifre': row[4]
                }
                for row in rows
            ]
        except Error as e:
            print(f"Platformları getirme hatası: {e}")
            return []
        
    def platform_ekle(self, kullanici_id, platform_adi, kullanici_adi, sifre, platform_rengi):
        """Yeni bir platform ekler."""
        try:
            cursor = self.conn.cursor()
            # Aynı platformun zaten var olup olmadığını kontrol et
            cursor.execute("""
                SELECT 1 FROM platformlar
                WHERE kullanici_id = ? AND platform_adi = ? AND kullanici_adi = ?
            """, (kullanici_id, platform_adi, kullanici_adi))
            if cursor.fetchone():
                print("Bu platform zaten mevcut, tekrar eklenmedi.")
                return  # Platform zaten mevcut, ekleme işlemini durdur
    
            # Platformu ekle
            sifre_hash = self.sifre_hashle(sifre)
            cursor.execute("""
                INSERT INTO platformlar (kullanici_id, platform_adi, platform_rengi, kullanici_adi, sifre_hash, sifre_duz)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (kullanici_id, platform_adi, platform_rengi, kullanici_adi, sifre_hash, sifre))
            self.conn.commit()

        except Error as e:
            print(f"Platform ekleme hatası: {e}")

    def platform_sil(self, platform_id):
        """Belirtilen platformu veritabanından siler."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM platformlar WHERE id = ?", (platform_id,))
            self.conn.commit()

        except Error as e:
            print(f"Platform silme hatası: {e}")