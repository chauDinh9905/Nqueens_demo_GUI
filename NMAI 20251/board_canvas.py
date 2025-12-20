import tkinter as tk

class BoardCanvas:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg='white', width=450, height=450)
        self.canvas.pack(padx=10, pady=10)
        
    def draw_board(self, n, step):
        self.canvas.delete('all')
        cell_size = 400 // n
        offset = 25
        
        for i in range(n):
            for j in range(n):
                x1, y1 = offset + j*cell_size, offset + i*cell_size
                color = '#F5DEB3' if (i+j)%2==0 else '#D2691E'
                
                # Highlight ô đang tương tác
                if step and i == step['row'] and j == step['col']:
                    if step['type'] == 'try': color = '#87CEEB'
                    elif step['type'] == 'invalid': color = '#FFB6C1'
                
                # Nếu có hậu đã chốt
                if step and i < len(step['board']) and step['board'][i] == j:
                    color = '#90EE90'
                
                self.canvas.create_rectangle(x1, y1, x1+cell_size, y1+cell_size, fill=color)
                
                # Vẽ biểu tượng
                if step and i < len(step['board']) and step['board'][i] == j:
                    self.canvas.create_text(x1+cell_size/2, y1+cell_size/2, text='♛', font=('Arial', cell_size//2))
                elif step and i == step['row'] and j == step['col']:
                    char = '?' if step['type'] == 'try' else '✗'
                    self.canvas.create_text(x1+cell_size/2, y1+cell_size/2, text=char, font=('Arial', cell_size//2))

    def clear(self): self.canvas.delete('all')