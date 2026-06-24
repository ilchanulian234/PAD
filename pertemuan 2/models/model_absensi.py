import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database

class ModelAbsensi:
    @staticmethod
    def catat_kehadiran(user_id, status, keterangan=""):
        now = datetime.now()
        tanggal = now.strftime("%Y-%m-%d")
        jam_masuk = now.strftime("%H:%M:%S")
        
        conn = database.get_connection()
        cursor = conn.cursor()
        try:
            # Menggunakan skema kolom database mentor
            cursor.execute("""
                INSERT INTO absensi (user_id, tanggal, jam_masuk, status, keterangan)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, tanggal) DO UPDATE SET
                status = excluded.status,
                keterangan = excluded.keterangan
            """, (user_id, tanggal, jam_masuk, status, keterangan))
            conn.commit()
            return True
        except Exception as e:
            print(f"[ERROR] Gagal mencatat absensi: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_semua_rekap_untuk_dosen():
        conn = database.get_connection()
        cursor = conn.cursor()
        try:
            # Join menggunakan user_id dan memanggil kolom nama
            cursor.execute("""
                SELECT absensi.id, users.nama, absensi.tanggal, absensi.jam_masuk, absensi.status, absensi.keterangan
                FROM absensi
                JOIN users ON absensi.user_id = users.id
                ORDER BY absensi.tanggal DESC, absensi.jam_masuk DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"[ERROR] Gagal mengambil laporan: {e}")
            return []
        finally:
            conn.close()
