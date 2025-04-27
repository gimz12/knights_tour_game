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

    def test_algorithm_comparison(self):
        print("\n=== Algorithm Timing Comparison ===", flush=True)

        # Test backtracking
        print("Running Backtracking algorithm...", flush=True)
        t0 = time.time()
        knight_tour_backtracking(self.start_x, self.start_y, self.test_size)
        bt_time = time.time() - t0
        print(f"Backtracking took: {bt_time:.4f} seconds", flush=True)

        # Test Warnsdorff's
        print("\nRunning Warnsdorff's algorithm...", flush=True)
        t1 = time.time()
        knight_tour_warnsdorff(self.start_x, self.start_y, self.test_size)
        ws_time = time.time() - t1
        print(f"Warnsdorff took:   {ws_time:.4f} seconds", flush=True)

        # Show comparison
        print("\n=== Results ===", flush=True)
        print(f"Backtracking: {bt_time:.4f}s", flush=True)
        print(f"Warnsdorff:   {ws_time:.4f}s", flush=True)
        print(f"Difference:   {bt_time - ws_time:.4f}s", flush=True)

        self.assertLess(ws_time, bt_time)

if __name__ == "__main__":
    unittest.main(verbosity=2)
