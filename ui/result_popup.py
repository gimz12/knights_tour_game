from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

class ResultPopup(QWidget):
    def __init__(self, save_callback):
        super().__init__()
        self.setWindowTitle("Save Result")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Congratulations! You completed the tour."))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        layout.addWidget(self.name_input)

        save_btn = QPushButton("Save Result")
        save_btn.clicked.connect(lambda: save_callback(self.name_input.text()))
        layout.addWidget(save_btn)

        self.setLayout(layout)
