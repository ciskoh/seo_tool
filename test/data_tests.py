# -*- coding: utf-8 -*-
"""Unit tests for the funcitons in data"""

import unittest
import sys
from pathlib import Path
sys.path.append(Path("..", "src"))
from src.data import Question
from src.data import get_ppas_and_answers
class Test_q_data(unittest.TestCase):

    def test_q_init_with_question(self):
        print("\n testing with a question")
        q = Question("What is a damselfish?")
        self.assertEqual(len(q.keywords),2, "should be 2!")


    def test_q_init_with_kw(self):
        print("\n testing with kws!")
        q = Question("bread, butter, jam")
        self.assertEqual(len(q.keywords),3, "should be 3!")

    def test_question_generation(self):
        from src.data import generate_automatic_questions
        print("\n testing question generation")
        q = Question("bread, butter, jam")
        auto_q = generate_automatic_questions(q.keywords, Path("..", "references", "words_for_questions.csv"))
        self.assertEqual(all([q.keywords[0] in quest for quest in auto_q]), True, "missing keywords")

    def test_ppa_retrieval(self):
        #TODO: this test is not very good
        print("testing ppa retrieval")
        q_list=["What is a damselfish?", "What is clownfish?", "What is a sea sponge?" ]
        results = get_ppas_and_answers(q_list, mode="ppa")
        pass
        self.assertCountEqual(q_list, results["ppa"].keys())
if __name__ == '__main__':
    unittest.main()

