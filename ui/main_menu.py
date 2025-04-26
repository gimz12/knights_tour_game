from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

class MainMenu(QWidget):
    def __init__(self, start_game_callback, compare_callback):
        super().__init__()
        self.setWindowTitle("Knight's Tour Game")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Welcome to Knight's Tour!"))
        
        start_button = QPushButton("Start Game")
        compare_button = QPushButton("Compare Algorithms")
        
        start_button.clicked.connect(start_game_callback)
        compare_button.clicked.connect(compare_callback)

        layout.addWidget(start_button)
        layout.addWidget(compare_button)

        self.setLayout(layout)
