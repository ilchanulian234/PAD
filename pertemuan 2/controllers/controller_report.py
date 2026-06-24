import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.model_absensi import ModelAbsensi

class ControllerReport:
    def __init__(self):
        self.model = ModelAbsensi()

    def dapatkan_laporan_dosen(self):
        """Mengambil seluruh data absensi untuk dashboard dosen."""
        return self.model.get_semua_rekap_untuk_dosen()

    def hitung_statistik_kehadiran(self):
        """Menghitung total persentase status untuk grafik/ringkasan di dashboard."""
        semua_data = self.model.get_semua_rekap_untuk_dosen()
        
        statistik = {"Hadir": 0, "Izin": 0, "Sakit": 0, "Alpa": 0}
        for data in semua_data:
            status = data.get('status')
            if status in statistik:
                statistik[status] += 1
                
        return statistik
