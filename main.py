import streamlit as st
import os

from analysis.data_loader import load_data
from analysis.covid_analysis import COVIDAnalysis, COUNTRIES
from layout.main_layout import render_country_selector, render_results


DATA_PATH = os.path.join('.', 'WHO-COVID-19-global-daily-data.csv')

st.title('Processing COVID Data')

@st.cache_data
def cached_load():
    ''' Read in data from file and clean up missing data
    '''
    return load_data(DATA_PATH)

def main():
    # Read in Data
    data = cached_load()

    if st.checkbox('Show raw data'):
        st.write(data.head(50))

    # Select Country
    country = render_country_selector(COUNTRIES.keys())
    st.write("You selected:", country)

    # Create Analysis object
    analysis = COVIDAnalysis(country)
    analysis.load_data(data)
    analysis.fit_data(initial_guess=None)

    # Create visualisations
    render_results(analysis, country)


if __name__ == "__main__":
    main()
