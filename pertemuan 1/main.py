import customtkinter as ctk
from tkinter import messagebox

# 1. Konfigurasi Tema Global (Mendukung Dark/Light Mode Windows)
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

root = ctk.CTk()
root.title("REAL MADRID CF - PROFILE BIODATA")

# 2. Ukuran Jendela yang Lebih Pas dan Proporsional
window_width = 460
window_height = 580
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.resizable(False, False)

# 3. Kontainer Utama (Card Melengkung yang Elegan)
main_card = ctk.CTkFrame(
    master=root,
    corner_radius=20,
    fg_color=("#FFFFFF", "#1A1A1A"),
    border_width=1,
    border_color=("#E0E0E0", "#2D2D2D")
)
main_card.pack(expand=True, fill="both", padx=25, pady=25)

# 4. AVATAR PROFIL (Simulasi Foto Profil Berbentuk Lingkaran Tanpa File Eksternal)
avatar_frame = ctk.CTkFrame(
    master=main_card,
    width=90,
    height=90,
    corner_radius=45,  # Membuat frame menjadi bulat sempurna
    fg_color=("#001A4E", "#C5A059")  # Biru Gelap di Light, Emas di Dark
)
avatar_frame.pack(pady=(30, 10))
avatar_frame.pack_propagate(False)

avatar_text = ctk.CTkLabel(
    master=avatar_frame,
    text="I",  # Inisial nama depan Anda
    font=("Segoe UI", 36, "bold"),
    text_color="white"
)
avatar_text.place(relx=0.5, rely=0.5, anchor="center")

# 5. HEADER (Nama Utama & Badge Club)
name_title = ctk.CTkLabel(
    master=main_card,
    text="ilchanul",
    font=("Segoe UI", 24, "bold"),
    text_color=("#001A4E", "#FFFFFF")
)
name_title.pack(pady=(5, 2))

badge_label = ctk.CTkLabel(
    master=main_card,
    text="🏆 MADRIDISTA OFfICIAL MEMBER",
    font=("Segoe UI", 10, "bold"),
    text_color="#C5A059"
)
badge_label.pack(pady=(0, 20))

# 6. PANEL INFORMASI UTAMA (Gaya List Bersih)
info_container = ctk.CTkFrame(
    master=main_card, 
    fg_color=("#F5F7FA", "#242424"),
    corner_radius=12
)
info_container.pack(fill="x", padx=25, pady=5)

# Fungsi untuk menyalin teks otomatis saat diklik
def copy_data(text_to_copy):
    root.clipboard_clear()
    root.clipboard_append(text_to_copy)
    messagebox.showinfo("Berhasil Copied", f"Teks '{text_to_copy}' berhasil disalin!")

# Data Biodata Terstruktur
data_biodata = [
    ("NIM / ID", "2023010042", "📋"),
    ("Prodi", "Teknik Informatika", "🎓"),
    ("Mata Kuliah", "Pemrograman Desktop", "💻"),
    ("Kelas", "Tugas 2 - Pertemuan 1", "📝")
]

for title, val, icon in data_biodata:
    row_item = ctk.CTkFrame(master=info_container, fg_color="transparent")
    row_item.pack(fill="x", padx=15, pady=8)
    
    # Judul Kiri
    lbl_title = ctk.CTkLabel(
        master=row_item, 
        text=f"{icon}  {title}", 
        font=("Segoe UI", 12, "bold"),
        text_color=("#7F8C8D", "#95A5A6")
    )
    lbl_title.pack(side="left")
    
    # Isi Kanan (Bisa diklik untuk Copy Paste otomatis)
    btn_val = ctk.CTkButton(
        master=row_item,
        text=val,
        font=("Segoe UI", 13),
        text_color=("#001A4E", "#E3E3E3"),
        fg_color="transparent",
        hover_color=("#E0E6ED", "#333333"),
        height=24,
        anchor="e",
        command=lambda v=val: copy_data(v)
    )
    btn_val.pack(side="right", fill="x")

# 7. TOMBOL SOSIAL MEDIA / LINK EKSTERNAL
def open_instagram():
    messagebox.showinfo("Instagram", "Membuka Link Profil Instagram @ilchanul...")

social_button = ctk.CTkButton(
    master=main_card,
    text="🔗 Kunjungi Instagram",
    font=("Segoe UI", 12, "bold"),
    fg_color="#001A4E",
    hover_color="#002b80",
    text_color="white",
    corner_radius=10,
    height=40,
    command=open_instagram
)
social_button.pack(fill="x", padx=25, pady=(25, 0))

# Catatan kaki penutup kecil
footer_label = ctk.CTkLabel(
    master=main_card,
    text="Hala Madrid y Nada Más",
    font=("Segoe UI Light", 10, "italic"),
    text_color="gray"
)
footer_label.pack(pady=(15, 10))

root.mainloop()
