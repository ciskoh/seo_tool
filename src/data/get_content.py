"""module to get the content of identified links using
request and beautiful soup also with multi-threading

ATM it updates the text attribute in Answer objects"""

import sys

sys.path.append("..")
from src.classes import Question, Answer
import requests
from pathlib import Path
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor


def check_inputs(question: Question) -> None:
    if len(question.answers) == 0:
        raise ValueError("question has no answers")


def launch_request(link: str):
    """use request to get the content of a link"""
    response = requests.get(url=link)
    if response.status_code == 200:
        return response
    else:
        raise ConnectionError("request status not ok")

# TODO: add filter to get main corpus?
def parse_text_in_response(response)->list:
    """extract text and/or other elements from
    response"""
    soup = bs(response.content, 'html.parser')
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text


def thread_function_wrapper(answer,):
    """this takes an answer, scrapes the content of the link
        and returns the answer with the text as attributes
        Params:
        answer: Answer obj with text
        """
    print("starting in-thread operations")
    try:
        response = launch_request(answer.link)
        text = parse_text_in_response(response)
    except ConnectionError:
        text = ""
    finally:
        answer.text = text
        return None

def main(question: Question) -> Question:
    """ gets a question and scrapes all the answers
    using multithreading
    Parameters:
    question: Question object

    Returns Question object with scraped answers"""
    # checks
    check_inputs(question)
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(thread_function_wrapper, list(question.answers))
    print("shit is done, YO!")


    # launch multi-threading with ThreadExecPool
    # get answers with get answer

    # close thread
    pass


if __name__ == '__main__':
    import pickle

    test_query = pickle.load(open(Path("..", "..", 'data', 'test_query.p'), "rb"))
    # low level process
    my_q = test_query.questions[4]
    my_a = list(my_q.answers)[1]
    print(my_q, my_a)
    # resp = launch_request(my_a.link)
    # text = parse_response(resp, test=True)
    main(my_q)

    pass
