import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from analysis.data_loader import load_data


# ── Fixtures ──────────────────────────────────────────────────────────────────

# A header row matching the real CSV structure
CSV_HEADER = "Date_reported,Country_code,Country,WHO_region,New_cases,Cumulative_cases,New_deaths,Cumulative_deaths\n"


@pytest.fixture
def valid_csv(tmp_path: Path) -> str:
    """A minimal well-formed CSV file, matching the real data structure."""
    content = (
        CSV_HEADER
        + "2020-01-04,GB,United Kingdom,EUR,100,1000,5,50\n"
        + "2020-01-05,GB,United Kingdom,EUR,200,1200,10,60\n"
    )
    file = tmp_path / "covid_cases.csv"
    file.write_text(content)
    return str(file)


@pytest.fixture
def csv_with_missing_values(tmp_path: Path) -> str:
    """Blank New_cases and New_deaths cells, as seen in the real dataset."""
    content = (
        CSV_HEADER
        + "2020-01-04,AI,Anguilla,AMR,,0,,0\n"
        + "2020-01-04,AZ,Azerbaijan,EUR,,0,,0\n"
        + "2020-01-04,BD,Bangladesh,SEAR,0,0,0,0\n"
    )
    file = tmp_path / "covid_cases_missing.csv"
    file.write_text(content)
    return str(file)


@pytest.fixture
def csv_with_mixed_case_columns(tmp_path: Path) -> str:
    """Column headers with uppercase letters — should all be lowercased."""
    content = (
        "Date_reported,COUNTRY_CODE,Country,WHO_region,New_cases,Cumulative_cases,New_deaths,Cumulative_deaths\n"
        + "2020-01-04,GB,United Kingdom,EUR,100,1000,5,50\n"
    )
    file = tmp_path / "covid_cases_mixed.csv"
    file.write_text(content)
    return str(file)


