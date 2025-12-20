import tkinter as tk

class BoardCanvas:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg='white', width=500, height=500)
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)
        
    def draw_board(self, n, step):
        self.canvas.delete('all')
        size = 450 // n
        offset = 25
        
        for i in range(n):
            for j in range(n):
                x1, y1 = offset + j*size, offset + i*size
                color = '#F5DEB3' if (i+j)%2==0 else '#D2691E'
                
                if step and i == step['row'] and j == step['col']:
                    color = '#87CEEB' if step['type'] == 'try' else '#FFB6C1'
                if step and i < len(step['board']) and step['board'][i] == j:
                    color = '#90EE90'
                
                self.canvas.create_rectangle(x1, y1, x1+size, y1+size, fill=color, outline='black')
                
                if step and i < len(step['board']) and step['board'][i] == j:
                    self.canvas.create_text(x1+size/2, y1+size/2, text='♛', font=('Arial', size//2))
                elif step and i == step['row'] and j == step['col']:
                    char = '?' if step['type'] == 'try' else '✗'
                    self.canvas.create_text(x1+size/2, y1+size/2, text=char, font=('Arial', size//2))

    def clear(self): self.canvas.delete('all')