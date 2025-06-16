import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors



class DashboardNilai(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("DashboardNilai")
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

        # Tombol Report Nilai
        ctk.CTkButton(self, text="Report Nilai", command=self.open_report_nilai).place(
        relx=0.5, rely=0.9, relwidth=0.2, relheight=0.07
        )
        # Tombol Kembali
        ctk.CTkButton(self, text="Kembali", command=self.back_to_previous).place(
            relx=0.7, rely=0.9, relwidth=0.2, relheight=0.07
        )

        # Tambahkan tombol ke dashboard siswa
        ctk.CTkButton(self, text="Dashboard Materi & Soal", command=self.open_siswa_dashboard).place(
            relx=0.5, rely=0.8, relwidth=0.3, relheight=0.08, anchor="center"
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

    def open_report_nilai(self):
        from Screens.report_nilai import ReportNilaiScreen  # Ganti dengan nama file dan kelas yang sesuai
        self.withdraw()
        report_nilai_screen = ReportNilaiScreen(self.user_id, previous_screen=self)
        report_nilai_screen.mainloop()

    def open_siswa_dashboard(self):
        from Screens.siswa_dashboard import SiswaDashboard
        self.withdraw()
        siswa_dashboard = SiswaDashboard(self.user_id, previous_screen=self)
        siswa_dashboard.mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()   # Tampilkan kembali screen sebelumnya