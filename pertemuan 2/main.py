import customtkinter as ctk
from theme import AppTheme
from controllers.controller_auth import ControllerAuth
from controllers.controller_absensi import ControllerAbsensi
from controllers.controller_report import ControllerReport
from views.view_login import ViewLogin
from views.view_mahasiswa_dashboard import ViewMahasiswaDashboard
from views.view_dosen_dashboard import ViewDosenDashboard

import database


class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Setup Konfigurasi Window & Tema Kustom
        AppTheme.setup()
        self.title("Sistem Absensi Bisnis Pro")
        self.geometry("600x500")
        self.resizable(False, False)
        
        # 2. Inisialisasi Seluruh Controller
        self.auth_ctrl = ControllerAuth()
        self.absen_ctrl = ControllerAbsensi()
        self.report_ctrl = ControllerReport()
        
        # Container utama tempat bertukarnya halaman (View)
        self.current_frame = None
        self.buka_halaman_login()

    def ganti_halaman(self, frame_class, *args, **kwargs):
        """Fungsi dinamis untuk menghapus halaman lama dan memuat halaman baru."""
        if self.current_frame is not None:
            self.current_frame.destroy()
        
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def buka_halaman_login(self):
        self.ganti_halaman(ViewLogin, self.auth_ctrl, on_login_success=self.buka_dashboard_sesuai_role)

    def buka_dashboard_sesuai_role(self, user_session):
        if user_session["role"] == "dosen":
            self.ganti_halaman(ViewDosenDashboard, user_session, self.report_ctrl, on_logout=self.proses_logout)
        elif user_session["role"] == "mahasiswa":
            self.ganti_halaman(ViewMahasiswaDashboard, user_session, self.absen_ctrl, on_logout=self.proses_logout)

    def proses_logout(self):
        self.auth_ctrl.logout()
        self.buka_halaman_login()

if __name__ == "__main__":
    database.init_database()
    app = MainApplication()
    app.mainloop()
