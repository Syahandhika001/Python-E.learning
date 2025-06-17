import customtkinter as ctk
import webbrowser
from db import connect_db
from screeninfo import get_monitors

class GradientFrame(ctk.CTkCanvas):
    def __init__(self, master, color1, color2, **kwargs):
        super().__init__(master, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self.draw_gradient)

    def draw_gradient(self, event=None):
        self.delete("gradient")
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
            color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.lower("gradient")

class SiswaBahanAjar(ctk.CTk):
    def __init__(self, user_id, materi_id, previous_screen=None):
        super().__init__()
        self.user_id = user_id
        self.materi_id = materi_id
        self.previous_screen = previous_screen
        self.title("Bahan Ajar")
        self.configure(bg="#7f2100")
        self.set_fullscreen()

        # Gradient background
        self.gradient = GradientFrame(self, color1="#e65c00", color2="#7f2100")
        self.gradient.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.create_widgets()

    def set_fullscreen(self):
        monitor = get_monitors()[0]
        self.geometry(f"{monitor.width}x{monitor.height}+0+0")

    def create_widgets(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT judul FROM materi WHERE id=?", (self.materi_id,))
        result = cursor.fetchone()
        judul = result[0] if result else "Tidak Ditemukan"

        # Judul halaman
        ctk.CTkLabel(
            self.gradient,
            text=f"Bahan Ajar: {judul}",
            font=("Arial", 32, "bold"),
            text_color="#ffcc00",
            bg_color="#e65c00"
        ).pack(pady=(30, 10))

        # Frame utama (scrollable)
        frame_scroll = ctk.CTkScrollableFrame(self.gradient, fg_color="#e6d8a3", corner_radius=16)
        frame_scroll.pack(padx=40, pady=10, fill="both", expand=True)

        cursor.execute("SELECT nama_bahan, file_path FROM bahan_ajar WHERE materi_id=?", (self.materi_id,))
        bahan_list = cursor.fetchall()
        conn.close()

        if not bahan_list:
            ctk.CTkLabel(
                frame_scroll,
                text="Belum ada bahan ajar.",
                font=("Arial", 18, "bold"),
                text_color="#5a1d0a"
            ).pack(pady=20)
        else:
            for nama, file_path in bahan_list:
                # Card frame
                card = ctk.CTkFrame(frame_scroll, fg_color="#fdf2cf", corner_radius=14)
                card.pack(padx=10, pady=10, fill="x")

                # Nama bahan (diperbesar dan tidak terpotong)
                ctk.CTkLabel(
                    card,
                    text=nama,
                    font=("Arial", 18, "bold"),
                    text_color="#7f2100",
                    anchor="w",
                    wraplength=1000,
                    justify="left"
                ).pack(anchor="w", padx=15, pady=(12, 6))

                # Link bahan
                ctk.CTkLabel(
                    card,
                    text=file_path,
                    font=("Arial", 14),
                    text_color="#2980b9",
                    anchor="w",
                    justify="left",
                    wraplength=1000
                ).pack(anchor="w", padx=15, pady=(0, 6))

                # Tombol buka link
                if file_path.startswith("http://") or file_path.startswith("https://"):
                    ctk.CTkButton(
                        card,
                        text="Buka Link",
                        fg_color="#e67c4a",
                        hover_color="#d35400",
                        text_color="#fff",
                        font=("Arial", 14, "bold"),
                        corner_radius=10,
                        command=lambda link=file_path: webbrowser.open(link)
                    ).pack(padx=15, pady=(0, 12), anchor="e")

        # Tombol kembali
        ctk.CTkButton(
            self.gradient,
            text="Kembali",
            command=self.go_back,
            fg_color="#e67c4a",
            hover_color="#d35400",
            text_color="#fff",
            font=("Arial", 18, "bold"),
            corner_radius=10,
            width=130
        ).pack(pady=(10, 30))

    def go_back(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
