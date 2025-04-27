# main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_menu import MainMenu
from db.database import create_table
from ui.comparison_window import ComparisonWindow  # import here

# **1) Store it at module–level so it won't be GC'd**
comparison_window = None

def start_game():
    from ui.game_board import GameBoard
    board = GameBoard(lambda: None, lambda: None)
    board.show()

def compare_algorithms():
    global comparison_window
    board_size = 6  # You can change board size if you want
    comparison_window = ComparisonWindow(board_size=board_size)
    comparison_window.show()


app = QApplication(sys.argv)
create_table()
window = MainMenu(start_game, compare_algorithms)
window.show()
sys.exit(app.exec_())