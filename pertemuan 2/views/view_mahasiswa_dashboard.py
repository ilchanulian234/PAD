import customtkinter as ctk
from tkinter import messagebox

from theme import AppTheme


class ViewMahasiswaDashboard(ctk.CTkFrame):
    def __init__(self, parent, user, controller_absensi, on_logout):
        super().__init__(parent)
        self.user = user
        self.ctrl = controller_absensi
        self.on_logout = on_logout

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ===== Header card =====
        header = ctk.CTkFrame(self, fg_color="#1f2a3a", corner_radius=14)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Dashboard Mahasiswa",
            font=("Helvetica", 22, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            header,
            text=f"{self.user['nama_lengkap']}",
            font=("Helvetica", 14, "italic"),
            text_color="#a7b0bf",
        ).grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        # ===== Left: input absen =====
        input_card = ctk.CTkFrame(self, fg_color="#18202b", corner_radius=14)
        input_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=0)
        input_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(input_card, text="Input Absensi", font=("Helvetica", 16, "bold")).pack(
            anchor="w", padx=16, pady=(14, 10)
        )

        # Status picker
        self.status_var = ctk.StringVar(value="Hadir")
        self.dropdown = ctk.CTkOptionMenu(
            input_card,
            values=["Hadir", "Izin", "Sakit", "Alpa"],
            variable=self.status_var,
            width=320,
        )
        self.dropdown.pack(anchor="w", padx=16, pady=(0, 10))

        # Keterangan
        self.ket_input = ctk.CTkEntry(
            input_card,
            placeholder_text="Keterangan (wajib jika Izin/Sakit)",
            width=320,
        )
        self.ket_input.pack(anchor="w", padx=16, pady=(0, 14))

        # Preview status
        preview_frame = ctk.CTkFrame(input_card, fg_color="#111827", corner_radius=12)
        preview_frame.pack(fill="x", padx=16, pady=(0, 14))
        self.preview_label = ctk.CTkLabel(
            preview_frame,
            text="Status dipilih: Hadir",
            font=("Helvetica", 14, "bold"),
            text_color=AppTheme.COLOR_HADIR,
        )
        self.preview_label.pack(anchor="w", padx=12, pady=12)

        self.status_var.trace_add("write", lambda *_: self.refresh_preview())

        # Tombol aksi
        btn_row = ctk.CTkFrame(input_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            btn_row,
            text="Kirim Absen",
            command=self.kirim_absen,
            height=40,
            corner_radius=10,
            fg_color="#2ecc71",
            hover_color="#27ae60",
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_row,
            text="Logout",
            command=self.on_logout,
            height=40,
            corner_radius=10,
            fg_color="#e74c3c",
            hover_color="#c0392b",
        ).pack(side="left")

        # ===== Right: ringkasan & riwayat =====
        summary_card = ctk.CTkFrame(self, fg_color="#18202b", corner_radius=14)
        summary_card.grid(row=1, column=1, sticky="nsew", padx=(10, 0), pady=0)
        summary_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(summary_card, text="Riwayat Terakhir", font=("Helvetica", 16, "bold")).pack(
            anchor="w", padx=16, pady=(14, 10)
        )

        self.riwayat_box = ctk.CTkTextbox(summary_card, corner_radius=10)
        self.riwayat_box.pack(padx=16, pady=(0, 14), fill="both", expand=True)
        self.riwayat_box.configure(state="disabled")

        self.refresh_riwayat()
        self.refresh_preview()

    def refresh_preview(self):
        status = self.status_var.get()
        color_map = {
            "Hadir": AppTheme.COLOR_HADIR,
            "Izin": AppTheme.COLOR_IZIN,
            "Sakit": AppTheme.COLOR_SAKIT,
            "Alpa": AppTheme.COLOR_ALPA,
        }
        self.preview_label.configure(
            text=f"Status dipilih: {status}",
            text_color=color_map.get(status, "#ffffff"),
        )

    def refresh_riwayat(self):
        data = self.ctrl.ambil_riwayat_mahasiswa(self.user["id"])

        self.riwayat_box.configure(state="normal")
        self.riwayat_box.delete("1.0", "end")

        if not data:
            self.riwayat_box.insert("end", "Belum ada riwayat absensi.\n")
            self.riwayat_box.configure(state="disabled")
            return

        for row in data[:10]:
            ket = row.get("keterangan") or "-"
            self.riwayat_box.insert(
                "end",
                f"[{row['tanggal']} {row['waktu']}]\n"
                f"{row['status']} | {ket}\n"
                f"{'-' * 42}\n",
            )

        self.riwayat_box.configure(state="disabled")

    def kirim_absen(self):
        status = self.status_var.get()
        ket = self.ket_input.get()

        res = self.ctrl.input_absen(self.user["id"], status, ket)
        if res["status"] == "success":
            messagebox.showinfo("Berhasil", res["message"])
            self.ket_input.delete(0, "end")
            self.refresh_riwayat()
        else:
            messagebox.showerror("Peringatan", res["message"])

