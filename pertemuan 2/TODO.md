# TODO - Perbaikan Dashboard

- [x] Pastikan dashboard mahasiswa muncul (fix logika/routing + model)
- [x] Pastikan dashboard dosen muncul (fix method `get_semua_rekap_untuk_dosen`)
- [x] Pastikan database terinisialisasi saat aplikasi start (`database.init_database()` di `main.py`)
- [ ] Upgrade tampilan dashboard agar lebih profesional
  - [ ] Ubah layout login (header card, spacing, style)
  - [ ] Ubah dashboard mahasiswa (card layout, grid, tampilkan ringkasan, tabel/riwayat)
  - [ ] Ubah dashboard dosen (stat cards, filter periode sederhana, tabel riwayat)
  - [ ] Tambah komponen konsisten: header, sidebar kecil, tombol aksi yang rapi
  - [ ] Styling warna status absensi berdasarkan `theme.py`
