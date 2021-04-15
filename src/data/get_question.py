# -*- coding: utf-8 -*-
# module that deals with the user providing question or keywords,
# initial NLP (tokenizing and stemming) and similar
from src import Question

def get_question():
    user_input = input("Enter question or keywords?")
    q = Question(user_input)
    return q

if __name__ == '__main__':
    pass