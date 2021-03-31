# imported function and classes for src/data

# Question class

from src.data.get_question import Question, get_question
from src.data.generate_automatic_questions import generate_automatic_questions

if __name__ == '__main__':
    q = Question("bla,bla")
    print(q.keywords)
