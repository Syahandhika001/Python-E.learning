import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors


class ReportNilai(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Report Nilai - Guru")
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
        ctk.CTkLabel(self, text="Report Nilai Siswa", font=("Arial", 24)).place(relx=0.5, rely=0.05, anchor="center")

        # Tabel nilai
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.7, anchor="center")

        self.load_reports()

        # Tombol Kembali
        ctk.CTkButton(self, text="Kembali", command=self.back_to_previous).place(
            relx=0.5, rely=0.9, relwidth=0.2, relheight=0.07, anchor="center"
        )

    def load_reports(self):
        conn = connect_db()
        cursor = conn.cursor()

        # Ambil data nama siswa dan nilai mereka
        cursor.execute('''
            SELECT users.username, reports.score
            FROM reports
            JOIN users ON reports.user_id = users.id
            WHERE users.role = "siswa"
        ''')
        reports = cursor.fetchall()
        conn.close()

        # Tampilkan data dalam tabel
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if reports:
            # Header tabel
            ctk.CTkLabel(self.table_frame, text="Nama Siswa", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(self.table_frame, text="Nilai", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")

            # Data tabel
            for i, (username, score) in enumerate(reports, start=1):
                ctk.CTkLabel(self.table_frame, text=username, anchor="w").grid(row=i, column=0, padx=10, pady=5, sticky="w")
                ctk.CTkLabel(self.table_frame, text=str(score), anchor="w").grid(row=i, column=1, padx=10, pady=5, sticky="w")
        else:
            ctk.CTkLabel(self.table_frame, text="Belum ada data nilai.", font=("Arial", 14)).pack(pady=20)

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()  # Tampilkan kembali screen sebelumnya