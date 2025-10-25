import tkinter as tk
from tkinter import messagebox

#Import n_queens_solver
from n_queens_solver import NQueensSolver
from board_canvas import BoardCanvas
from control_panel import ControlPanel
from info_panel import InfoPanel

class NQueensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Visualizer")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # State
        self.n = 4
        self.steps = []
        self.solutions = []
        self.current_step = 0
        self.is_playing = False
        
        # Tạo GUI
        self._setup_ui()
    
    def _setup_ui(self):
        """Khởi tạo giao diện"""
        # Control panel
        callbacks = {
            'start': self.start_solve,
            'reset': self.reset,
            'prev': self.prev_step,
            'play': self.toggle_play,
            'next': self.next_step,
            'speed': lambda v: setattr(self, 'speed', int(v))
        }
        self.control_panel = ControlPanel(self.root, callbacks)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Board frame
        board_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        board_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(board_frame, text="Bàn cờ N-Queens", 
                font=('Arial', 14, 'bold'), bg='white', pady=5).pack()
        
        self.board_canvas = BoardCanvas(board_frame)
        
        # Legend
        self._create_legend(board_frame)
        
        # Info panel
        self.info_panel = InfoPanel(main_frame)
    
    def _create_legend(self, parent):
        """Tạo chú thích"""
        legend_frame = tk.Frame(parent, bg='white')
        legend_frame.pack(pady=5)
        
        legends = [
            ("♛ Quân hậu đã đặt", '#90EE90'),
            ("? Đang thử", '#87CEEB'),
            ("✗ Không hợp lệ", '#FFB6C1')
        ]
        
        for text, color in legends:
            frame = tk.Frame(legend_frame, bg='white')
            frame.pack(side=tk.LEFT, padx=10)
            tk.Canvas(frame, width=20, height=20, bg=color, 
                     highlightthickness=1, highlightbackground='black').pack(side=tk.LEFT, padx=2)
            tk.Label(frame, text=text, bg='white', font=('Arial', 9)).pack(side=tk.LEFT)
    
    def start_solve(self):
        """Bắt đầu giải"""
        try:
            self.n = self.control_panel.get_n()
            if self.n < 4 or self.n > 8:
                messagebox.showerror("Lỗi", "N phải từ 4 đến 8")
                return
        except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ")
            return
        
        # Giải bài toán
        solver = NQueensSolver(self.n)
        self.steps, self.solutions = solver.solve_with_steps()
        self.current_step = 0
        self.is_playing = False
        
        # Cập nhật UI
        self._enable_controls()
        self._update_display()
        self.info_panel.update_solutions_list(self.solutions)
    
    def reset(self):
        """Reset toàn bộ"""
        self.is_playing = False
        self.steps = []
        self.solutions = []
        self.current_step = 0
        
        self._disable_controls()
        self.board_canvas.clear()
        self.info_panel.reset(self.n)
    
    def prev_step(self):
        """Bước trước"""
        if self.current_step > 0:
            self.current_step -= 1
            self._update_display()
    
    def next_step(self):
        """Bước sau"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._update_display()
    
    def toggle_play(self):
        """Chuyển đổi play/pause"""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.control_panel.play_btn.config(text="⏸ Dừng")
            self._play_animation()
        else:
            self.control_panel.play_btn.config(text="▶ Phát")
    
    def _play_animation(self):
        """Phát animation"""
        if self.is_playing and self.current_step < len(self.steps) - 1:
            self.next_step()
            speed = self.control_panel.get_speed()
            self.root.after(speed, self._play_animation)
        else:
            self.is_playing = False
            self.control_panel.play_btn.config(text="▶ Phát")
    
    def _update_display(self):
        """Cập nhật hiển thị"""
        if not self.steps:
            return
        
        step = self.steps[self.current_step]
        
        # Cập nhật bàn cờ
        self.board_canvas.draw_board(self.n, step)
        
        # Cập nhật thông tin
        self.info_panel.update_step(self.current_step + 1, len(self.steps))
        self.info_panel.set_message(step['message'])
        self.info_panel.update_status(step['type'])
        self.info_panel.update_queens(len(step['board']), self.n)
        self.info_panel.update_solutions_count(len(self.solutions))
    
    def _enable_controls(self):
        """Bật các nút điều khiển"""
        self.control_panel.start_btn.config(state='disabled')
        self.control_panel.reset_btn.config(state='normal')
        self.control_panel.prev_btn.config(state='normal')
        self.control_panel.play_btn.config(state='normal', text="▶ Phát")
        self.control_panel.next_btn.config(state='normal')
    
    def _disable_controls(self):
        """Tắt các nút điều khiển"""
        self.control_panel.start_btn.config(state='normal')
        self.control_panel.reset_btn.config(state='disabled')
        self.control_panel.prev_btn.config(state='disabled')
        self.control_panel.play_btn.config(state='disabled')
        self.control_panel.next_btn.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensApp(root)
    root.mainloop()