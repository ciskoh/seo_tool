# -*- coding: utf-8 -*-
# module that deals with the user providing question or keywords,
# initial NLP (tokenizing and stemming) and similar
import re

class Question():
    raw_string = None
    keywords: list = None
    related_questions: list = []
    answers_link: list = None

    def __init__(self, raw_string):
        """initialises object and detects if raw_string is question or list of keywords"""
        self.raw_string = raw_string
        if len(self.raw_string.split(" ")) > 2 and ("?" in self.raw_string):
            print("you entered a question!")
            self.keywords = self.get_keywords_from_question()
            self.related_questions.append(raw_string)
        else:
            print("you entered keywords!")
            self.raw_string = re.sub("[\W]", ",", self.raw_string)
            self.keywords = [k for k in self.raw_string.split(",") if len(k) > 0]


    def get_keywords_from_question(self, raw_string):
        """ basic keyword retrieval from question
        """
        clean_input = re.sub("[^A-Za-z0-9\s]", "", raw_string).lower()
        Q0_tokens = clean_input.split(" ")  # TODO:  this can be improved with tokenizer
        lst2 = sorted(Q0_tokens, key=len, reverse=True)
        return lst2[:2]

def get_question():
    user_input = input("Enter question or keywords?")
    q = Question(user_input)
    return q

if __name__ == '__main__':
    pass