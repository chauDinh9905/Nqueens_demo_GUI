import tkinter as tk
from n_queens_solver import NQueensSolver
from board_canvas import BoardCanvas
from control_panel import ControlPanel
from info_panel import InfoPanel

class NQueensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Visualizer")
        self.root.geometry("1100x700")
        
        self.n = 4
        self.steps = []
        self.current_step = 0
        self.is_playing = False
        
        callbacks = {
            'start': self.start_solve,
            'reset': self.reset,
            'prev': self.prev_step,
            'play': self.toggle_play,
            'next': self.next_step,
            'speed': lambda v: None
        }
        
        self.control_panel = ControlPanel(self.root, callbacks)
        
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)
        
        self.board_canvas = BoardCanvas(container)
        self.info_panel = InfoPanel(container)

    def start_solve(self):
        self.n = self.control_panel.get_n()
        algo = self.control_panel.get_option()
        
        solver = NQueensSolver(self.n)
        # Nhận thêm biến is_timeout từ solver
        self.steps, solutions, exec_time, first_time, is_timeout = solver.solve_with_steps(algo)
        
        self.current_step = 0
        self.info_panel.update_solutions_list(solutions)
        self.info_panel.update_times(exec_time, first_time)
        
        if is_timeout:
            self.info_panel.set_message("⚠️ Tốn quá nhiều thời gian! Đã dừng tìm kiếm.")
        
        self._update_display()
        self._set_btn_state('normal')

    def _update_display(self):
        if not self.steps: return
        step = self.steps[self.current_step]
        self.board_canvas.draw_board(self.n, step)
        self.info_panel.update_step(self.current_step + 1, len(self.steps))
        self.info_panel.set_message(step['message'])

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self._update_display()
        else:
            self.is_playing = False

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_display()

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self._play_animation()

    def _play_animation(self):
        if self.is_playing and self.current_step < len(self.steps) - 1:
            self.next_step()
            self.root.after(self.control_panel.get_speed(), self._play_animation)
        else:
            self.is_playing = False

    def reset(self):
        self.is_playing = False
        self.steps = []
        self.current_step = 0
        self.board_canvas.clear()
        self.info_panel.reset()
        self._set_btn_state('disabled')

    def _set_btn_state(self, state):
        btns = [self.control_panel.reset_btn, self.control_panel.prev_btn, 
                self.control_panel.play_btn, self.control_panel.next_btn]
        for b in btns: b.config(state=state)

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensApp(root)
    root.mainloop()