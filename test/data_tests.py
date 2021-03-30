# -*- coding: utf-8 -*-
"""Unit tests for the funcitons in data"""

import unittest
import sys
from pathlib import Path
sys.path.append(Path("..", "src"))
from src.data import Question

class Test_q_data(unittest.TestCase):

    def test_q_init_with_question(self):
        print("\n testing with a question")
        q = Question("What is a damselfish?")
        self.assertEqual(len(q.keywords),2, "should be 2!")

    def test_q_init_with_kw(self):
        print("\ntesting with kws!")
        q = Question("bread, butter, jam")

        self.assertEqual(len(q.keywords),3, "should be 3!")

if __name__ == '__main__':
    unittest.main()

