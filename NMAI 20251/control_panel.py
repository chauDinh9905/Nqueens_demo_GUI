import tkinter as tk
from tkinter import ttk

class ControlPanel:
    def __init__(self, parent, callbacks):
        self.callbacks = callbacks
        self.frame = tk.Frame(parent, bg='#f0f0f0', padx=10, pady=10)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        self._create_widgets()
    
    def _create_widgets(self):
        # Nhập N
        tk.Label(self.frame, text="N:", bg='#f0f0f0', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.n_var = tk.StringVar(value="4")
        tk.Spinbox(self.frame, from_=4, to=12, textvariable=self.n_var, width=3).pack(side=tk.LEFT, padx=5)
        
        # Chọn Thuật toán
        tk.Label(self.frame, text="Thuật toán:", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        self.option_var = tk.StringVar(value="Đệ quy")
        self.option_menu = tk.OptionMenu(self.frame, self.option_var, "Đệ quy", "Forward Checking", "Forward Checking + LCV")
        self.option_menu.pack(side=tk.LEFT, padx=5)

        # Nút bấm
        self.start_btn = self._create_button("🚀 Bắt đầu", self.callbacks['start'], '#4CAF50')
        self.reset_btn = self._create_button("🔄 Reset", self.callbacks['reset'], '#757575', 'disabled')
        self.prev_btn = self._create_button("◀", self.callbacks['prev'], '#2196F3', 'disabled')
        self.play_btn = self._create_button("▶ Phát", self.callbacks['play'], '#FF9800', 'disabled')
        self.next_btn = self._create_button("▶", self.callbacks['next'], '#2196F3', 'disabled')
        
        # Tốc độ
        tk.Label(self.frame, text="Tốc độ:", bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.IntVar(value=500)
        tk.Scale(self.frame, from_=50, to=1500, orient=tk.HORIZONTAL, variable=self.speed_var, length=100).pack(side=tk.LEFT)

    def _create_button(self, text, command, color, state='normal'):
        btn = tk.Button(self.frame, text=text, command=command, bg=color, fg='white', font=('Arial', 9, 'bold'), state=state)
        btn.pack(side=tk.LEFT, padx=2)
        return btn
    
    def get_n(self): return int(self.n_var.get())
    def get_speed(self): return self.speed_var.get()
    def get_option(self): return self.option_var.get()