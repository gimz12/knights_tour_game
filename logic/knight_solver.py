import random

moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
         (-2, -1), (-1, -2), (1, -2), (2, -1)]

def is_valid(x, y, board, board_size):
    return 0 <= x < board_size and 0 <= y < board_size and board[x][y] == -1

def knight_tour_backtracking(start_x, start_y, board_size=8):
    board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
    path = []

    def solve(x, y, move_count):
        if move_count == board_size * board_size:
            path.append((x, y))
            return True

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, board, board_size):
                board[nx][ny] = move_count
                path.append((x, y))
                print(f"[BT-DEBUG] Move {move_count}: ({nx}, {ny})")
                if solve(nx, ny, move_count + 1):
                    return True
                board[nx][ny] = -1
                path.pop()
                print(f"[BT-DEBUG] Backtracking from ({nx}, {ny})")

        return False

    board[start_x][start_y] = 0
    print(f"[BT-DEBUG] Starting position: ({start_x}, {start_y})")
    solve(start_x, start_y, 1)
    return path + [(start_x, start_y)] if (start_x, start_y) not in path else path


def count_onward_moves(x, y, board, board_size):
    return sum(1 for dx, dy in moves
               if is_valid(x + dx, y + dy, board, board_size))

def knight_tour_warnsdorff(start_x, start_y, board_size=8):
    board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
    x, y = start_x, start_y
    board[x][y] = 0
    path = [(x, y)]

    print(f"[WS-DEBUG] Starting position: ({x}, {y})")

    for move_num in range(1, board_size * board_size):
        candidates = []
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, board, board_size):
                count = count_onward_moves(nx, ny, board, board_size)
                candidates.append(((nx, ny), count))

        if not candidates:
            print(f"[WS-DEBUG] No more moves at step {move_num}")
            return []

        candidates.sort(key=lambda el: el[1])
        min_deg = candidates[0][1]
        min_candidates = [pos for pos, deg in candidates if deg == min_deg]
        x, y = random.choice(min_candidates)
        board[x][y] = move_num
        path.append((x, y))
        print(f"[WS-DEBUG] Move {move_num}: ({x}, {y})")

    return path
