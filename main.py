#   /********************************************************************************
#   * Copyright © 2021-2022, Matteo Jucker Riva
#   * All rights reserved. This program and the accompanying materials

#   * Contributors:
#   *     Matteo Jucker Riva, Ph.D.
#   *******************************************************************************/
from src.data import get_question, generate_automatic_questions, get_ppas_and_answers
from pathlib import Path
# Main script to run the no_answer_tool
def main():
    # step 1 get input from user
    q = get_question()

    # step 2 generate automatic questions
    gen_qs = generate_automatic_questions(q.keywords, Path("references", "words_for_questions.csv"))
    q.related_questions += gen_qs
    print(q.related_questions)
    # step 3 get people also ask questions
    ppas = get_ppas_and_answers(q.related_questions, mode="ppa")['ppa']
    print(ppas)
    ppas_flattened =set([q for sublist in ppas for q in sublist])
    q.related_questions +=ppas_flattened
    answers = get_ppas_and_answers(q.related_questions, mode="link")['link']
    for x,a in zip(q.related_questions, answers):
        print("\n")
        print(x, ":")
        print("\n".join(a[:20]))



if __name__ == '__main__':
    main()