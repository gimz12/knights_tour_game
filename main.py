import sys
from PyQt5.QtWidgets import QApplication, QInputDialog
from ui.main_menu import MainMenu
from db.database import create_table
from ui.comparison_window import ComparisonWindow  

comparison_window = None

def start_game():
    from ui.game_board import GameBoard
    
    # Ask the user for the board size
    board_size, ok = QInputDialog.getInt(None, "Select Board Size", "Enter board size:", 8, 4, 12, 1)
    if ok:
        board = GameBoard(board_size=board_size)
        board.show()

def compare_algorithms():
    global comparison_window
    board_size = 6  # Board size 
    comparison_window = ComparisonWindow(board_size=board_size)
    comparison_window.show()

app = QApplication(sys.argv)
create_table()
window = MainMenu(start_game, compare_algorithms)
window.show()
sys.exit(app.exec_())
