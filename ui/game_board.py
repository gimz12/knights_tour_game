from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QMessageBox
from PyQt5.QtGui import QColor
import random

class GameBoard(QWidget):
    def __init__(self, validate_func=None, finish_func=None):
        super().__init__()
        self.setWindowTitle("Play the Knight's Tour")
        self.grid = QGridLayout()
        self.buttons = [[QPushButton("") for _ in range(8)] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                btn = self.buttons[i][j]
                btn.setFixedSize(60, 60)
                btn.clicked.connect(lambda checked, x=i, y=j: self.handle_move(x, y))
                self.grid.addWidget(btn, i, j)

        self.setLayout(self.grid)
        self.reset_game()  # Set initial state

    def reset_game(self):
        self.knight_pos = (random.randint(0, 7), random.randint(0, 7))
        self.path = [self.knight_pos]
        self.update_ui()

    def update_ui(self):
        for i in range(8):
            for j in range(8):
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

            if len(self.path) == 64:
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
            0 <= nx < 8 and 0 <= ny < 8 and (nx, ny) not in self.path
            for nx, ny in possible_moves
        )

        if not has_moves:
            QMessageBox.information(
                self, "Game Over", 
                f"😕 No more valid moves!\nYou visited {len(self.path)} squares.\nThe game will now reset."
            )
            self.reset_game()
