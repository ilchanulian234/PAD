import customtkinter as ctk
from theme import AppTheme

class AccordionRow(ctk.CTkFrame):
    """Komponen tiruan Headless UI Disclosure (Accordion) dengan warna solid premium."""
    def __init__(self, parent, data, bg_color):
        # Menggunakan warna solid terdefinisi guna menghindari bug rendering teks hilang
        super().__init__(parent, fg_color=bg_color, corner_radius=12)
        self.data = data
        self.is_open = False

        self.grid_columnconfigure(0, weight=1)

        # -----------------------------------------------------------------
        # DISCLOSURE BUTTON (Header Baris yang Dapat Diklik)
        # -----------------------------------------------------------------
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent", cursor="hand2")
        self.button_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=14)
        self.button_frame.grid_columnconfigure(0, weight=1)

        # Cap Tanggal dan Nama Mahasiswa (Kiri)
        title_text = f"[{data['tanggal']}]   {data['nama_lengkap']}"
        self.title_label = ctk.CTkLabel(
            self.button_frame, 
            text=title_text, 
            font=("Segoe UI", 13, "bold"), 
            text_color="#ffffff"
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        # Badge Teks Status Kehadiran (Kanan)
        status_txt = data['status'].upper()
        color_badge = AppTheme.COLOR_HADIR if status_txt == "HADIR" else AppTheme.COLOR_IZIN if status_txt == "IZIN" else AppTheme.COLOR_SAKIT if status_txt == "SAKIT" else AppTheme.COLOR_ALPA
        
        self.status_label = ctk.CTkLabel(
            self.button_frame,
            text=status_txt,
            font=("Segoe UI", 11, "bold"),
            text_color=color_badge
        )
        self.status_label.grid(row=0, column=1, sticky="e", padx=(0, 25))

        # Simbol Chevron Interaktif
        self.chevron_label = ctk.CTkLabel(self.button_frame, text="▼", font=("Segoe UI", 11), text_color="#64748b")
        self.chevron_label.grid(row=0, column=2, sticky="e")

        # Mengikat Event Klik di Semua Sisi Komponen Baris
        self.button_frame.bind("<Button-1>", lambda e: self.toggle_disclosure())
        self.title_label.bind("<Button-1>", lambda e: self.toggle_disclosure())
        self.status_label.bind("<Button-1>", lambda e: self.toggle_disclosure())
        self.chevron_label.bind("<Button-1>", lambda e: self.toggle_disclosure())

        # -----------------------------------------------------------------
        # DISCLOSURE PANEL (Konten Detail yang Tersembunyi)
        # -----------------------------------------------------------------
        self.panel_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        ket_txt = data.get('keterangan') or "Tidak ada catatan tambahan."
        detail_text = f"Jam Presensi : {data['waktu']}\nKeterangan   : {ket_txt}"
        
        self.detail_label = ctk.CTkLabel(
            self.panel_frame, 
            text=detail_text, 
            font=("Segoe UI", 12), 
            text_color="#94a3b8", # Pengganti text-white/50 yang stabil
            justify="left",
            anchor="w"
        )
        self.detail_label.pack(fill="x", padx=16, pady=(0, 14))

    def toggle_disclosure(self):
        """Aksi buka-tutup panel saat judul baris diklik."""
        if self.is_open:
            self.panel_frame.grid_forget()
            self.chevron_label.configure(text="▼")
            self.is_open = False
        else:
            self.panel_frame.grid(row=1, column=0, sticky="ew")
            self.chevron_label.configure(text="▲")
            self.is_open = True


class ViewDosenDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, controller_report, on_logout):
        # Disetel menggunakan warna latar belakang solid agar teks putih menyala tajam
        super().__init__(parent, fg_color="#0f172a") 
        self.user = user
        self.report = controller_report
        self.on_logout = on_logout

        # Mengunci keseimbangan layout vertikal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # =================================================================
        # HEADER CARD
        # =================================================================
        header = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=16, height=85)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 16))
        header.grid_propagate(False)
        header.grid_columnconfigure(0, weight=1)
        header.grid_rowconfigure(0, weight=1)

        info_frame = ctk.CTkFrame(header, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="w", padx=20)
        
        ctk.CTkLabel(info_frame, text="DASHBOARD DOSEN", font=("Segoe UI", 18, "bold"), text_color="#ffffff").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(info_frame, text=f"Dosen Aktif: {self.user['nama_lengkap']}", font=("Segoe UI", 12), text_color="#94a3b8").grid(row=1, column=0, sticky="w", pady=(2, 0))

        logout_btn = ctk.CTkButton(
            header, text="Keluar", command=self.on_logout,
            width=90, height=34, corner_radius=10,
            fg_color="#ef4444", hover_color="#dc2626", font=("Segoe UI", 12, "bold")
        )
        logout_btn.grid(row=0, column=1, sticky="e", padx=20)

        # =================================================================
        # ROW STATISTIK 
        # =================================================================
        stats_wrapper = ctk.CTkFrame(self, fg_color="transparent")
        stats_wrapper.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16))
        for i in range(4): stats_wrapper.grid_columnconfigure(i, weight=1)

        stats = self.report.hitung_statistik_kehadiran()
        self._render_stat_card(stats_wrapper, 0, "HADIR", stats.get("Hadir", 0), AppTheme.COLOR_HADIR)
        self._render_stat_card(stats_wrapper, 1, "IZIN", stats.get("Izin", 0), AppTheme.COLOR_IZIN)
        self._render_stat_card(stats_wrapper, 2, "SAKIT", stats.get("Sakit", 0), AppTheme.COLOR_SAKIT)
        self._render_stat_card(stats_wrapper, 3, "ALPA", stats.get("Alpa", 0), AppTheme.COLOR_ALPA)

        # =================================================================
        # CONTAINER DAFTAR JURNAL ACCORDION
        # =================================================================
        accordion_container = ctk.CTkFrame(self, fg_color="transparent")
        accordion_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        accordion_container.grid_columnconfigure(0, weight=1)
        accordion_container.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            accordion_container, 
            text="Riwayat Log Kehadiran Jurnal (Klik baris untuk ekspansi detail)", 
            font=("Segoe UI", 14, "bold"), 
            text_color="#f8fafc"
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # DIKUNCI: Ditambahkan batas ukuran minimal agar area scroll tidak menyusut jadi 0
        self.scroll_list = ctk.CTkScrollableFrame(
            accordion_container, 
            fg_color="#1e293b", 
            corner_radius=16,
            height=300
        )
        self.scroll_list.grid(row=1, column=0, sticky="nsew")
        self.scroll_list.grid_columnconfigure(0, weight=1)

        self.muat_laporan_accordion()

    def _render_stat_card(self, parent, col_index, label, value, text_color):
        card = ctk.CTkFrame(parent, fg_color="#1e293b", height=85, corner_radius=14)
        card.grid(row=0, column=col_index, sticky="ew", padx=(0 if col_index == 0 else 6, 0 if col_index == 3 else 6))
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text=label, font=("Segoe UI", 11, "bold"), text_color="#64748b").grid(row=0, column=0, sticky="w", padx=16, pady=(12, 0))
        ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 26, "bold"), text_color=text_color).grid(row=1, column=0, sticky="w", padx=16, pady=(2, 10))

    def muat_laporan_accordion(self):
        """Memproses kompilasi baris data absensi ke antarmuka."""
        data_laporan = self.report.dapatkan_laporan_dosen()

        # Pembersihan total komponen lama
        for widget in self.scroll_list.winfo_children():
            widget.destroy()

        if not data_laporan:
            empty_lbl = ctk.CTkLabel(
                self.scroll_list, 
                text="Belum ada transaksi log absensi dari mahasiswa.", 
                font=("Segoe UI", 13, "italic"), 
                text_color="#64748b"
            )
            empty_lbl.grid(row=0, column=0, pady=50, sticky="ew")
            return

        for idx, row in enumerate(data_laporan):
            # Pola warna baris berselang-seling yang kokoh (Zebra line style)
            bg_row = "#111827" if idx % 2 == 0 else "#1f2937"
            
            row_accordion = AccordionRow(self.scroll_list, row, bg_row)
            row_accordion.grid(row=idx, column=0, sticky="ew", pady=4, padx=6)
