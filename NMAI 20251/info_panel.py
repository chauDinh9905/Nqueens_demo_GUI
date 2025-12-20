import tkinter as tk

class InfoPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._create_widgets()
    
    def _create_widgets(self):
        tk.Label(self.frame, text="Thông tin giải thuật", font=('Arial', 12, 'bold'), bg='white').pack(pady=5)
        self.step_label = tk.Label(self.frame, text="Bước: 0 / 0", bg='white', font=('Arial', 10))
        self.step_label.pack()
        
        self.message_text = tk.Text(self.frame, height=3, width=32, font=('Arial', 9), bg='#e3f2fd', state='disabled')
        self.message_text.pack(padx=10, pady=5)
        
        # Hiển thị thời gian
        self.time_label = tk.Label(self.frame, text="Tổng thời gian: 0.00 ms", font=('Arial', 10), bg='white')
        self.time_label.pack(pady=2)
        
        self.first_time_label = tk.Label(self.frame, text="Lời giải đầu: 0.00 ms", font=('Arial', 10, 'bold'), fg='#4CAF50', bg='white')
        self.first_time_label.pack(pady=2)
        
        tk.Label(self.frame, text="Danh sách nghiệm:", font=('Arial', 10, 'bold'), bg='white').pack(pady=(10, 0))
        self.solutions_text = tk.Text(self.frame, height=12, width=32, bg='#f5f5f5', font=('Courier', 9))
        self.solutions_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def update_times(self, total_ms, first_ms):
        self.time_label.config(text=f"Tổng thời gian: {total_ms:.4f} ms")
        self.first_time_label.config(text=f"Lời giải đầu: {first_ms:.4f} ms")

    def set_message(self, text):
        self.message_text.config(state='normal')
        self.message_text.delete('1.0', tk.END)
        self.message_text.insert('1.0', text)
        self.message_text.config(state='disabled')

    def update_step(self, current, total):
        self.step_label.config(text=f"Bước: {current} / {total}")

    def update_solutions_list(self, solutions):
        self.solutions_text.delete('1.0', tk.END)
        for i, s in enumerate(solutions, 1):
            self.solutions_text.insert(tk.END, f"{i}. {[x+1 for x in s]}\n")

    def reset(self):
        self.update_times(0, 0)
        self.set_message("Nhấn bắt đầu để chạy...")
        self.update_step(0, 0)
        self.solutions_text.delete('1.0', tk.END)