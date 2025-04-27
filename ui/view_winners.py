from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
from db.database import connect_db

class ViewWinners(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Winners List")
        self.resize(400, 400)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.load_winners()

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.close)

        layout.addWidget(QLabel("Saved Winners:"))
        layout.addWidget(self.list_widget)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_winners(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, method, sequence FROM winners")
        winners = cursor.fetchall()
        conn.close()

        for winner in winners:
            name, method, sequence = winner
            self.list_widget.addItem(f"{name} - {method}\nPath: {sequence}\n")
