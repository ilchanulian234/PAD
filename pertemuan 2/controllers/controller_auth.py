import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.model_user import ModelUser

class ControllerAuth:
    def __init__(self):
        # Menyimpan data user yang sedang aktif login (Session)
        self.current_user = None

    def login(self, username, password):
        """Menangani proses login user."""
        # Validasi input dasar
        if not username or not password:
            return {"status": "error", "message": "Username dan password tidak boleh kosong!"}
        
        # Cek ke database melalui Model
        user = ModelUser.login(username, password)
        
        if user:
            self.current_user = user
            return {
                "status": "success", 
                "message": f"Selamat datang, {user['nama_lengkap']}!",
                "user": user
            }
        
        return {"status": "error", "message": "Username atau password salah!"}

    def logout(self):
        """Menghapus sesi login saat ini."""
        self.current_user = None
        return {"status": "success", "message": "Berhasil logout."}
