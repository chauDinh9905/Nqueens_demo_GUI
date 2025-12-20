import time

class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.steps = []
        self.solutions = []
        
    def solve_with_steps(self, algo_type="Đệ quy"):
        """Giải bài toán và đo thời gian thực hiện"""
        start_time = time.perf_counter()
        self.steps = []
        self.solutions = []
        
        visited_col = [False] * self.n
        visited_dig_pri = [False] * (2 * self.n - 1)
        visited_dig_sec = [False] * (2 * self.n - 1)
        
        if algo_type == "Đệ quy":
            self._backtrack(0, visited_col, visited_dig_pri, visited_dig_sec, [])
        else:
            self._solve_advanced(0, visited_col, visited_dig_pri, visited_dig_sec, [], algo_type)
            
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000 # Chuyển sang ms
        
        return self.steps, self.solutions, execution_time

    def _backtrack(self, cur_row, visited_col, visited_dig_pri, visited_dig_sec, pos):
        if cur_row == self.n:
            self.solutions.append(pos.copy())
            self.steps.append({
                'type': 'solution', 'board': pos.copy(), 'row': cur_row, 'col': -1,
                'message': f'🎉 Tìm thấy nghiệm {len(self.solutions)}'
            })
            return

        for col_id in range(self.n):
            dig_pri_id = cur_row - col_id + self.n - 1
            dig_sec_id = cur_row + col_id
            
            self.steps.append({
                'type': 'try', 'board': pos.copy(), 'row': cur_row, 'col': col_id,
                'message': f'🔍 Thử đặt hậu tại ({cur_row+1}, {col_id+1})'
            })
            
            if not visited_col[col_id] and not visited_dig_pri[dig_pri_id] and not visited_dig_sec[dig_sec_id]:
                visited_col[col_id] = visited_dig_pri[dig_pri_id] = visited_dig_sec[dig_sec_id] = True
                pos.append(col_id)
                self.steps.append({
                    'type': 'place', 'board': pos.copy(), 'row': cur_row, 'col': col_id,
                    'message': f'✓ Đặt thành công tại ({cur_row+1}, {col_id+1})'
                })
                
                self._backtrack(cur_row + 1, visited_col, visited_dig_pri, visited_dig_sec, pos)
                
                pos.pop()
                visited_col[col_id] = visited_dig_pri[dig_pri_id] = visited_dig_sec[dig_sec_id] = False
                self.steps.append({
                    'type': 'backtrack', 'board': pos.copy(), 'row': cur_row, 'col': col_id,
                    'message': f'← Quay lui khỏi ({cur_row+1}, {col_id+1})'
                })
            else:
                self.steps.append({
                    'type': 'invalid', 'board': pos.copy(), 'row': cur_row, 'col': col_id,
                    'message': f'✗ Vị trí ({cur_row+1}, {col_id+1}) bị tấn công'
                })

    def _solve_advanced(self, cur_row, v_col, v_pri, v_sec, pos, algo_type):
        if cur_row == self.n:
            self.solutions.append(pos.copy())
            self.steps.append({'type': 'solution', 'board': pos.copy(), 'row': cur_row, 'col': -1, 'message': '🎉 Tìm thấy nghiệm!'})
            return

        # Lấy danh sách các cột khả thi (Domain)
        candidates = []
        for col_id in range(self.n):
            p_id, s_id = cur_row - col_id + self.n - 1, cur_row + col_id
            if not v_col[col_id] and not v_pri[p_id] and not v_sec[s_id]:
                candidates.append(col_id)

        # LCV (Least Constraining Value)
        if "LCV" in algo_type:
            candidates.sort(key=lambda c: self._count_conflicts(cur_row, c, v_col, v_pri, v_sec))

        for col_id in candidates:
            p_id, s_id = cur_row - col_id + self.n - 1, cur_row + col_id
            
            # Forward Checking
            if "Forward Checking" in algo_type:
                if self._has_empty_domain(cur_row + 1, col_id, v_col, v_pri, v_sec):
                    self.steps.append({
                        'type': 'invalid', 'board': pos.copy(), 'row': cur_row, 'col': col_id,
                        'message': f'⚠️ FC: Đặt ({cur_row+1}, {col_id+1}) khiến hàng sau vô nghiệm'
                    })
                    continue

            v_col[col_id] = v_pri[p_id] = v_sec[s_id] = True
            pos.append(col_id)
            self.steps.append({'type': 'place', 'board': pos.copy(), 'row': cur_row, 'col': col_id, 'message': f'✓ Đặt hậu ({cur_row+1}, {col_id+1})'})
            
            self._solve_advanced(cur_row + 1, v_col, v_pri, v_sec, pos, algo_type)
            
            pos.pop()
            v_col[col_id] = v_pri[p_id] = v_sec[s_id] = False
            self.steps.append({'type': 'backtrack', 'board': pos.copy(), 'row': cur_row, 'col': col_id, 'message': f'← Quay lui'})

    def _count_conflicts(self, row, col, v_col, v_pri, v_sec):
        count = 0
        for r in range(row + 1, self.n):
            for c in range(self.n):
                if not v_col[c] and not v_pri[r-c+self.n-1] and not v_sec[r+c]:
                    if c == col or (r-c) == (row-col) or (r+c) == (row+col):
                        count += 1
        return count

    def _has_empty_domain(self, next_row, cur_col, v_col, v_pri, v_sec):
        if next_row >= self.n: return False
        for r in range(next_row, self.n):
            possible = False
            for c in range(self.n):
                if not v_col[c] and not v_pri[r-c+self.n-1] and not v_sec[r+c]:
                    if c != cur_col and (r-c) != (next_row-1-cur_col) and (r+c) != (next_row-1+cur_col):
                        possible = True
                        break
            if not possible: return True
        return False