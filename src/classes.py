# classes for stroring questions and answers

import re
import uuid


class Question:
    """Class that holds Questions.
     parent_questions is a list of other question objects
     Answers include objects of type Answer only for the main question"""
    unique_id: str = None
    main_question = None
    keywords: list = None
    parent_questions: set = set([])
    answers: list = None
    is_user_question: bool = False

    # TODO: maybe implement "type" attribute to distinguish between user, ppa and automatically generated?

    def __init__(self, main_question, is_user_question=False, parent_question_id=None):
        """initialises object and detects if main_question is question or list of keywords
        Parameters:
            main_question : string of current question
        Optional parameters:
            is_user_question: bool if is user input
            parent_question_id: str or Question object"""
        self.unique_id: str = None
        self.main_question = None
        self.keywords: list = None
        self.parent_questions: set = set([])
        self.answers: list = None
        self.is_user_question: bool = False

        self.main_question = str(main_question)
        self.unique_id = str(self.create_unique_id())
        if len(self.main_question.split(" ")) > 2 and ("?" in self.main_question):
            print("you entered a question!")
            self.keywords = self.get_keywords_from_question(self.main_question)
            # self.parent_questions.append(main_question)
        else:
            print("you entered keywords!")
            self.main_question = re.sub("[\W]", ",", self.main_question)
            self.keywords = [k for k in self.main_question.split(",") if len(k) > 0]
        if is_user_question:
            self.is_user_question = True
        if parent_question_id:
            id = parent_question_id if isinstance(parent_question_id, str) else parent_question_id.unique_id
            self.parent_questions.add(parent_question_id)


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

    def __str__(self):
        return self.main_question


class Answer:
    """class containing answer to a question and related metric"""
    main_question_id: str = None
    link: str = None
    ranking_metrics: float = None
    quality_metrics: float = None
    similarity_metrics: float = None

    def __init__(self, q, link):
        self.main_question_id: str = None
        self.link: str = None
        self.ranking_metrics: float = None
        self.quality_metrics: float = None
        self.similarity_metrics: float = None
        self.main_question_id = q.unique_id
        self.link = link

    def __str__(self):
        return self.link


class Question_holder:


    def __init__(self, q_list):
        """initializes Question_holder """
        self.main_question_id: str = None
        self.questions: list = []
        self.answers: list = []

        for q in q_list:
            # get user question id
            if q.is_user_question:
                self.main_question_id = q.unique_id
            self.questions
            if isinstance(q, Question):
                self.questions.append(q)
            else:
                raise TypeError("object q is not of type Question")


    def ingest_new_questions(self, new_questions):
        """function to import new questions as Question objects
        parameters:
        new_questions: list or dic of questions, if list the parent question will be the main
                        question of the Question_holder, if new_questions is a dic the key will be used to match with
                        existing parent questions """
        if isinstance(new_questions, list):
            parent_q_id = self.main_question_id
            for new_q in new_questions:
                self.set_question(new_q, parent_q_id)
        elif isinstance(new_questions, dict):
            for k in new_questions:
                parent_q_id = [q.unique_id for q in self.questions if str(q) == k ]
                if not parent_q_id:
                    raise LookupError("parent question not found!")
                if isinstance(new_questions[k],list):
                    for new_q in new_questions[k]:
                        self.set_question(new_q, parent_q_id[0])

    def set_question(self, new_q, parent_q_id=None):
        """function to set questions while checking to avoid repetition
        and consolidating parent questions
        parameters:
        new_q: string
        parent_q_id: str with unique_id DISCARDED
        """
        # set params
        if isinstance(new_q, Question):
            raise NotImplementedError("new_q must be a string for now!")

        parent_q_id = parent_q_id if parent_q_id else self.main_question_id

        if new_q in [str(q) for q in self.questions]:
            existing_q = [q for q in self.questions if str(q) == new_q][0]
            existing_q.parent_questions.add(parent_q_id)
        else:
            self.questions.append(Question(new_q, False, parent_q_id))

    def __str__(self):
        if self.questions:
            fin_str = "Questions: "
            fin_str += "; ".join([str(q) for q in self.questions])
        if self.answers:
            fin_str += "\n Answers: "
            fin_str += "; ".join([str(a) for a in self.answers])
        return fin_str