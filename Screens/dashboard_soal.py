import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors


class DashboardSoal(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("Dashboard Soal - Guru")
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
        ctk.CTkLabel(self, text="Dashboard Soal", font=("Arial", 24)).place(relx=0.5, rely=0.05, anchor="center")

        # Tombol Report Nilai
        ctk.CTkButton(self, text="Report Nilai", command=self.open_report_nilai).place(
        relx=0.5, rely=0.9, relwidth=0.2, relheight=0.07
        )
        # Tombol Buat Soal
        ctk.CTkButton(self, text="Buat Soal", command=self.open_guru_screen).place(
            relx=0.3, rely=0.9, relwidth=0.2, relheight=0.07
        )

        # Tombol Kembali
        ctk.CTkButton(self, text="Kembali", command=self.exit_to_login).place(
            relx=0.7, rely=0.9, relwidth=0.2, relheight=0.07
        )

        # Tabel soal
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.7, anchor="center")

        self.load_questions()

    def open_report_nilai(self):
        from Screens.report_nilai import ReportNilai  # Import ReportNilai
        self.withdraw()  # Sembunyikan window saat ini
        report_nilai = ReportNilai(self.user_id, previous_screen=self)
        report_nilai.mainloop()

    def open_guru_screen(self):
        from Screens.guru_screen import GuruApp  # Import GuruApp untuk "Buat Soal"
        self.withdraw()
        guru_app = GuruApp(self.user_id, previous_screen=self)
        guru_app.mainloop()

    def open_edit_soal(self, soal_id):
        from Screens.edit_soal import EditSoal # Import EditSoal untuk mengedit soal
        self.withdraw()
        edit_soal = EditSoal(soal_id, self.user_id, previous_screen=self)
        edit_soal.mainloop()

    def load_questions(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, question FROM questions")
        questions = cursor.fetchall()
        conn.close()

        # Tampilkan soal dalam tabel
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if questions:
            for i, (q_id, question) in enumerate(questions):
                # Tambahkan tombol untuk setiap soal
                ctk.CTkButton(
                    self.table_frame,
                    text=f"{i + 1}. {question}",
                    command=lambda q_id=q_id: self.open_edit_soal(q_id),
                    anchor="w"
                ).grid(row=i, column=0, sticky="w", padx=10, pady=5)
        else:
            ctk.CTkLabel(self.table_frame, text="Belum ada soal.", font=("Arial", 14)).pack(pady=20)


    def exit_to_login(self):
        from Screens.login_screen import LoginApp
        self.destroy()
        login_app = LoginApp()
        login_app.mainloop()

    def back_to_previous(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()  # Tampilkan kembali screen sebelumnya