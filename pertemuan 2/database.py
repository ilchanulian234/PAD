import sqlite3
import os

DATABASE_NAME = "sistem_absensi.db"

def get_connection():
    """Membuat dan mengembalikan koneksi ke database SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Mengembalikan hasil query dalam bentuk dictionary (bukan tuple) agar mudah dibaca di Controller
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Membuat tabel-tabel utama jika belum ada (Skema Database)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Tabel Users (Untuk login Dosen dan Mahasiswa)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('dosen', 'mahasiswa')) NOT NULL,
        nama_lengkap TEXT NOT NULL
    )
    """)
    
    # 2. Tabel Absensi
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS absensi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mahasiswa_id INTEGER NOT NULL,
        tanggal TEXT NOT NULL,
        waktu TEXT NOT NULL,
        status TEXT CHECK(status IN ('Hadir', 'Izin', 'Sakit', 'Alpa')) NOT NULL,
        keterangan TEXT,
        FOREIGN KEY (mahasiswa_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    
    # 3. Membuat Akun Demo Otomatis jika database masih kosong (Seeding)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Password idealnya di-hash (misal menggunakan bcrypt), ini versi teks dasar untuk inisialisasi awal
        demo_users = [
            ('dosen1', 'pass123', 'dosen', 'Dr. Budi Santoso'),
            ('mhs1', 'mhs123', 'mahasiswa', 'Rian Hidayat'),
            ('mhs2', 'mhs123', 'mahasiswa', 'Siti Aminah')
        ]
        cursor.executemany("""
        INSERT INTO users (username, password, role, nama_lengkap) 
        VALUES (?, ?, ?, ?)
        """, demo_users)
        print("[INFO] Database kosong. Akun demo berhasil dibuat!")

    conn.commit()
    conn.close()
    print("[SUCCESS] Inisialisasi database selesai.")

if __name__ == "__main__":
    # Menjalankan fungsi ini langsung jika file database.py dieksekusi
    init_database()
