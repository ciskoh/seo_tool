# classes for stroring questions and answers

import re
import uuid
import pandas as pd


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

    def __init__(self, link, q_id):
        self.main_question_id: str = None
        self.link: str = None
        self.ranking_metrics: float = None
        self.quality_metrics: float = None
        self.similarity_metrics: float = None
        self.main_question_id = q_id
        self.parent_questions: set = set([self.main_question_id])
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

    def __str__(self):
        if self.questions:
            fin_str = "Questions: "
            fin_str += "; ".join([str(q) for q in self.questions])
        if self.answers:
            fin_str += "\n Answers: "
            fin_str += "; ".join([str(a) for a in self.answers])
        return fin_str

    def ingest_new_questions(self, new_questions):
        """function to import multiple new questions as Question objects
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
                parent_q_id = [q.unique_id for q in self.questions if str(q) == k]
                if not parent_q_id:
                    raise LookupError("parent question not found!")
                if isinstance(new_questions[k], list):
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

    def get_question(self, q_id=None, q_str=None):
        """returns a question in the query holder using id or string
        Parameters:
        q_id: str of question
        q_str: str of question

        Returns Question object"""

        if not q_id and not q_str:
            raise ValueError("q_id or q_str must be set")
        if q_id and q_str:
            raise ValueError("choose either q_id or q_str")

        if q_id:
            got_q = [q for q in self.questions if q.unique_id == q_id]
        if q_str:
            got_q =  [q for q in self.questions if str(q) == q_str]
        if not got_q:
            raise ValueError("Question not found")
        else:
            return got_q[0]

    def remove_unwanted_questions(self, q_list, mode="k") -> None:
        """removes unwanted questions from query
        Parameters:
        q_list: list of {string} questions
        mode: str "k" if q_list are the questions to keep or "r" if q_list are the questions to be removed

        Returns None
        """
        if mode == "k":
            for q in self.questions:
                if str(q) not in q_list:
                    self.questions.remove(q)
        if mode == "r":
            for q in self.questions:
                if str(q) in q_list:
                    self.questions.remove(q)

    def set_answer(self, new_a, parent_q_id=None):
        """function to set questions while checking to avoid repetition
        and consolidating parent questions
        parameters:
        new_a: string
        parent_q_id: str with unique_id DISCARDED
        """
        # set params
        if isinstance(new_a, Answer):
            raise NotImplementedError("new_a must be a string for now!")

        parent_q_id = parent_q_id if parent_q_id else self.main_question_id

        if new_a in [str(a) for a in self.answers]:
            existing_a = [a for a in self.answers if str(a) == new_a][0]
            existing_a.parent_questions.add(parent_q_id)
        else:
            self.answers.append(Answer(new_a, False))

    def ingest_new_answers(self, new_answers):

        if isinstance(new_answers, list):
            parent_q_id = self.main_question_id
            for new_q in new_answers:
                self.set_question(new_q, parent_q_id)
        elif isinstance(new_answers, dict):
            for k in new_answers:
                parent_q_id = [q.unique_id for q in self.questions if str(q) == k]
                if not parent_q_id:
                    raise LookupError("parent question not found!")
                if isinstance(new_answers[k], list):
                    for new_a in new_answers[k]:
                        self.set_answer(new_a, parent_q_id[0])

    def to_list(self, mode=None, id=False) -> list:
        """exports all questions and /or answers as list
        Parameters:
        mode: str "q" for questions and "a" for answers
        id: bool adds ids as second level list

        Returns list"""
        if mode == "q":
            my_qs = [str(q) for q in self.questions]
            if id:
                my_ids = [q.unique_id for q in self.questions]
                my_qs = list([my_qs, my_ids])
            return my_qs
        elif mode == "a":
            my_as = [str(a) for a in self.answers]
            if id:
                my_ids = [a.unique_id for a in self.questions]
                my_as = list([my_as, my_ids])
            return my_as
        else:
            raise ValueError("mode parameter must be 'q' or 'a'!!")
    #TODO: add more columns
    def to_pandas(self):
        answer_list=self.answers
        question_list=self.questions
        final_dict={}
        fin_df = pd.DataFrame(columns=["parent_question", "link"])
        for n,a in enumerate(answer_list):
            try:
                parent_q = str(self.get_question(q_id=a.parent_questions))
            except ValueError:
                parent_q = "Question not found!!!"

            fin_df.loc[n]=[parent_q, a.link]

        return fin_df



