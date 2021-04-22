# -*- coding: utf-8 -*-
"""Unit tests for the funcitons in data"""

import unittest
import sys
from pathlib import Path
sys.path.append(Path("..", "src"))
from src import Question, Answer, Question_holder
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

class Test_classes(unittest.TestCase):

    def test_question_holder_creation(self):
        print("testing set method of Question_holder class ")
        q = Question("What is a damselfish?", True)
        q2 = Question("What is a clownfish?")
        query = Question_holder([q, q2])
        self.assertEqual(query.main_question_id,q.unique_id)
        del q,q2,query
        return None

    def test_question_holder_set(self):
        print("testing set method of Question_holder class ")

        p = Question("What is a prot?", True)
        p2 = "What is a prit?"
        p3 = "What is a prut?"

        query2 = Question_holder([p])
        query2.set_question(p2, p.unique_id)
        query2.set_question(p3, p.unique_id)
        query2.set_question(p3, query2.questions[1].unique_id)

        test = query2.questions[-1].parent_questions
        self.assertEqual(len(query2.questions), 3)
        self.assertEqual(len(query2.questions[-1].parent_questions), 2)

if __name__ == '__main__':
    unittest.main()

