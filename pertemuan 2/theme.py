import customtkinter as ctk

class AppTheme:
    # Mode penampilan default (bisa diganti ke "light")
    APPEARANCE_MODE = "dark"
    # Tema warna dasar komponen utama
    COLOR_THEME = "blue" 
    
    # Warna Kustom untuk Status Absensi agar dashboard terlihat interaktif
    COLOR_HADIR = "#2ecc71"   # Hijau
    COLOR_IZIN = "#3498db"    # Biru
    COLOR_SAKIT = "#f1c40f"   # Kuning
    COLOR_ALPA = "#e74c3c"    # Merah

    @staticmethod
    def setup():
        """Menerapkan konfigurasi visual global."""
        ctk.set_appearance_mode(AppTheme.APPEARANCE_MODE)
        ctk.set_default_color_theme(AppTheme.COLOR_THEME)
