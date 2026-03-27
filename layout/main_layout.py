import streamlit as st
from collections.abc import Iterable


from analysis.covid_analysis import COVIDAnalysis
from analysis.constants import DEFAULT_COUNTRY


def render_country_selector(countries: Iterable[str]) -> st.selectbox:
    """Creates the dropdown list for the country selector"""
    st.subheader("Select Country")

    sorted_countries = sorted(countries)

    # Create dropdown select box with countries sorted
    return st.selectbox(
        "What Country would you like to explore?",
        sorted_countries,
        index=sorted_countries.index(DEFAULT_COUNTRY),
    )


def render_results(analysis: COVIDAnalysis, country: str) -> None:
    # Have two columns
    col1, col2 = st.columns([3, 1])

    with col1:
        # Create interactive plot
        fig = analysis.visualise_cases_interactive()
        st.plotly_chart(fig)

    with col2:
        # Create textual info
        total_cases = analysis.optimum_params[0]
        msg = (
            f"Using this very basic analysis, we expect there to be a total"
            f" of {int(total_cases):,} cases of COVID in {country}"
        )

        # Add vertical spacing
        for _ in range(12):
            st.write("")

        st.write(msg)


def render_context(path) -> None:
    """Creates some markdown text to explain what is happening with
    the analysis, and what are the caveats and limitations with it.
    """
    with open(path, "r", encoding="utf-8") as fi:
        md_text = fi.read()

    st.markdown(md_text)
