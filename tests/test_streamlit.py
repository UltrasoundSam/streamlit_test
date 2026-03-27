# tests/test_streamlit_app.py

from streamlit.testing.v1 import AppTest


def test_app_loads():
    """Ensure the app starts up cleanly and renders the title."""
    at = AppTest.from_file("main.py").run()

    assert at.session_state is not None
    print(at.text)

    # The page should render at least one widget (country selector)
    assert len(at.get("selectbox")) >= 1


def test_country_selector_present():
    """Ensure the selectbox for countries appears."""
    at = AppTest.from_file("main.py").run()

    select_boxes = at.get("selectbox")
    assert len(select_boxes) >= 1


def test_country_selection_works():
    at = AppTest.from_file("main.py").run()

    # Retrieve the first selectbox
    box = at.get("selectbox")[0]

    # Choose the first option
    first_country = box.options[0]
    box.select(first_country)
    at.run()

    # Validate the widget updated properly
    assert box.value == first_country


def test_results_are_rendered():
    """Ensure the results section shows some visualisation or text output."""
    at = AppTest.from_file("main.py").run()

    # Select a country
    box = at.get("selectbox")[0]
    box.select(box.options[0])
    at.run()

    # Now expect results to have been generated
    # We can't know exact text, but typical features will appear:
    assert len(at.get("plotly_chart")) >= 1 or "cases" in at.text.lower()
