#   /********************************************************************************
#   * Copyright © 2021-2022, Matteo Jucker Riva
#   * All rights reserved. This program and the accompanying materials

#   * Contributors:
#   *     Matteo Jucker Riva, Ph.D.
#   *******************************************************************************/
from src import Question, Answer, Question_holder
from src.data import get_question, generate_automatic_questions, get_ppas_and_answers
from pathlib import Path


# Main script to run the no_answer_tool
def main_get_questions(first_q=None, **kwargs):
    """main function retrieving automatically generated question and
    Google's PPA questions based on initial user input
    """
    # step 1 get input from user
    if isinstance(first_q, str):
        q = Question(first_q, True, None)
    elif isinstance(first_q, Question):
        q = first_q
    else:
        raise ValueError("cannot recognise user input")

    query = Question_holder([q])
    # step 2 generate automatic questions
    gen_qs = generate_automatic_questions(q.keywords, Path("references", "words_for_questions.csv"))
    # transform gen_qs into a list of Question objects
    # step 3 get people also ask questions
    ppas = get_ppas_and_answers(gen_qs, mode="ppa", **kwargs)['ppa']
    ppas_list=sum(ppas.values(), [])
    query.ingest_new_questions(ppas_list)
    return query

def main_get_answers(query, **kwargs):
    """downloads answers and adds them to the query"""
    # step4 get answers for all questions
    if not isinstance(query, Question_holder):
        print("main "+str(type(query)))
        raise ValueError(f"query object not recognized!")
    if not len(query.questions) >= 2:
        raise ValueError("no questions found in query")

    new_answers = get_ppas_and_answers([str(q) for q in query.questions], mode="link", **kwargs)['link']
    query.ingest_new_answers(new_answers)

    return query


if __name__ == '__main__':

    # store object for testing
    query = main_get_questions("what is a damselfish?")
    query = main_get_answers(query)
    test = query.to_pandas().to_dict()
    import pickle
    pickle.dump(query, open(Path("data", "test_query.p"), "wb"))
    pass
