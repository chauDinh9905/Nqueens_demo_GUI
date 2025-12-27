import time

class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.steps = []
        self.solutions = []
        self.first_sol_time = 0 
        self.start_time = 0
        self.timeout_limit = 10.0  # Giới hạn 10 giây
        self.is_timeout = False

    def solve_with_steps(self, algo_type="Đệ quy"):
        self.start_time = time.perf_counter()
        self.first_sol_time = 0
        self.steps = []
        self.solutions = []
        self.is_timeout = False
        
        visited_col = [False] * self.n
        visited_dig_pri = [False] * (2 * self.n - 1)
        visited_dig_sec = [False] * (2 * self.n - 1)
        
        try:
            if algo_type == "Đệ quy":
                self._backtrack(0, visited_col, visited_dig_pri, visited_dig_sec, [])
            else:
                self._solve_advanced(0, visited_col, visited_dig_pri, visited_dig_sec, [], algo_type)
        except StopIteration:
            # Dùng StopIteration để thoát khỏi đệ quy nhanh chóng
            pass
            
        execution_time = (time.perf_counter() - self.start_time) * 1000 
        return self.steps, self.solutions, execution_time, self.first_sol_time, self.is_timeout

    def _check_constraints(self):
        """Kiểm tra thời gian và giới hạn N"""
        # 1. Kiểm tra timeout
        if (time.perf_counter() - self.start_time) > self.timeout_limit:
            self.is_timeout = True
            self.steps.append({
                'type': 'invalid', 'board': [], 'row': -1, 'col': -1,
                'message': '❌ Tốn quá nhiều thời gian!'
            })
            raise StopIteration
        
        # 2. Kiểm tra N > 13 và đã có 1 lời giải
        if self.n > 13 and len(self.solutions) >= 1:
            raise StopIteration

    def _record_solution(self, pos):
        self.solutions.append(pos.copy())
        if len(self.solutions) == 1:
            self.first_sol_time = (time.perf_counter() - self.start_time) * 1000
        
        self.steps.append({
            'type': 'solution', 'board': pos.copy(), 'row': self.n, 'col': -1,
            'message': f'🎉 Tìm thấy nghiệm {len(self.solutions)}: { [p+1 for p in pos] }'
        })

    def _backtrack(self, cur_row, visited_col, visited_dig_pri, visited_dig_sec, pos):
        self._check_constraints() # Kiểm tra mỗi khi vào một tầng đệ quy mới

        if cur_row == self.n:
            self._record_solution(pos)
            return

        for col_id in range(self.n):
            # Kiểm tra thời gian cả trong vòng lặp để thoát nhanh hơn
            if (time.perf_counter() - self.start_time) > self.timeout_limit: self._check_constraints()

            dig_pri_id = cur_row - col_id + self.n - 1
            dig_sec_id = cur_row + col_id
            
            self.steps.append({
                'type': 'try', 'board': pos.copy(), 'row': cur_row, 'col': col_id,
                'message': f'🔍 Thử đặt tại ({cur_row+1}, {col_id+1})'
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
        self._check_constraints()

        if cur_row == self.n:
            self._record_solution(pos)
            return

        candidates = []
        for col_id in range(self.n):
            p_id, s_id = cur_row - col_id + self.n - 1, cur_row + col_id
            if not v_col[col_id] and not v_pri[p_id] and not v_sec[s_id]:
                candidates.append(col_id)

        if "LCV" in algo_type:
            candidates.sort(key=lambda c: self._count_conflicts(cur_row, c, v_col, v_pri, v_sec))

        for col_id in candidates:
            p_id, s_id = cur_row - col_id + self.n - 1, cur_row + col_id
            
            if "Forward Checking" in algo_type:
                if self._has_empty_domain(cur_row + 1, col_id, v_col, v_pri, v_sec):
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