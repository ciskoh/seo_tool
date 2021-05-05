## this module allows to run the main_function on streamlit

from main import main_get_questions, main_get_answers
from src import Question_holder
from src.data import get_ppas_and_answers
import streamlit as st
import time
import base64

st.title(" no answer tool v 0.1 alpha")
"""
Welcome to the "No answer tool"

This tool explores Google to check which have no good answer available

Input your question or keyword below and let the tool do the rest

The tool will:
1. Search for questions using Googles 'People Also Ask'
2. Analyse the links in the result section to evaluate authority, relevance, and quality of each answer 
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

@st.cache(allow_output_mutation=True)
def streamlit_get_more_ppa(query, **kwargs):
    new_qs=get_ppas_and_answers([str(q) for q in query.questions], **kwargs )


# TODO: remove unwanted questons does not behave properly
@st.cache(allow_output_mutation=True)
def streamlit_get_answers(query,  **kwargs):
    """get answers only for selected questions
    Parameters:
    query: Question Holder object
    keep_qs: Questions to keep"""
    query = main_get_answers(query, **kwargs)
    return query


def get_table_download_link(df) -> str:
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download spreadsheet in csv format</a>'
    return href


def streamlit_main():
    """main function to create a streamlit GUI"""
    flow_control = create_flow_control(6)
    credentials=[st.secrets['uname'], st.secrets['pw']]
    if st.button("Press to Start") and not any(flow_control):
        flow_control[0] = True

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
        st.warning("Downloading most relevant questions from Google.\n This can take up to 2 minute")
        query = streamlit_get_ppa(user_input, credentials=credentials)
        question_list = query.to_list("q")
        if question_list:
            st.success("All question retrieved")
            st.write(question_list)
            flow_control[2] = True
    # get more questions?
    if flow_control[2]:
        st.markdown("""## Step 2. Get your answers""")

        more = st.checkbox("Fetch more questions?")
        if st.button("confirm"):
            flow_control[3] = True
            if more:
                st.warning("Searching for more questions, be patient!")
                query=streamlit_get_more_ppa(query, credentials=credentials)
                st.success("New questions retrieved")
                st.write(question_list)

    # download answers
    if flow_control[3]:
        st.warning("Downloading most relevant answers from Google.\n This can take up to 1 minute")
        query = streamlit_get_answers(query, credentials=credentials)
        if query:
            flow_control[4] = True

    # display table with results and allow downloading
    if flow_control[4]:
        st.success("Your data is ready")
        final_df = query.to_pandas()
        st.dataframe(final_df)  # TODO repair this
        st.write(get_table_download_link(final_df), unsafe_allow_html=True)
        flow_control[5]=True

    if flow_control[5]:
        st.markdown("""##Step 3. Get metrics""")
        st.warning("metrics not implemented yet!")

        reboot = st.button("Restart with new query")
        if reboot:
            flow_control = None


if __name__ == '__main__':
    streamlit_main()
