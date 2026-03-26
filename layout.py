import streamlit as st
from collections.abc import Iterable


def render_country_selector(countries: Iterable[str]) -> st.selectbox:
    '''Creates the dropdown list for the country selector
    '''
    st.subheader('Select Country')

    # Create dropdown select box with countries sorted
    return st.selectbox('What Country would you like to explore?',
                        sorted(countries))