import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database

class ModelAbsensi:
    @staticmethod
    def catat_kehadiran(mahasiswa_id, status, keterangan=""):
        """Mencatat absensi baru ke dalam database."""
        now = datetime.now()
        tanggal = now.strftime("%Y-%m-%d")
        waktu = now.strftime("%H:%M:%S")
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO absensi (mahasiswa_id, tanggal, waktu, status, keterangan)
                VALUES (?, ?, ?, ?, ?)
            """, (mahasiswa_id, tanggal, waktu, status, keterangan))
            conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] Gagal mencatat absensi: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_rekap_by_mahasiswa(mahasiswa_id):
        """Mengambil riwayat absensi untuk mahasiswa tertentu."""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tanggal, waktu, status, keterangan 
            FROM absensi 
            WHERE mahasiswa_id = ? 
            ORDER BY tanggal DESC, waktu DESC
        """, (mahasiswa_id,))
        
        riwayat = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return riwayat

    @staticmethod
    def get_semua_rekap_untuk_dosen():
        """Mengambil seluruh data absensi mahasiswa untuk tampilan dosen."""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Query bersih untuk menggabungkan tabel absensi dan users
            cursor.execute("""
                SELECT absensi.id, users.nama_lengkap, absensi.tanggal, absensi.waktu, absensi.status, absensi.keterangan
                FROM absensi
                JOIN users ON absensi.mahasiswa_id = users.id
                ORDER BY absensi.tanggal DESC, absensi.waktu DESC
            """)
            laporan = [dict(row) for row in cursor.fetchall()]
            return laporan
        except Exception as e:
            print(f"[ERROR] Gagal mengambil laporan dosen: {e}")
            return []
        finally:
            conn.close()

