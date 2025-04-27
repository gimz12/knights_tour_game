from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

class MainMenu(QWidget):
    def __init__(self, start_game_callback, compare_callback, view_winners_callback):
        super().__init__()
        self.setWindowTitle("Knight's Tour Game")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Welcome to Knight's Tour!"))
        
        start_button = QPushButton("Start Game")
        compare_button = QPushButton("Compare Algorithms")
        winners_button = QPushButton("View Winners")  # New button

        start_button.clicked.connect(start_game_callback)
        compare_button.clicked.connect(compare_callback)
        winners_button.clicked.connect(view_winners_callback)  # Connect it

        layout.addWidget(start_button)
        layout.addWidget(compare_button)
        layout.addWidget(winners_button)  # Add it to layout

        self.setLayout(layout)
