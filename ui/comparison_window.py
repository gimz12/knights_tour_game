from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import time
import traceback

from logic.knight_solver import knight_tour_backtracking, knight_tour_warnsdorff

class WorkerSignals(QObject):
    finished = pyqtSignal(float, float, bool, bool, list, list)
    error = pyqtSignal(str)

class AlgorithmRunner(QRunnable):
    def __init__(self, start_x, start_y, board_size):
        super().__init__()
        self.start_x = start_x
        self.start_y = start_y
        self.board_size = board_size
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            print("[DEBUG] Starting backtracking algorithm")
            t0 = time.time()
            result_bt = knight_tour_backtracking(self.start_x, self.start_y, self.board_size)
            bt_time = time.time() - t0
            success_bt = isinstance(result_bt, list) and len(result_bt) == self.board_size ** 2
            print(f"[DEBUG] Backtracking finished in {bt_time:.4f}s with success: {success_bt}")

            print("[DEBUG] Starting Warnsdorff algorithm")
            t1 = time.time()
            result_ws = knight_tour_warnsdorff(self.start_x, self.start_y, self.board_size)
            ws_time = time.time() - t1
            success_ws = isinstance(result_ws, list) and len(result_ws) == self.board_size ** 2
            print(f"[DEBUG] Warnsdorff finished in {ws_time:.4f}s with success: {success_ws}")

            self.signals.finished.emit(bt_time, ws_time, success_bt, success_ws, result_bt, result_ws)

        except Exception as e:
            traceback_str = traceback.format_exc()
            print("[ERROR] Exception in AlgorithmRunner:\n", traceback_str)
            self.signals.error.emit(traceback_str)

class ComparisonWindow(QWidget):
    def __init__(self, start_x, start_y, board_size=8):
        super().__init__()
        self.setWindowTitle("Algorithm Comparison")
        self.resize(800, 700)

        self.layout = QVBoxLayout()
        self.status_label = QLabel("Running comparison… please wait.")
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)

        print("[DEBUG] Initializing ComparisonWindow")

        self.threadpool = QThreadPool()
        self.worker = AlgorithmRunner(start_x, start_y, board_size)
        self.worker.signals.finished.connect(self.display_results)
        self.worker.signals.error.connect(self.display_error)
        self.threadpool.start(self.worker)

    def display_results(self, bt_time, ws_time, bt_success, ws_success, bt_path, ws_path):
        print("[DEBUG] Received comparison results, updating UI…")
        self.status_label.hide()

        grid = QGridLayout()
        board_size = len(bt_path) ** 0.5
        board_size = int(board_size)

        bt_steps = {pos: idx+1 for idx, pos in enumerate(bt_path)}
        ws_steps = {pos: idx+1 for idx, pos in enumerate(ws_path)}

        for x in range(board_size):
            for y in range(board_size):
                label = QLabel()
                label.setFixedSize(50, 50)
                label.setAlignment(Qt.AlignCenter)
                font = QFont("Courier", 10)
                label.setFont(font)
                label.setStyleSheet("border: 1px solid gray;")

                bt = bt_steps.get((x, y))
                ws = ws_steps.get((x, y))

                if bt and ws:
                    label.setText(f"B:{bt}\nW:{ws}")
                    label.setStyleSheet("background-color: #eaeaff; color: purple; border: 1px solid black;")
                elif bt:
                    label.setText(f"B:{bt}")
                    label.setStyleSheet("background-color: #d0e7ff; color: blue;")
                elif ws:
                    label.setText(f"W:{ws}")
                    label.setStyleSheet("background-color: #ffe4cc; color: orange;")

                grid.addWidget(label, x, y)

        self.layout.addLayout(grid)

        # Performance Chart
        fig, ax = plt.subplots()
        ax.bar(["Backtracking", "Warnsdorff"], [bt_time, ws_time], color=["#1f77b4", "#ff7f0e"])
        ax.set_ylabel("Time (seconds)")
        ax.set_title("Knight’s Tour: Algorithm Performance")
        ax.tick_params(axis='x', rotation=15)

        canvas = FigureCanvas(fig)
        self.layout.addWidget(canvas)
        canvas.draw()

        # Result Summary
        if bt_success and ws_success:
            result_msg = "🎉 Both algorithms found a complete tour! (Win)"
        elif bt_success or ws_success:
            result_msg = "⚖️ Only one algorithm found a complete tour. (Draw)"
        else:
            result_msg = "😞 Neither algorithm found a solution. (Loss)"

        print("[DEBUG] Showing result message:", result_msg)
        QMessageBox.information(self, "Comparison Result", result_msg)

    def display_error(self, error_msg):
        print("[ERROR] Displaying error in UI")
        self.status_label.setText("An error occurred:\n" + error_msg)
        QMessageBox.critical(self, "Error", error_msg)
