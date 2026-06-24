import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.model_absensi import ModelAbsensi

class ControllerAbsensi:
    def __init__(self):
        self.model = ModelAbsensi()

    def input_absen(self, mahasiswa_id, status, keterangan=""):
        """Validasi dan kirim data absensi ke model."""
        status_valid = ['Hadir', 'Izin', 'Sakit', 'Alpa']
        
        if status not in status_valid:
            return {"status": "error", "message": "Status absensi tidak valid!"}
            
        if (status == 'Izin' or status == 'Sakit') and not keterangan.strip():
            return {"status": "error", "message": "Keterangan wajib diisi jika Izin atau Sakit!"}

        # Simpan ke database
        sukses = self.model.catat_kehadiran(mahasiswa_id, status, keterangan)
        
        if sukses:
            return {"status": "success", "message": "Absensi berhasil dicatat!"}
        return {"status": "error", "message": "Gagal menyimpan data ke database."}

    def ambil_riwayat_mahasiswa(self, mahasiswa_id):
        """Mengambil data riwayat untuk mahasiswa tertentu."""
        return self.model.get_rekap_by_mahasiswa(mahasiswa_id)
