class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.steps = []
        self.solutions = []
        
    def solve_with_steps(self):
        """Giải bài toán N-Queens và ghi lại từng bước"""
        self.steps = []
        self.solutions = []
        
        visited_col = [False] * self.n
        visited_dig_pri = [False] * (2 * self.n - 1)
        visited_dig_sec = [False] * (2 * self.n - 1)
        
        self._backtrack(0, visited_col, visited_dig_pri, visited_dig_sec, [])
        
        return self.steps, self.solutions
    
    def _backtrack(self, cur_row, visited_col, visited_dig_pri, visited_dig_sec, pos):
        """Thuật toán backtracking đệ quy"""
        if cur_row == self.n:
            self.solutions.append(pos.copy())
            self.steps.append({
                'type': 'solution',
                'board': pos.copy(),
                'row': cur_row,
                'col': -1,
                'message': f'🎉 Tìm thấy nghiệm {len(self.solutions)}: [{", ".join(map(str, [p+1 for p in pos]))}]'
            })
            return
        
        for col_id in range(self.n):
            dig_pri_id = cur_row - col_id + self.n - 1
            dig_sec_id = cur_row + col_id
            
            # Thử đặt
            self.steps.append({
                'type': 'try',
                'board': pos.copy(),
                'row': cur_row,
                'col': col_id,
                'message': f'🔍 Thử đặt hậu tại hàng {cur_row+1}, cột {col_id+1}'
            })
            
            if not visited_col[col_id] and not visited_dig_pri[dig_pri_id] and not visited_dig_sec[dig_sec_id]:
                # Đặt quân hậu
                visited_col[col_id] = visited_dig_pri[dig_pri_id] = visited_dig_sec[dig_sec_id] = True
                pos.append(col_id)
                
                self.steps.append({
                    'type': 'place',
                    'board': pos.copy(),
                    'row': cur_row,
                    'col': col_id,
                    'message': f'✓ Đặt hậu thành công tại ({cur_row+1}, {col_id+1})'
                })
                
                # Đệ quy
                self._backtrack(cur_row + 1, visited_col, visited_dig_pri, visited_dig_sec, pos)
                
                # Backtrack
                pos.pop()
                visited_col[col_id] = visited_dig_pri[dig_pri_id] = visited_dig_sec[dig_sec_id] = False
                
                self.steps.append({
                    'type': 'backtrack',
                    'board': pos.copy(),
                    'row': cur_row,
                    'col': col_id,
                    'message': f'← Backtrack: Gỡ hậu tại ({cur_row+1}, {col_id+1})'
                })
            else:
                # Vị trí không hợp lệ
                self.steps.append({
                    'type': 'invalid',
                    'board': pos.copy(),
                    'row': cur_row,
                    'col': col_id,
                    'message': f'✗ Không thể đặt tại ({cur_row+1}, {col_id+1}) - Bị tấn công'
                })