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

        self.assertEqual(len(query2.questions), 3)
        self.assertEqual(len(query2.questions[-1].parent_questions), 2)

    def test_query_list_output(self):
        print("testing list output")
        p = Question("What is a prot?", True)
        p2 = "What is a prit?"
        p3 = "What is a prut?"

        query3 = Question_holder([p])
        query3.set_question(p2, p.unique_id)
        query3.set_question(p3, p.unique_id)
        query3.set_question(p3, query3.questions[1].unique_id)

        output = query3.to_list('q',True)
        print(output)
        self.assertEqual(len(output), 2)
        self.assertEqual(len(output[0]), len(output[1]) )
        self.assertEqual(len(output[0]), 3 )

    def test_query_pandas_output(self):
        print("testing pandas output")
        p = Question("What is a prot?", True)
        p2 = "What is a prit?"
        p3 = "What is a prut?"
        a2 = "www.blabla.com"
        a3 = "www.blibli.com"

        query3 = Question_holder([p])
        query3.set_question(p2, p.unique_id)
        query3.set_question(p3, p.unique_id)
        query3.set_question(p3, query3.questions[1].unique_id)
        query3.set_answer(a2, p.unique_id)
        query3.set_answer(a3, query3.questions[-1].unique_id)

        output = query3.to_pandas()
        print(output)
        self.assertEqual(len(output), 2)
        self.assertEqual(output.shape, (2,2))


    def test_question_holder_remove_unwanted_questions(self):
        print("testing remove_unwanted_questions of Question_holder class ")

        print("testing list output")
        p = Question("What is a prot?", True)
        p2 = "What is a prit?"
        p3 = "What is a prut?"

        query3 = Question_holder([p])
        query3.set_question(p2, p.unique_id)
        query3.set_question(p3, p.unique_id)
        query3.set_question(p3, query3.questions[1].unique_id)

        query3.remove_unwanted_questions([p2,p3], "k")
        self.assertEqual(len(query3.questions), 2)
        self.assertEqual(str(query3.questions[-1]), p3)

        query3.remove_unwanted_questions([p, p3], "r")
        self.assertEqual(len(query3.questions), 1)
        self.assertEqual(str(query3.questions[-1]), p2)

    def test_question_holder_set_answer(self):
        print("testing set_answer method of Question_holder class ")

        p = Question("What is a prot?", True)
        query4 = Question_holder([p])
        a2 = "www.blabla.com"
        a3 = "www.blibli.com"

        query4.set_answer(a2, p.unique_id)
        query4.set_answer(a3, p.unique_id)
        query4.set_answer(a3, "blabla")

        self.assertEqual(len(query4.answers), 2)
        self.assertEqual(len(query4.answers[-1].parent_questions), 2)

    def test_question_holder_ingest_answers(self):
        print("testing ingest answers method of Question_holder class ")

        p = Question("What is a prot?", True)
        query4 = Question_holder([p])
        a2 = "www.blabla.com"
        a3 = "www.blibli.com"
        query4.ingest_new_answers({str(p): [a2,a3]} )
        self.assertEqual(len(query4.answers), 2)
        self.assertEqual(len(query4.answers[-1].parent_questions), 1)

    def test_question_holder_main_get_questions(self):
        from main import main_get_questions
        q = "What is a damselfish?"
        query = main_get_questions(q)
        self.assertEqual(isinstance(query, src.classes.Question-holder, True))






if __name__ == '__main__':
    unittest.main()

