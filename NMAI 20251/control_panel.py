import tkinter as tk
from tkinter import ttk

class ControlPanel:
    def __init__(self, parent, callbacks):
        self.callbacks = callbacks
        self.frame = tk.Frame(parent, bg='#f0f0f0', padx=10, pady=10)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tạo các widget điều khiển"""
        # Nhập N
        tk.Label(self.frame, text="Kích thước N:", bg='#f0f0f0', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.n_var = tk.StringVar(value="4")
        self.n_spinbox = tk.Spinbox(self.frame, from_=4, to=8, textvariable=self.n_var, 
                                    width=5, font=('Arial', 10))
        self.n_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Nút bắt đầu
        self.start_btn = tk.Button(self.frame, text="🚀 Bắt đầu giải", 
                                   command=self.callbacks['start'],
                                   bg='#4CAF50', fg='white',
                                   font=('Arial', 10, 'bold'), padx=10)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(self.frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Các nút điều khiển
        self.reset_btn = self._create_button("🔄 Reset", self.callbacks['reset'], 
                                            '#757575', 'disabled')
        self.prev_btn = self._create_button("◀ Trước", self.callbacks['prev'], 
                                           '#2196F3', 'disabled')
        self.play_btn = self._create_button("▶ Phát", self.callbacks['play'], 
                                           '#FF9800', 'disabled')
        self.next_btn = self._create_button("Sau ▶", self.callbacks['next'], 
                                           '#2196F3', 'disabled')
        
        ttk.Separator(self.frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Thanh tốc độ
        tk.Label(self.frame, text="Tốc độ:", bg='#f0f0f0', 
                font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        self.speed_var = tk.IntVar(value=500)
        self.speed_slider = tk.Scale(self.frame, from_=100, to=2000, orient=tk.HORIZONTAL,
                                    variable=self.speed_var, length=150,
                                    command=self.callbacks['speed'])
        self.speed_slider.pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.frame, text="ms", bg='#f0f0f0', 
                font=('Arial', 10)).pack(side=tk.LEFT)
    
    def _create_button(self, text, command, color, state='normal'):
        """Tạo button với style"""
        btn = tk.Button(self.frame, text=text, command=command,
                       bg=color, fg='white', font=('Arial', 10, 'bold'), 
                       state=state)
        btn.pack(side=tk.LEFT, padx=5)
        return btn
    
    def get_n(self):
        """Lấy giá trị N"""
        return int(self.n_var.get())
    
    def get_speed(self):
        """Lấy tốc độ"""
        return self.speed_var.get()