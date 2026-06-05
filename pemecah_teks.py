import tkinter as tk
from tkinter import scrolledtext, messagebox
import re
from datetime import datetime

class TextSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Splitter PRO - Max 6000 Karakter")
        self.root.geometry("900x800")
        self.root.minsize(800, 600)

        self.chunks = []

        # --- UI Components ---
        
        # 1. Input Section
        tk.Label(root, text="Masukkan Teks Panjang (Maks 200rb+ karakter):", font=('Arial', 10, 'bold')).pack(pady=5)
        self.text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=12)
        self.text_input.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Binding event untuk update counter secara real-time
        self.text_input.bind("<KeyRelease>", self.update_counters)

        # Tambahan Fitur 1: Info Jumlah Kata & Karakter
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(padx=10, fill=tk.X)
        
        self.lbl_char_count = tk.Label(self.info_frame, text="Karakter: 0", font=('Arial', 9, 'bold'), fg="#555")
        self.lbl_char_count.pack(side=tk.LEFT, padx=5)
        
        self.lbl_word_count = tk.Label(self.info_frame, text="Kata: 0", font=('Arial', 9, 'bold'), fg="#555")
        self.lbl_word_count.pack(side=tk.LEFT, padx=15)

        # 2. Control Section
        self.btn_proses = tk.Button(root, text="PROSES & PECAH TEKS", command=self.split_text, 
                                   bg="#2196F3", fg="white", font=('Arial', 10, 'bold'), pady=8)
        self.btn_proses.pack(pady=10)

        # 3. Output Buttons Section (Pecahan)
        tk.Label(root, text="Hasil Pecahan (Klik untuk Copy):", font=('Arial', 9, 'italic')).pack()
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(padx=10, pady=5, fill=tk.X)

        # 4. Console Log Section (Textbox Output)
        tk.Label(root, text="Console Log:", font=('Arial', 9, 'bold')).pack(anchor="w", padx=10)
        self.log_console = tk.Text(root, height=8, bg="#1e1e1e", fg="#00ff00", font=('Consolas', 9))
        self.log_console.pack(padx=10, pady=5, fill=tk.X)
        self.log_console.config(state=tk.DISABLED)

        self.log("Aplikasi siap digunakan.")

    def update_counters(self, event=None):
        """Menghitung jumlah karakter dan kata secara real-time"""
        # Mengambil teks (mengabaikan newline otomatis di akhir teks Tkinter)
        text = self.text_input.get("1.0", tk.END).strip()
        
        char_count = len(text)
        # Menghitung kata berdasarkan spasi/whitespace
        word_count = len(text.split()) if text else 0
        
        # Update ke label UI
        self.lbl_char_count.config(text=f"Karakter: {char_count:,}".replace(",", "."))
        self.lbl_word_count.config(text=f"Kata: {word_count:,}".replace(",", "."))

    def log(self, message):
        """Fungsi untuk mencetak log ke console textbox"""
        self.log_console.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_console.see(tk.END)
        self.log_console.config(state=tk.DISABLED)

    def split_text(self):
        input_data = self.text_input.get("1.0", tk.END).strip()
        
        if not input_data:
            self.log("ERROR: Input kosong, proses dibatalkan.")
            messagebox.showwarning("Peringatan", "Teks kosong!")
            return

        # Kosongkan tombol sebelumnya
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        self.chunks = []

        # Algoritma Pemecah Kalimat
        sentences = re.split(r'(?<=[.!?])\s+', input_data)
        
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= 6000:
                current_chunk += sentence + " "
            else:
                self.chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            self.chunks.append(current_chunk.strip())

        self.log(f"BERHASIL: Teks dipecah menjadi {len(self.chunks)} bagian.")
        self.create_buttons()

    def create_buttons(self):
        for i, content in enumerate(self.chunks):
            btn = tk.Button(
                self.button_frame, 
                text=f"Bagian {i+1}", 
                width=12,
                command=lambda c=content, b=i: self.copy_to_clipboard(c, b)
            )
            btn.grid(row=i // 7, column=i % 7, padx=5, pady=5)

    def copy_to_clipboard(self, text, index):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        
        # Update warna tombol
        target_button = self.button_frame.winfo_children()[index]
        target_button.configure(bg="#455a64", fg="white") 
        
        # Tambahan Fitur 2: Ambil potongan awal kalimat (misal 40 karakter pertama) + bumbu "..."
        snippet = text[:40].replace('\n', ' ') + "..." if len(text) > 40 else text
        
        self.log(f"COPY: Bagian {index+1} ({len(text)} karakter) disalin. Teks: \"{snippet}\"")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextSplitterApp(root)
    root.mainloop()