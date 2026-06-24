import customtkinter as ctk
from tkinter import messagebox

class ViewMahasiswaDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, controller_absensi, on_logout):
        # Menggunakan warna solid terdefinisi gelap malam agar senada dengan panel dosen
        super().__init__(parent, fg_color="#0f172a")
        self.user = user
        self.ctrl = controller_absensi
        self.on_logout = on_logout
        
        # Konfigurasi Grid Layout Utama Terpusat
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # =================================================================
        # 1. HEADER CARD (INFORMASI MAHASISWA)
        # =================================================================
        header = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=16, height=85)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 16))
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)
        header.grid_rowconfigure(0, weight=1)

        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="w", padx=20)
        
        ctk.CTkLabel(
            info_frame, 
            text="PRESENSI MANDIRI MAHASISWA", 
            font=("Segoe UI", 16, "bold"), 
            text_color="#ffffff"
        ).grid(row=0, column=0, sticky="w")
        
        # DISESUAIKAN: Menggunakan ['nama'] dari database mentor agar tidak kosong/error
        ctk.CTkLabel(
            info_frame, 
            text=f"Nama: {self.user['nama']}  |  Role: Mahasiswa", 
            font=("Segoe UI", 12), 
            text_color="#94a3b8"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Tombol Keluar
        logout_btn = ctk.CTkButton(
            header, text="Keluar", command=self.on_logout,
            width=80, height=34, corner_radius=10,
            fg_color="#ef4444", hover_color="#dc2626", font=("Segoe UI", 11, "bold")
        )
        logout_btn.grid(row=0, column=1, sticky="e", padx=20)

        # =================================================================
        # 2. PANEL FORM INPUT ABSENSI (SAAS FLAT STYLE)
        # =================================================================
        form_card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=16)
        form_card.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        form_card.grid_columnconfigure(0, weight=1)
        
        # Judul Form
        ctk.CTkLabel(
            form_card, 
            text="Silakan Isi Status Kehadiran Anda Hari Ini", 
            font=("Segoe UI", 14, "bold"), 
            text_color="#f8fafc"
        ).pack(pady=(24, 16))

        # Dropdown Opsi Status Absen
        self.status_var = ctk.StringVar(value="Hadir")
        self.dropdown = ctk.CTkOptionMenu(
            form_card, 
            values=["Hadir", "Izin", "Sakit"], 
            variable=self.status_var,
            width=280,
            height=38,
            corner_radius=10,
            fg_color="#334155",
            button_color="#475569",
            button_hover_color="#64748b"
        )
        self.dropdown.pack(pady=10)
        
        # Kolom Teks Input Catatan Keterangan
        self.ket_input = ctk.CTkEntry(
            form_card, 
            placeholder_text="Keterangan Tambahan (Wajib isi jika Anda Izin / Sakit)", 
            width=280,
            height=38,
            corner_radius=10,
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#ffffff"
        )
        self.ket_input.pack(pady=10)
        
        # Tombol Submit Utama
        submit_btn = ctk.CTkButton(
            form_card, 
            text="SUBMIT PRESENSI", 
            command=self.kirim_absen, 
            width=280,
            height=42,
            corner_radius=12,
            fg_color="#10b981", 
            hover_color="#059669",
            font=("Segoe UI", 13, "bold")
        )
        submit_btn.pack(pady=(20, 24))

    def kirim_absen(self):
        """Mengirim data form ke controller dengan validasi keamanan."""
        status = self.status_var.get()
        ket = self.ket_input.get()
        
        # Mengirim data ke controller absensi
        res = self.ctrl.input_absen(self.user['id'], status, ket)
        if res["status"] == "success":
            messagebox.showinfo("Berhasil", "Presensi Anda hari ini sukses tersimpan di database!")
            self.ket_input.delete(0, 'end')
        else:
            messagebox.showerror("Gagal", res["message"])
