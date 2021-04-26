#   /********************************************************************************
#   * Copyright © 2021-2022, Matteo Jucker Riva
#   * All rights reserved. This program and the accompanying materials

#   * Contributors:
#   *     Matteo Jucker Riva, Ph.D.
#   *******************************************************************************/
from src import Question, Answer, Question_holder
from src.data import get_question, generate_automatic_questions, get_ppas_and_answers
from pathlib import Path


def create_child_question_series(str_q_list, parent_q):
    final_q_list=[]
    for q in str_q_list:
        new_q = Question(q, False, parent_q)
        final_q_list.append(new_q)
    return final_q_list

# Main script to run the no_answer_tool
def main(first_q=None):
    # step 1 get input from user
    q = get_question()
    query = Question_holder([q])
    # step 2 generate automatic questions
    gen_qs = generate_automatic_questions(q.keywords, Path("references", "words_for_questions.csv"))
    # transform gen_qs into a list of Question objects
    query.ingest_new_questions(gen_qs)
    print(query)
    # step 3 get people also ask questions
    ppas = get_ppas_and_answers(query.questions, mode="ppa")['ppa']
    query.ingest_new_questions(ppas)

    # step4 get answers for all questions
    answers = get_ppas_and_answers(query.questions, mode="link")['link']
    print(query)

if __name__ == '__main__':
    # import json
    # temp_path = "data/raw/clean_results.json"
    # with open(temp_path, "r") as file:
    #     clean_res = json.load(file)
    # q=Question("what is a damselfish?", True)
    # query = Question_holder([q])
    # # step 2 generate automatic questions
    # gen_qs = generate_automatic_questions(q.keywords, Path("references", "words_for_questions.csv"))
    # # transform gen_qs into a list of Question objects
    # query.ingest_new_questions({str(q):gen_qs})
    # print(str(query))
    # ppas=clean_res["ppa"]
    # query.ingest_new_questions(ppas)
    # print(ppas)
    main()
