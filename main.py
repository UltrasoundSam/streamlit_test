import streamlit as st
import pandas as pd
import numpy as np
import os

from analysis import COVIDAnalysis


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
                           ("Italy",
                            "United Kingdom of Great Britain and Northern Ireland",
                            "Morocco"))
    st.write("You selected:", country)

    # Create Analysis object
    analysis = COVIDAnalysis(country)
    analysis.load_data(data)
    analysis.fit_data(initial_guess=None)
    fig, ax = analysis.visualise_cases()
    st.pyplot(fig)

    # hist_values = np.histogram(data[DATE_COLUMN].dt.hour,
    #                            bins=24,
    #                            range=(0,24))[0]
    # st.bar_chart(hist_values)

    # # Some number in the range 0-23
    # hour_to_filter = st.slider('hour', 0, 23, 17)
    # filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    # st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    # st.map(filtered_data)

if __name__ == "__main__":
    main()
