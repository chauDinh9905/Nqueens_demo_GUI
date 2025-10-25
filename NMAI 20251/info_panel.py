import tkinter as tk

class InfoPanel:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Tạo các widget hiển thị thông tin"""
        tk.Label(self.frame, text="Thông tin thuật toán", 
                font=('Arial', 14, 'bold'), bg='white', pady=5).pack()
        
        # Nhãn bước
        self.step_label = tk.Label(self.frame, text="Bước: 0 / 0", 
                                   font=('Arial', 11, 'bold'), bg='white', pady=5)
        self.step_label.pack()
        
        # Message box
        msg_frame = tk.Frame(self.frame, bg='#e3f2fd', relief=tk.GROOVE, bd=2)
        msg_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.message_text = tk.Text(msg_frame, height=3, wrap=tk.WORD, 
                                   font=('Arial', 10), bg='#e3f2fd', relief=tk.FLAT)
        self.message_text.pack(padx=5, pady=5)
        self.set_message('Nhấn "Bắt đầu giải" để xem thuật toán hoạt động')
        
        # Chi tiết
        details_frame = tk.LabelFrame(self.frame, text="Chi tiết", 
                                     font=('Arial', 11, 'bold'),
                                     bg='white', padx=10, pady=10)
        details_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.status_label = tk.Label(details_frame, text="Trạng thái: Chờ", 
                                     font=('Arial', 10), bg='white', anchor='w')
        self.status_label.pack(fill=tk.X, pady=2)
        
        self.queens_label = tk.Label(details_frame, text="Số hậu đã đặt: 0 / 4", 
                                    font=('Arial', 10), bg='white', anchor='w')
        self.queens_label.pack(fill=tk.X, pady=2)
        
        self.solutions_label = tk.Label(details_frame, text="Nghiệm tìm được: 0", 
                                       font=('Arial', 10), bg='white', anchor='w')
        self.solutions_label.pack(fill=tk.X, pady=2)
        
        # Danh sách nghiệm
        solutions_frame = tk.LabelFrame(self.frame, text="Các nghiệm tìm được", 
                                       font=('Arial', 11, 'bold'), 
                                       bg='white', padx=10, pady=10)
        solutions_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.solutions_text = tk.Text(solutions_frame, height=10, wrap=tk.WORD,
                                     font=('Courier', 9), bg='#f5f5f5')
        solutions_scroll = tk.Scrollbar(solutions_frame, 
                                       command=self.solutions_text.yview)
        self.solutions_text.config(yscrollcommand=solutions_scroll.set)
        
        self.solutions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        solutions_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def set_message(self, text):
        """Cập nhật thông báo"""
        self.message_text.config(state='normal')
        self.message_text.delete('1.0', tk.END)
        self.message_text.insert('1.0', text)
        self.message_text.config(state='disabled')
    
    def update_step(self, current, total):
        """Cập nhật bước hiện tại"""
        self.step_label.config(text=f"Bước: {current} / {total}")
    
    def update_status(self, step_type):
        """Cập nhật trạng thái"""
        status_map = {
            'solution': '🎉 Tìm thấy nghiệm!',
            'place': '✓ Đặt hậu',
            'try': '🔍 Đang thử',
            'backtrack': '← Quay lui',
            'invalid': '✗ Không hợp lệ'
        }
        self.status_label.config(text=f"Trạng thái: {status_map.get(step_type, 'Chờ')}")
    
    def update_queens(self, placed, total):
        """Cập nhật số quân hậu"""
        self.queens_label.config(text=f"Số hậu đã đặt: {placed} / {total}")
    
    def update_solutions_count(self, count):
        """Cập nhật số nghiệm"""
        self.solutions_label.config(text=f"Nghiệm tìm được: {count}")
    
    def update_solutions_list(self, solutions):
        """Cập nhật danh sách nghiệm"""
        self.solutions_text.delete('1.0', tk.END)
        for idx, sol in enumerate(solutions, 1):
            self.solutions_text.insert(tk.END, 
                f"{idx}. [{', '.join(map(str, [s+1 for s in sol]))}]\n")
    
    def reset(self, n=4):
        """Reset thông tin"""
        self.set_message('Nhấn "Bắt đầu giải" để xem thuật toán hoạt động')
        self.update_step(0, 0)
        self.status_label.config(text="Trạng thái: Chờ")
        self.update_queens(0, n)
        self.update_solutions_count(0)
        self.solutions_text.delete('1.0', tk.END)