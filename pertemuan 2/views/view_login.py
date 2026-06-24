import customtkinter as ctk
from tkinter import messagebox

class ViewLogin(ctk.CTkFrame):
    def __init__(self, parent, controller_auth, on_login_success):
        super().__init__(parent)
        self.auth = controller_auth
        self.on_success = on_login_success
        
        # Desain Form UI Login
        self.label = ctk.CTkLabel(self, text="SISTEM ABSENSI AKADEMIK", font=("Helvetica", 20, "bold"))
        self.label.pack(pady=30)
        
        self.username_input = ctk.CTkEntry(self, placeholder_text="Username", width=250)
        self.username_input.pack(pady=10)
        
        self.password_input = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=250)
        self.password_input.pack(pady=10)
        
        self.login_btn = ctk.CTkButton(self, text="Login", command=self.proses_login, width=250)
        self.login_btn.pack(pady=20)

    def proses_login(self):
        user = self.username_input.get()
        pwd = self.password_input.get()
        
        # Eksekusi logika otentikasi dari controller
        hasil = self.auth.login(user, pwd)
        if hasil["status"] == "success":
            messagebox.showinfo("Sukses", hasil["message"])
            self.on_success(hasil["user"])
        else:
            messagebox.showerror("Gagal", hasil["message"])
