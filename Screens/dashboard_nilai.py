import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors



class DashboardNilai(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Dashboard Nilai - Siswa")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen  # Simpan referensi ke screen sebelumnya
        self.create_widgets()

    def set_fullscreen_windowed(self):
        # Dapatkan resolusi layar utama
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        # Atur ukuran jendela agar sesuai dengan resolusi layar
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        # Label judul
        ctk.CTkLabel(self, text="Dashboard Nilai", font=("Arial", 24)).place(relx=0.5, rely=0.05, anchor="center")

        # Tabel nilai
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.place(relx=0.5, rely=0.4, relwidth=0.8, relheight=0.4, anchor="center")

        self.load_scores()

        # Tombol Kerjakan Soal
        ctk.CTkButton(self, text="Kerjakan Soal", command=self.open_siswa_screen).place(
            relx=0.3, rely=0.9, relwidth=0.2, relheight=0.07
        )

        # Tombol Kembali
        ctk.CTkButton(self, text="Kembali", command=self.back_to_previous).place(
            relx=0.7, rely=0.9, relwidth=0.2, relheight=0.07
        )

    def load_scores(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT score FROM reports WHERE user_id=?", (self.user_id,))
        scores = cursor.fetchall()
        conn.close()

        # Tampilkan nilai dalam tabel
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if scores:
            for i, (score,) in enumerate(scores):
                ctk.CTkLabel(self.table_frame, text=f"Nilai {i + 1}: {score}", anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        else:
            ctk.CTkLabel(self.table_frame, text="Belum ada nilai.", font=("Arial", 14)).pack(pady=20)

    def open_siswa_screen(self):
        from Screens.siswa_screen import SiswaApp  # Import SiswaApp untuk mengerjakan soal
        self.destroy()
        siswa_app = SiswaApp(self.user_id)
        siswa_app.mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()  # Tampilkan kembali screen sebelumnya