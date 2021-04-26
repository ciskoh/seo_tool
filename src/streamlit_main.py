## this module allows to run the main_function on streamlit

from main import main
import streamlit as st
"""
# no answer tool v 0.1 alpha

*elcome to the "No answer tool"

This tool explores Google to check which have no defined answer

Input your question or keyword below and let the tool do the rest
"""

"""## step1. please enter your question or keyword(s)!    
__Notes__:    
* Questions should be of more than 4 words and ending with a '?'    
* Keywords can be any number of words, divided by a ','    """

user_input = st.text_input("Enter a question or keywords", "-999" )
if user_input != "-999":
    main(user_input)
