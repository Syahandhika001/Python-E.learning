import customtkinter as ctk
from screeninfo import get_monitors
from db import connect_db

# --- CLASS GRADIENT FRAME (langsung disatukan) ---
class GradientFrame(ctk.CTkCanvas):
    def __init__(self, master, color1="#e65c00", color2="#7f2100"):
        super().__init__(master, highlightthickness=0)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        steps = 100
        for i in range(steps):
            r1, g1, b1 = self.winfo_rgb(self.color1)
            r2, g2, b2 = self.winfo_rgb(self.color2)
            r = int(r1 + (r2 - r1) * i / steps) >> 8
            g = int(g1 + (g2 - g1) * i / steps) >> 8
            b = int(b1 + (b2 - b1) * i / steps) >> 8
            color = f'#{r:02x}{g:02x}{b:02x}'
            y1 = int(i * height / steps)
            y2 = int((i+1) * height / steps)
            self.create_rectangle(0, y1, width, y2, outline="", fill=color, tags=("gradient",))
        self.lower("gradient")

# --- KELAS UTAMA UNTUK SISWA MENGERJAKAN SOAL ---
class SiswaKerjakanSoal(ctk.CTk):
    def __init__(self, user_id, materi_id, previous_screen=None):
        super().__init__()
        self.user_id = user_id
        self.materi_id = materi_id
        self.previous_screen = previous_screen
        self.current_index = 0
        self.selected_answers = {}
        self.score = 0
        self.title("Kerjakan Soal - Siswa")
        self.set_fullscreen()

        self.gradient = GradientFrame(self)
        self.gradient.pack(fill="both", expand=True)

        self.load_questions()

    def set_fullscreen(self):
        monitor = get_monitors()[0]
        self.geometry(f"{monitor.width}x{monitor.height}+0+0")

    def load_questions(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE materi_id=?", (self.materi_id,))
        self.questions = cursor.fetchall()
        conn.close()

        if self.questions:
            self.show_question(self.current_index)
        else:
            self.show_info("Belum ada soal.", error=True)

    def show_question(self, index):
        for widget in self.gradient.winfo_children():
            widget.destroy()

        q = self.questions[index]
        ctk.CTkLabel(self.gradient, text=f"Soal {index+1}:", font=("Arial", 28, "bold"), text_color="#5a1d0a").pack(pady=(40, 10))
        ctk.CTkLabel(self.gradient, text=q[2], font=("Arial", 20, "bold"), text_color="#5a1d0a", wraplength=900).pack(pady=10)

        options = [("A", q[3]), ("B", q[4]), ("C", q[5]), ("D", q[6])]
        for kode, teks in options:
            ctk.CTkButton(
                self.gradient, text=f"{kode}. {teks}", font=("Arial", 16, "bold"),
                command=lambda o=kode: self.select_answer(o, q),
                fg_color="#e6d8a3", hover_color="#d4c68e", text_color="#7f6a2a", corner_radius=15, height=45
            ).pack(pady=6)

        ctk.CTkButton(self.gradient, text="Kembali", command=self.go_back,
                      fg_color="#888888", text_color="white", font=("Arial", 14, "bold")).pack(pady=30)

    def select_answer(self, answer, question):
        if question[0] in self.selected_answers:
            return

        self.selected_answers[question[0]] = answer
        correct = question[7]
        explanation = question[8]

        if answer == correct:
            self.score += 1
            result_text = f"✅ Benar! Jawaban: {correct}"
            color = "#2e8b57"
        else:
            result_text = f"❌ Salah. Jawaban yang benar adalah {correct}.\nPenjelasan: {explanation}"
            color = "#c0392b"

        for widget in self.gradient.winfo_children():
            widget.configure(state="disabled")

        ctk.CTkLabel(
            self.gradient, text=result_text,
            font=("Arial", 16, "bold"), text_color=color,
            wraplength=900, justify="center"
        ).pack(pady=(20, 30))

        next_text = "Selesai" if self.current_index + 1 == len(self.questions) else "Lanjut"
        ctk.CTkButton(
            self.gradient, text=next_text, command=self.next_question,
            fg_color="#e67c4a", hover_color="#d35400", text_color="#5a1d0a",
            font=("Arial", 16, "bold"), corner_radius=15
        ).pack()

    def next_question(self):
        self.current_index += 1
        if self.current_index < len(self.questions):
            self.show_question(self.current_index)
        else:
            self.finish_quiz()

    def finish_quiz(self):
        for widget in self.gradient.winfo_children():
            widget.destroy()

        total = len(self.questions)
        nilai = int((self.score / total) * 100) if total > 0 else 0

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO reports (user_id, score) VALUES (?, ?)", (self.user_id, nilai))
        conn.commit()
        conn.close()

        ctk.CTkLabel(self.gradient, text=f"Skor Anda: {nilai}", font=("Arial", 28, "bold"), text_color="#5a1d0a").pack(pady=40)
        ctk.CTkLabel(self.gradient, text="Terima kasih sudah mengerjakan!", font=("Arial", 20), text_color="#5a1d0a").pack(pady=10)
        ctk.CTkButton(self.gradient, text="Kembali", command=self.go_back,
                      fg_color="#e67c4a", hover_color="#d35400", text_color="white",
                      font=("Arial", 16, "bold"), corner_radius=15).pack(pady=20)

    def show_info(self, message, error=False):
        for widget in self.gradient.winfo_children():
            widget.destroy()
        color = "#ff0000" if error else "#5a1d0a"
        ctk.CTkLabel(self.gradient, text=message, font=("Arial", 18, "bold"), text_color=color).pack(pady=20)
        ctk.CTkButton(self.gradient, text="Kembali", command=self.go_back,
                      fg_color="#888888", text_color="white", font=("Arial", 14, "bold")).pack(pady=10)

    def go_back(self):
        self.destroy()
        if self.previous_screen:
            self.previous_screen.deiconify()
