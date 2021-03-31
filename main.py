#   /********************************************************************************
#   * Copyright © 2021-2022, Matteo Jucker Riva
#   * All rights reserved. This program and the accompanying materials

#   * Contributors:
#   *     Matteo Jucker Riva, Ph.D.
#   *******************************************************************************/
from src.data import get_question
from src.data import generate_automatic_questions
from pathlib import Path
# Main script to run the no_answer_tool
def main():
    q = get_question()
    gen_qs = generate_automatic_questions(q.keywords, Path("references", "words_for_questions.csv"))
    q.related_questions += gen_qs
    print(q.related_questions)
    pass
if __name__ == '__main__':
    main()