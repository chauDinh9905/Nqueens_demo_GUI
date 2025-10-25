import tkinter as tk

class BoardCanvas:
    def __init__(self, parent, width=500, height=500):
        self.canvas = tk.Canvas(parent, bg='white', width=width, height=height)
        self.canvas.pack(padx=10, pady=10)
        self.width = width
        self.height = height
        
    def draw_board(self, n, step):
        """Vẽ bàn cờ với trạng thái hiện tại"""
        self.canvas.delete('all')
        
        if not step:
            return
        
        # Tạo ma trận bàn cờ
        board = [[None for _ in range(n)] for _ in range(n)]
        
        # Đặt các quân hậu
        for row, col in enumerate(step['board']):
            board[row][col] = 'queen'
        
        # Đánh dấu ô đang thử
        if step['type'] in ['try', 'invalid'] and step['row'] < n and step['col'] >= 0:
            board[step['row']][step['col']] = step['type']
        
        # Tính kích thước ô
        cell_size = min(60, 450 // n)
        board_size = n * cell_size
        offset_x = (self.width - board_size) // 2
        offset_y = (self.height - board_size) // 2
        
        # Vẽ từng ô
        for i in range(n):
            for j in range(n):
                x1 = offset_x + j * cell_size
                y1 = offset_y + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                # Chọn màu
                is_light = (i + j) % 2 == 0
                color = self._get_cell_color(board[i][j], is_light)
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                            outline='black', width=2)
                
                # Vẽ ký hiệu
                self._draw_symbol(board[i][j], (x1 + x2) / 2, (y1 + y2) / 2, cell_size)
    
    def _get_cell_color(self, cell_type, is_light):
        """Lấy màu cho ô cờ"""
        if cell_type == 'queen':
            return '#90EE90' if is_light else '#228B22'
        elif cell_type == 'try':
            return '#87CEEB' if is_light else '#4682B4'
        elif cell_type == 'invalid':
            return '#FFB6C1' if is_light else '#DC143C'
        else:
            return '#F5DEB3' if is_light else '#D2691E'
    
    def _draw_symbol(self, cell_type, cx, cy, cell_size):
        """Vẽ ký hiệu trên ô cờ"""
        font_size = max(12, cell_size // 2)
        
        if cell_type == 'queen':
            self.canvas.create_text(cx, cy, text='♛', 
                                  font=('Arial', font_size, 'bold'))
        elif cell_type == 'try':
            self.canvas.create_text(cx, cy, text='?', 
                                  font=('Arial', font_size, 'bold'))
        elif cell_type == 'invalid':
            self.canvas.create_text(cx, cy, text='✗', 
                                  font=('Arial', font_size, 'bold'))
    
    def clear(self):
        """Xóa bàn cờ"""
        self.canvas.delete('all')