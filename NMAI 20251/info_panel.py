import tkinter as tk

class InfoPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._create_widgets()
    
    def _create_widgets(self):
        tk.Label(self.frame, text="Thông tin", font=('Arial', 12, 'bold'), bg='white').pack(pady=5)
        self.step_label = tk.Label(self.frame, text="Bước: 0 / 0", bg='white')
        self.step_label.pack()
        
        self.message_text = tk.Text(self.frame, height=3, width=30, font=('Arial', 9), bg='#e3f2fd')
        self.message_text.pack(padx=10, pady=5)
        
        self.time_label = tk.Label(self.frame, text="Thời gian giải: 0.00 ms", font=('Arial', 10, 'italic'), fg='#1976D2', bg='white')
        self.time_label.pack(pady=5)
        
        self.solutions_text = tk.Text(self.frame, height=10, width=30, bg='#f5f5f5')
        self.solutions_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    def update_time(self, ms): self.time_label.config(text=f"Thời gian giải: {ms:.4f} ms")
    def set_message(self, text):
        self.message_text.config(state='normal')
        self.message_text.delete('1.0', tk.END); self.message_text.insert('1.0', text)
        self.message_text.config(state='disabled')
    def update_step(self, current, total): self.step_label.config(text=f"Bước: {current} / {total}")
    def update_solutions_list(self, solutions):
        self.solutions_text.delete('1.0', tk.END)
        for i, s in enumerate(solutions, 1): self.solutions_text.insert(tk.END, f"{i}. { [x+1 for x in s] }\n")
    def reset(self):
        self.update_time(0); self.set_message("Sẵn sàng"); self.update_step(0, 0)
        self.solutions_text.delete('1.0', tk.END)