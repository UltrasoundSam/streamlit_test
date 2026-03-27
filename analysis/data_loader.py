import pandas as pd

DATE_COLUMN = "Date_reported"


def load_data(path: str) -> pd.DataFrame:
    """Read in data from file and clean up missing data"""
    data = pd.read_csv(path)

    # Sometimes if no new data to report, it is simply blank
    data = data.fillna(0)
    data["New_cases"] = data["New_cases"].astype(int)
    data["New_deaths"] = data["New_deaths"].astype(int)

    # Also want to convert Date into datetime object
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    # Convert all names to lowercase
    data.rename(lambda x: str(x).lower(), axis="columns", inplace=True)
    return data
