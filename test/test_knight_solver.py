# test/test_knight_solver.py

import unittest
import time
import random

from logic.knight_solver import (
    knight_tour_backtracking,
    knight_tour_warnsdorff
)

class TestKnightSolver(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Only run once per full test class
        cls.test_size = 6
        cls.start_x = random.randint(0, cls.test_size - 1)
        cls.start_y = random.randint(0, cls.test_size - 1)
        print(f"\n[Test Setup] Random start position: ({cls.start_x}, {cls.start_y})\n", flush=True)

    def test_backtracking_solution(self):
        path = knight_tour_backtracking(self.start_x, self.start_y, self.test_size)
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), self.test_size * self.test_size)

    def test_warnsdorff_solution(self):
        path = knight_tour_warnsdorff(self.start_x, self.start_y, self.test_size)
        self.assertIsInstance(path, list)
        self.assertEqual(len(path), self.test_size * self.test_size)

    def test_warnsdorff_is_faster(self):
        t0 = time.time()
        knight_tour_backtracking(self.start_x, self.start_y, self.test_size)
        bt_dur = time.time() - t0

        t1 = time.time()
        knight_tour_warnsdorff(self.start_x, self.start_y, self.test_size)
        ws_dur = time.time() - t1

        print(f"[Timing] Backtracking: {bt_dur:.4f}s | Warnsdorff: {ws_dur:.4f}s", flush=True)
        self.assertLess(ws_dur, bt_dur)

    def test_multiple_rounds_timing(self):
        rounds = 10
        bt_times = []
        ws_times = []

        for i in range(rounds):
            print(f"[Round {i+1}] Testing backtracking...", flush=True)
            t0 = time.time()
            knight_tour_backtracking(self.start_x, self.start_y, self.test_size)
            bt_time = time.time() - t0
            bt_times.append(bt_time)
            print(f"[Round {i+1}] Backtracking took {bt_time:.4f} seconds", flush=True)

            print(f"[Round {i+1}] Testing Warnsdorff...", flush=True)
            t1 = time.time()
            knight_tour_warnsdorff(self.start_x, self.start_y, self.test_size)
            ws_time = time.time() - t1
            ws_times.append(ws_time)
            print(f"[Round {i+1}] Warnsdorff took   {ws_time:.4f} seconds", flush=True)

        # Average times
        avg_bt = sum(bt_times) / rounds
        avg_ws = sum(ws_times) / rounds

        print("\n=== Timing Summary ===", flush=True)
        print(f"Backtracking average time: {avg_bt:.4f} seconds", flush=True)
        print(f"Warnsdorff average time:   {avg_ws:.4f} seconds", flush=True)

        self.assertLess(avg_ws, avg_bt)

if __name__ == "__main__":
    unittest.main(verbosity=2)
