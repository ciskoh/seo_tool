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
        self.answers: set = set([])
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

    def set_answer(self, new_a):
        """function to set questions while checking to avoid repetition
        and consolidating parent questions
        parameters:
        new_a: string
        parent_q_id: str with unique_id
        """
        # set params
        if isinstance(new_a, Answer):
            raise NotImplementedError("answer must be a string for now!")
        if new_a not in [str(a) for a in self.answers]:
            self.answers.add(Answer(new_a, self.unique_id))
        else:
            raise ValueError("Answer already present")

    def __str__(self):
        return self.main_question


class Answer:
    """class containing answer to a question and related metric"""
    unique_id: str = None
    link: str = None
    metrics = None
    parent_questions = set([])
    def __init__(self, link, q_id):
        self.unique_id: str = str(self.create_unique_id())
        self.link: str = link
        self.parent_questions: set = set([q_id])
        self.metrics = None

    def create_unique_id(self):
        unique_id = uuid.uuid4()
        return unique_id

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
            got_q = [q for q in self.questions if str(q) == q_str]
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

    def ingest_new_answers(self, new_answers):

        if isinstance(new_answers, list):
            parent_q_id = self.main_question_id
            for new_q in new_answers:
                self.set_question(new_q, parent_q_id)
        elif isinstance(new_answers, dict):
            for k in new_answers:
                parent_q = self.get_question(q_str=k)
                if isinstance(new_answers[k], list):
                    for new_a in new_answers[k]:
                        parent_q.set_answer(new_a)
                else:
                    parent_q.set_answer(new_answers[k])

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

    # TODO: add more columns

    def to_pandas(self, columns=["parent_question", "link"]):
        """get a pandas df with all questions and answers in query"""
        final_lst = []
        for q in self.questions:
            if q.answers:
                final_lst += [[str(q),str(a)] for a in q.answers]
            else:
                final_lst.append([str(q), ""])

        fin_df = pd.DataFrame(final_lst, columns=columns)
        return fin_df


if __name__ == '__main__':
    p = Question("What is a prot?", True)
    p2 = "What is a prit?"
    p3 = "What is a prut?"

    query3 = Question_holder([p])
    query3.set_question(p2, p.unique_id)
    query3.set_question(p3, p.unique_id)
    query3.set_question(p3, query3.questions[1].unique_id)
    a2 = "www.blabla.com"
    a3 = "www.blibli.com"
    p_q = p.unique_id
    A2 = Answer(a2, p_q)

    query3.ingest_new_answers({p2:[a2,a3]})


    got_q = query3.get_question(q_id=p.unique_id)
    got_q2 = query3.get_question(q_str=str(p2))
    pass
    print(got_q)
    my_df = query3.to_pandas()
    print(my_df)
