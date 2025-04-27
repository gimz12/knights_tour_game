from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtGui import QColor
import random
from logic.knight_solver import knight_tour_warnsdorff

class GameBoard(QWidget):
    def __init__(self, board_size=8, validate_func=None, finish_func=None):
        super().__init__()
        self.setWindowTitle("Play the Knight's Tour")
        self.board_size = board_size  # Set board size dynamically
        self.grid = QGridLayout()
        self.buttons = [[QPushButton("") for _ in range(board_size)] for _ in range(board_size)]

        # Create buttons and add to the grid layout
        for i in range(board_size):
            for j in range(board_size):
                btn = self.buttons[i][j]
                btn.setFixedSize(60, 60)
                btn.clicked.connect(lambda checked, x=i, y=j: self.handle_move(x, y))
                self.grid.addWidget(btn, i, j)

        # Add an "Auto Solve" button
        self.auto_solve_button = QPushButton("Auto Solve")
        self.auto_solve_button.clicked.connect(self.auto_solve)
        self.grid.addWidget(self.auto_solve_button, board_size, 0, 1, board_size)

        self.setLayout(self.grid)
        self.reset_game()  # Set initial state

        self.path_step = 0  # Track the current step in the solution path

    def reset_game(self):
        self.knight_pos = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
        self.path = [self.knight_pos]
        self.update_ui()

    def update_ui(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                btn = self.buttons[i][j]
                btn.setText("")
                btn.setStyleSheet("")

                if (i, j) in self.path and (i, j) != self.knight_pos:
                    btn.setStyleSheet("background-color: lightblue;")

        x, y = self.knight_pos
        self.buttons[x][y].setText("♞")
        self.buttons[x][y].setStyleSheet("background-color: lightgreen; font-size: 20px;")

    def handle_move(self, x, y):
        if (x, y) in self.path:
            return

        last_x, last_y = self.knight_pos
        if (abs(x - last_x), abs(y - last_y)) in [(1, 2), (2, 1)]:
            self.knight_pos = (x, y)
            self.path.append(self.knight_pos)
            self.update_ui()

            if len(self.path) == self.board_size * self.board_size:
                QMessageBox.information(self, "Victory", "🎉 You completed the Knight's Tour!")
                self.reset_game()
            else:
                self.check_game_status()
        else:
            QMessageBox.warning(self, "Invalid Move", "That's not a valid knight move!")

    def check_game_status(self):
        x, y = self.knight_pos
        possible_moves = [(x + dx, y + dy) for dx, dy in 
                          [(2, 1), (1, 2), (-1, 2), (-2, 1),
                           (-2, -1), (-1, -2), (1, -2), (2, -1)]]
        
        has_moves = any(
            0 <= nx < self.board_size and 0 <= ny < self.board_size and (nx, ny) not in self.path
            for nx, ny in possible_moves
        )

        if not has_moves:
            QMessageBox.information(
                self, "Game Over", 
                f"😕 No more valid moves!\nYou visited {len(self.path)} squares.\nThe game will now reset."
            )
            self.reset_game()

    def auto_solve(self):
        # Use the knight's tour Warnsdorff's heuristic algorithm to find the solution
        start_x, start_y = self.knight_pos
        self.path = knight_tour_warnsdorff(start_x, start_y, self.board_size)
        self.path_step = 0  # Reset the step tracker

        # Start the timer to show one move at a time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_step)
        self.timer.start(500)  # Set interval to 500ms (can be adjusted)

    def show_next_step(self):
        if self.path_step < len(self.path):
            # Update knight position and path
            self.knight_pos = self.path[self.path_step]
            self.path_step += 1
            self.update_ui()

        if self.path_step == len(self.path):
            # Stop the timer when the path is fully shown
            self.timer.stop()
            QMessageBox.information(self, "Victory", "🎉 The Knight's Tour is completed automatically!")
            self.reset_game()
