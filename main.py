import sys
from PyQt5.QtWidgets import QApplication, QInputDialog
from ui.main_menu import MainMenu
from db.database import create_table
from ui.comparison_window import ComparisonWindow
from ui.view_winners import ViewWinners  # Import new winners window

comparison_window = None
winners_window = None

def start_game():
    from ui.game_board import GameBoard
    
    # Ask the user for the board size
    board_size, ok = QInputDialog.getInt(None, "Select Board Size", "Enter board size:", 8, 4, 12, 1)
    if ok:
        board = GameBoard(board_size=board_size)
        board.show()

def compare_algorithms():
    global comparison_window
    board_size = 6  
    comparison_window = ComparisonWindow(board_size=board_size)
    comparison_window.show()

def view_winners():
    global winners_window
    winners_window = ViewWinners()
    winners_window.show()

app = QApplication(sys.argv)
create_table()


window = MainMenu(start_game, compare_algorithms, view_winners)
window.show()

sys.exit(app.exec_())
