import customtkinter as ctk
from db import connect_db
from screeninfo import get_monitors


class GradientFrame(ctk.CTkFrame):
    def __init__(self, master, color1, color2, **kwargs):
        super().__init__(master, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.canvas.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = height
        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
            self.canvas.create_line(0, i, width, i, fill=color)


class ReportNilai(ctk.CTk):
    def __init__(self, user_id, previous_screen=None):
        super().__init__()
        self.title("ReportNilai")
        self.set_fullscreen_windowed()
        self.user_id = user_id
        self.previous_screen = previous_screen  # Simpan referensi ke screen sebelumnya
        # Gradient background
        self.gradient = GradientFrame(self, "#ff6600", "#b34700")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.create_widgets()

    def set_fullscreen_windowed(self):
        # Dapatkan resolusi layar utama
        monitor = get_monitors()[0]
        screen_width = monitor.width
        screen_height = monitor.height

        # Atur ukuran jendela agar sesuai dengan resolusi layar
        self.geometry(f"{screen_width}x{screen_height}+0+0")

    def create_widgets(self):
        card = ctk.CTkFrame(self.gradient, fg_color="#f2f2f2", corner_radius=16)
        card.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")

        # Label judul
        ctk.CTkLabel(card, text="Report Nilai Siswa", font=("Arial", 28, "bold"), text_color="#ff6600").place(relx=0.5, rely=0.08, anchor="center")

        # Tabel nilai
        self.table_frame = ctk.CTkFrame(card, fg_color="#fff7e6", corner_radius=8)
        self.table_frame.place(relx=0.5, rely=0.55, relwidth=0.9, relheight=0.7, anchor="center")

        self.load_reports()

        # Tombol Kembali
        ctk.CTkButton(card, text="Kembali", command=self.back_to_previous, fg_color="#b34700", hover_color="#ff6600", text_color="white", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.93, relwidth=0.2, relheight=0.07, anchor="center")

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