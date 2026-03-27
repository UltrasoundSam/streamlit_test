import streamlit as st
import os

from analysis.data_loader import load_data
from analysis.covid_analysis import COVIDAnalysis, COUNTRIES
from analysis.constants import COUNTRIES
from layout.main_layout import render_country_selector, render_results, render_context


DATA_PATH = os.path.join('data', 'WHO-COVID-19-global-daily-data.csv')

# Define page style - must be first streamlit command
st.set_page_config(
    page_title="COVID Data Explorer",
    page_icon="📈"  #, layout="wide"
)

st.title('Processing COVID Data')

@st.cache_data
def cached_load():
    ''' Read in data from file and clean up missing data
    '''
    return load_data(DATA_PATH)

def main():
    # Render context info
    render_context(os.path.join("layout", "intro.md"))

    # Read in Data
    data = cached_load()

    # Select Country
    country = render_country_selector(COUNTRIES.keys())

    # Create Analysis object
    analysis = COVIDAnalysis(country)
    analysis.load_data(data)
    analysis.fit_data(initial_guess=None)

    # Create visualisations
    render_results(analysis, country)

    if st.checkbox('Show raw data'):
        st.write(data[data['country_code'] == COUNTRIES[country]])


if __name__ == "__main__":
    main()
