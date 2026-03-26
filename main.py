import streamlit as st
import pandas as pd
import numpy as np
import os

from analysis import COVIDAnalysis, COUNTRIES


DATE_COLUMN = 'Date_reported'
DATA_PATH = os.path.join('.', 'WHO-COVID-19-global-daily-data.csv')

st.title('Processing COVID Data')

@st.cache_data
def load_data():
    ''' Read in data from file and clean up missing data
    '''
    data = pd.read_csv(DATA_PATH)

    # Sometimes if no new data to report, it is simply blank
    data = data.fillna(0)
    data['New_cases'] = data['New_cases'].astype(int)
    data['New_deaths'] = data['New_deaths'].astype(int)

    # Also want to convert Date into datetime object
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    # Convert all names to lowercase
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def main():
    # Read in Data
    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text("Done! (using st.cache_data)")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data.head(50))

    # Select Country
    st.subheader('Select Country')
    country = st.selectbox('What Country would you like to explore?',
                           COUNTRIES.keys())
    st.write("You selected:", country)

    # Create Analysis object
    analysis = COVIDAnalysis(country)
    analysis.load_data(data)
    analysis.fit_data(initial_guess=None)

    # Have two columns
    col1, col2 = st.columns([3, 1])

    with col1:
        # Create interactive plot
        fig = analysis.visualise_cases_interactive()
        st.plotly_chart(fig)

    with col2:
        # Create textual info
        total_cases = analysis.optimum_params[0]
        msg = f'Using this very basic analysis, we expect there to be a total of {int(total_cases):,} cases of COVID in {country}'

        for _ in range(12):
            st.write("")
        st.write(msg)


if __name__ == "__main__":
    main()
