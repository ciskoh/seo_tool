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
def main():
    # step 1 get input from user
    q = get_question()
    query = Question_holder([q])
    # step 2 generate automatic questions
    gen_qs = generate_automatic_questions(q.keywords, Path("references", "words_for_questions.csv"))
    # transform gen_qs into a list of Question objects
    new_q_list= create_child_question_series(gen_qs,q)
    query.questions += new_q_list
    print(q.parent_questions)
    # step 3 get people also ask questions
    ppas = get_ppas_and_answers(query.questions, mode="ppa")['ppa']
    print(ppas)
    ppas_flattened =set([q for sublist in ppas for q in sublist])
    q.parent_questions +=ppas_flattened
    # step4 get answers for all questions
    answers = get_ppas_and_answers(q.parent_questions, mode="link")['link']
    for x,a in zip(q.parent_questions, answers):
        print("\n")
        print(x, ":")
        print("\n".join(a[:20]))

if __name__ == '__main__':
    main()