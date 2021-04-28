## this module allows to run the main_function on streamlit

from main import main_get_questions, main_get_answers
from src import Question_holder
import streamlit as st
import time
import base64

st.title(" no answer tool v 0.1 alpha")
"""
Welcome to the "No answer tool"

This tool explores Google to check which have no defined answer

Input your question or keyword below and let the tool do the rest
"""


@st.cache(allow_output_mutation=True)
def create_flow_control(n):
    """returns a list for flow control. The list can be mutated outside
    the function and will remain in memory"""
    return [False] * n


@st.cache(allow_output_mutation=True)
def streamlit_get_ppa(user_input, **kwargs):
    """returns query with ppa questions from google
    using DataForSEO api
    Parameters:
    user_input: str user_input

    Returns Question-holder object"""
    query = main_get_questions(user_input, **kwargs)
    return query


# TODO: remove unwanted questons does not behave properly
@st.cache(allow_output_mutation=True)
def streamlit_get_answers(query, keep_qs, **kwargs):
    """get answers only for selected questions
    Parameters:
    query: Question Holder object
    keep_qs: Questions to keep"""
    print("before removing", len(query.questions))
    query.remove_unwanted_questions(keep_qs, "k")
    print("after removing", len(query.questions))
    print(str(query))
    return main_get_answers(query, **kwargs)


def get_table_download_link(df) -> str:
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href


def streamlit_main():
    """main function to create a streamlit GUI"""
    flow_control = create_flow_control(5)
    credentials=[st.secrets['uname'], st.secrets['pw']]

    if st.button("Press to Start") and not any(flow_control):
        flow_control[0] = True
        st.text(str(flow_control[0]))

    # get user input
    if flow_control[0]:
        st.markdown("""## step1. please enter your question or keyword(s).    
        __Notes__:    
        * Questions should be of more than 4 words and ending with a '?'    
        * Keywords can be any number of words, divided by a space    
        """)
        user_input = st.text_input("Enter a question or keywords", "")
        if st.button("Confirm") or user_input:
            flow_control[1] = True
    # search for People also Ask questions
    if flow_control[1]:
        st.warning("Downloading most relevant questions from Google.\n This can take up to 1 minute")
        query = streamlit_get_ppa(user_input, credentials=credentials)
        question_list = query.to_list("q")
        if question_list:
            st.success("All question retrieved")
            st.write(question_list)
            flow_control[2] = True
    # filter questions
    if flow_control[2]:
        st.markdown("""## Step 2. Filter your questions. 
        Choose which questions are appropriate to your query. 
        Notes:
        * Please drag the questions that you want to include in the box
        * The more questions you choose the more time you need to wait    
        """)
        # question_list=query.to_list()

        keep_qs = st.multiselect("Choose the relevant questions", question_list)
        st.write('You selected:', keep_qs)
        # breakpoint()
        if st.button("confirm selected questions"):
            flow_control[3] = True

    # download answers
    if flow_control[3]:
        st.warning("Downloading most relevant answers from Google.\n This can take up to 1 minute")
        query = streamlit_get_answers(query, keep_qs)
        if query:
            flow_control[4] = True

    # display table with results and allow downloading
    if flow_control[4]:
        st.success("Your data is ready")
        final_df = query.to_pandas()
        st.dataframe(final_df)  # TODO repair this
        st.write(get_table_download_link(final_df), unsafe_allow_html=True)


if __name__ == '__main__':
    streamlit_main()
