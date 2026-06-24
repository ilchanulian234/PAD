import sys
import os

# Menambahkan folder utama ke path agar bisa mengimpor database.py dengan aman
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database

class ModelUser:
    @staticmethod
    def login(username, password):
        """Memverifikasi username dan password dari database."""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, role, nama_lengkap 
            FROM users 
            WHERE username = ? AND password = ?
        """, (username, password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # Mengubah hasil sqlite3.Row menjadi dictionary Python biasa
            return dict(user)
        return None

    @staticmethod
    def get_all_mahasiswa():
        """Mengambil semua data user yang memiliki role mahasiswa."""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, nama_lengkap FROM users WHERE role = 'mahasiswa'")
        mahasiswa_list = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return mahasiswa_list
