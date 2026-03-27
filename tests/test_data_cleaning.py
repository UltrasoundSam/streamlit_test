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


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestLoadDataReturnsCorrectStructure:
    """Check that the function returns a DataFrame with the expected shape."""

    def test_returns_a_dataframe(self, valid_csv: str) -> None:
        result = load_data(valid_csv)
        assert isinstance(result, pd.DataFrame)

    def test_returns_correct_number_of_rows(self, valid_csv: str) -> None:
        result = load_data(valid_csv)
        assert len(result) == 2

    def test_returns_all_eight_columns(self, valid_csv: str) -> None:
        result = load_data(valid_csv)
        assert len(result.columns) == 8

    def test_expected_columns_are_present(self, valid_csv: str) -> None:
        expected_columns = {
            'date_reported', 'country_code', 'country', 'who_region',
            'new_cases', 'cumulative_cases', 'new_deaths', 'cumulative_deaths'
        }
        result = load_data(valid_csv)
        assert expected_columns == set(result.columns)

    def test_columns_are_lowercased(self, csv_with_mixed_case_columns: str) -> None:
        result = load_data(csv_with_mixed_case_columns)
        for column in result.columns:
            assert column == column.lower(), f"Column '{column}' is not lowercase"


class TestLoadDataHandlesMissingValues:
    """Verify that blank cells are filled with 0 rather than left as NaN.

    In the real dataset, countries with no new activity simply have blank
    cells rather than an explicit 0 — load_data should normalise these.
    """

    def test_no_null_values_remain(self, csv_with_missing_values: str) -> None:
        result = load_data(csv_with_missing_values)
        assert not result.isnull().values.any()

    def test_missing_new_cases_filled_with_zero(self, csv_with_missing_values: str) -> None:
        # Anguilla and Azerbaijan both have blank New_cases in the fixture
        result = load_data(csv_with_missing_values)
        anguilla = result[result['country'] == 'Anguilla']
        assert anguilla['new_cases'].iloc[0] == 0

    def test_missing_new_deaths_filled_with_zero(self, csv_with_missing_values: str) -> None:
        result = load_data(csv_with_missing_values)
        azerbaijan = result[result['country'] == 'Azerbaijan']
        assert azerbaijan['new_deaths'].iloc[0] == 0

    def test_row_with_no_missing_values_is_unchanged(self, csv_with_missing_values: str) -> None:
        # Bangladesh has explicit 0s — fillna should not affect it
        result = load_data(csv_with_missing_values)
        bangladesh = result[result['country'] == 'Bangladesh']
        assert bangladesh['new_cases'].iloc[0] == 0
        assert bangladesh['new_deaths'].iloc[0] == 0


class TestLoadDataTypes:
    """Ensure columns are cast to the correct dtypes after loading."""

    def test_new_cases_is_integer(self, valid_csv: str) -> None:
        result = load_data(valid_csv)
        assert result['new_cases'].dtype == np.int64

    def test_new_deaths_is_integer(self, valid_csv: str) -> None:
        result = load_data(valid_csv)
        assert result['new_deaths'].dtype == np.int64

    def test_date_reported_is_datetime(self, valid_csv: str) -> None:
        result = load_data(valid_csv)
        assert pd.api.types.is_datetime64_any_dtype(result['date_reported'])

    def test_date_values_are_parsed_correctly(self, valid_csv: str) -> None:
        result = load_data(valid_csv)
        assert result['date_reported'].iloc[0] == pd.Timestamp("2020-01-04")


class TestLoadDataEdgeCases:
    """Test behaviour at the boundaries — empty files, bad paths, etc."""

    def test_raises_error_for_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_data("non_existent_file.csv")

    def test_empty_csv_returns_empty_dataframe(self, tmp_path: Path):
        file = tmp_path / "empty.csv"
        file.write_text(CSV_HEADER)
        result = load_data(str(file))
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
