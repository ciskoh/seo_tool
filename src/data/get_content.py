"""module to get the content of identified links using
request and BF4 also with multi-threading"""

import sys

sys.path.append("..")
from src.classes import Question, Answer
import requests
from pathlib import Path


def check_inputs(question: Question) -> None:
    if len(question.answers) == 0:
        raise ValueError("question has no answers")


def launch_request(link: str):
    """use request to get the content of a link"""
    response = requests.get(url=link)
    if response.status == 200:
        return response
    else:
        raise ConnectionError("request status not ok")


def parse_response(response, **kwargs):
    """extract text and/or other elements from
    """
    pass


def get_answer(answer: Answer) -> Answer:
    """this takes an answer, scrapes the content of the link
    and returns the answer with the text as attributes
    Params:
    answer: Answer obj with text
    """
    response = launch_request(answer.link)
    text = parse_response(response)
    return text


def main(question: Question) -> Question:
    """ gets a question and scrapes all the answers
    using multithreading
    Parameters:
    question: Question object

    Returns Question object with scraped answers"""
    # checks
    check_inputs(question)
    # prepare list of answers

    # launch multi-threading
    test_question.answers[0]
    # get answers with get answer

    # close thread
    pass


if __name__ == '__main__':
    import pickle
    query = pickle.load(open(Path("..", "..", 'data', 'test_query.p'), "rb"))
    main(query.questions[0])