# -*- coding: utf-8 -*-
# This module generates automatic questions using permutations\
# and basic lists of random words

from pathlib import Path
import csv
import os

def get_words_for_questions(path):
    """reads the word list in path and returns a list of question words"""
    assert os.path.exists(path), "list of question words not found!"
    with open(path) as f:
        reader = csv.reader(f)
        question_words = [ a[0].replace(" ", "") for a in list(reader)]
    return question_words

def generate_automatic_questions(kw_list, path):
    """generate automatic questions using list of words
     in references/words_for_questions
     Params
     kw_list: list = list of keywords to create questions with"""
    q_start = get_words_for_questions(path)
    # removes keywords if the are question words
    kw_list = [kw for kw in kw_list if kw not in q_start ]

    q_complete = [a + " " + " ".join(kw_list) + " ?" for a in q_start]
    return q_complete

if __name__ == '__main__':
    path = Path("..", "..", "references", "words_for_questions.csv")
    kw_list = [ "damselfish", "jellyfish"]
    q_list = generate_automatic_questions(kw_list, path)
    for q in q_list:
        print(q)