# classes for stroring questions and answers

import re
import uuid


class Question:
    """Class that holds Questions.
     related_questions is a list of other question objects
     Answers include objects of type Answer only for the main question"""
    unique_id: str = None
    main_question = None
    keywords: list = None
    related_questions: set = {}
    answers: list = None
    is_user_question: bool = False

    def __init__(self, main_question, is_user_question=False):
        """initialises object and detects if main_question is question or list of keywords"""
        self.main_question = main_question
        self.unique_id = str(self.create_unique_id())
        if len(self.main_question.split(" ")) > 2 and ("?" in self.main_question):
            print("you entered a question!")
            self.keywords = self.get_keywords_from_question(self.main_question)
            # self.related_questions.append(main_question)
        else:
            print("you entered keywords!")
            self.main_question = re.sub("[\W]", ",", self.main_question)
            self.keywords = [k for k in self.main_question.split(",") if len(k) > 0]
        if is_user_question:
            self.is_user_question = True

    def get_keywords_from_question(self, main_question):
        """ basic keyword retrieval from question
        """
        clean_input = re.sub("[^A-Za-z0-9\s]", "", main_question).lower()
        Q0_tokens = clean_input.split(" ")  # TODO:  this can be improved with tokenizer
        lst2 = sorted(Q0_tokens, key=len, reverse=True)
        return lst2[:2]

    def create_unique_id(self):
        unique_id = uuid.uuid4()
        return unique_id

class Answer:
    """class containing answer to a question and related metric"""
    main_question_id: str = None
    link: str = None
    ranking_metrics: float = None
    quality_metrics: float = None
    similarity_metrics: float = None

    def __init__(self, q, link):
        self.main_question_id = q.unique_id
        self.link = link

class Question_holder:
    main_question_id: str = None
    questions : list = []
    answers : list = []

    def __init__(self,q_list):
        """initializes """
        for q in q_list:
            # get user question id
            if not self.main_question_id:
                if q.is_user_question:
                    self.main_question_id = q.unique_id

            if isinstance(q, Question):
                self.questions.append(q)
            else:
                raise TypeError("object q is not of type Question")
