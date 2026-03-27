import numpy as np
import numpy.typing as npt
import scipy.optimize as so
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from datetime import timezone
from typing import Optional

from analysis.constants import COUNTRIES


class COVIDAnalysis:
    def __init__(self, country_name: str) -> None:
        """Initialise object with country name"""
        self.__country = country_name

        # Want to know start and end date of data
        self.__start_date = dt.datetime(2020, 1, 1)
        self.__end_date = dt.datetime(2020, 6, 1)

        # Same with cases and dates
        self.__cases = None
        self.__dates = None

        # Optimum parameters
        self.__params = np.array(3 * [np.nan])

    def __repr__(self) -> str:
        """Returns friendly representation of object"""
        return f"COVIDAnalysis(country_name={self.country})"

    def __str__(self) -> str:
        """Returns friendly representation of object"""
        start = self.start_date.strftime("%d/%m/%y")
        end = self.end_date.strftime("%d/%m/%y")
        msg = f"COVID Data from {self.country} between {start} and {end}"
        return msg

    @property
    def country(self) -> str:
        """Return name of country"""
        return self.__country

    @country.setter
    def country(self, country_name: str, data: pd.DataFrame) -> None:
        """Changes the name of the country and reloads data"""
        self.__country = country_name
        self.load_data(data)

    @property
    def start_date(self) -> dt.datetime:
        """Returns first date of data"""
        if not self.__start_date:
            # No data imported yet so
            print("No data imported yet")

        return convert_to_datetime(self.__start_date)

    @property
    def end_date(self) -> dt.datetime:
        """Returns first date of data"""
        if not self.__end_date:
            # No data imported yet so
            print("No data imported yet")

        return convert_to_datetime(self.__end_date)

    @property
    def dates(self) -> None | npt.NDArray[np.datetime64]:
        """Returns tuple of date objects detailing dates that
        data was collected.
        """
        return self.__dates

    @property
    def cases(self) -> None | npt.NDArray[np.int64]:
        """Returns tuple of date objects detailing dates that
        data was collected.
        """
        return self.__cases

    @property
    def optimum_params(self) -> npt.NDArray[np.float32]:
        """Returns the optimum parameters found after
        curve fitting
        """
        return self.__params

    def load_data(self, total_data: pd.DataFrame) -> None:
        """Filters the data from the master dataframe to select
        only data from the relevant country name.

        Saves data to class attributes self.dates and self.cases

        Inputs:
            filename [str] - path to csv file containing data

        Returns:
            None - but updates self.cases, self.dates,
        """
        # Create filters
        country_name_filter = total_data["country_code"] == COUNTRIES[self.country]  # noqa: E501
        date_filter1 = total_data["date_reported"] > "2020-01-01"
        date_filter2 = total_data["date_reported"] < "2020-06-01"

        # Apply filters and assign to internal attributes
        self.__data = total_data[country_name_filter & date_filter1 & date_filter2]  # noqa: E501
        self.__cases = self.__data["cumulative_cases"].values
        self.__dates = self.__data["date_reported"].values

        # Define start and end date
        self.__start_date = self.__dates[0]
        self.__end_date = self.__dates[-1]

    def _gompertz(
        self, date: float | npt.NDArray[np.float64], a: float, b: float, c: float
    ) -> float | npt.NDArray[np.float64]:
        """Helper function defining gompertz curve in the form of
        a*e^-b^-ct.

        Inputs:
            date [float]        - Unix timestamp defining specific time
            a [float]           - Parameter of a in above curve
            b [float]           - Parameter of b in above curve
            c [float]           - Parameter of c in above curve

        Outputs:
            value [float]       - Gompertz curve evaluated at given date
        """
        return a * np.exp(-b * np.exp(-c * date))

    def fit_data(self, initial_guess: Optional[tuple[float, float, float]]) -> None:
        """Perform curve fit on data to find the optimum parameter
        for the Gompertz curve given the COVID data. Optional guesses
        for the parameter can be optionally given.

        Inputs:
            initial_guess       - Optional initial guess for parameters a, b, c
                                 as a tuple (a_guess, b_guess, c_guess)

        Returns:
            None - but updates self.params
        """
        # We currently have dates in terms of datetimes, let's convert it to
        # numerical value as days
        start_of_year = np.datetime64("2020-01-01 00:00:00.0")
        days = (self.dates - start_of_year) / np.timedelta64(1, "D")
        days += 1

        # Give default values if no initial values are given
        if not initial_guess:
            initial_guess = (1.0, 1.0, 1.0)

        # All the parameters should be strictly positive, so can define bounds
        # for curve fit
        bounds = ((0, 0, 0), (np.inf, np.inf, np.inf))

        # Now we can perform the curve fit
        try:
            covid_fit, covid_covariance = so.curve_fit(
                f=self._gompertz,
                xdata=days,
                ydata=self.cases,
                p0=initial_guess,
                bounds=bounds,
            )
        except RuntimeError:
            covid_fit = None

        # Update optimal params
        self.__params = covid_fit

    def predict_cases(
        self, dates: np.datetime64 | npt.NDArray[np.datetime64]
    ) -> float | npt.NDArray[np.float64]:
        """For a given date (or series of dates) it predicts what the expected
         number of cumulative COVID cases should be

        Inputs:
            dates [np.datimes] - A single datetime or collection of datetime
                                 objects to evaluate curve

        Returns:
            cum_cases [float]  - Cumulative number of cases at given dates
        """
        start_of_year = np.datetime64("2020-01-01 00:00:00.0")
        timestamps = (dates - start_of_year) / np.timedelta64(1, "D")
        timestamps += 1

        # Now dates are in numeric factor, we can pass it over to gompertz
        cum_cases = self._gompertz(timestamps, *self.optimum_params)
        return cum_cases

    def visualise_cases(self) -> tuple[plt.Figure, plt.Axes]:
        """Visualises case numbers on a graph showing the cumululative number.
        If the curve fit is available, it will plot the curve fit as well.

        Inputs:
            None

        Returns:
            fig [plt.figure]        - Figure object to modify layout
            ax [plt.axes]           - matplotlib axis with data
        """
        # Create figure
        fig, ax = plt.subplots(figsize=(15, 5))

        # Plot case numbers on there
        ax.plot(self.dates, self.cases / 1000.0, ".", label="Data")
        ax.set_ylabel("Cumulative COVID Case numbers (1000s)")
        ax.set_title(f"COVID Case numbers in {self.country}")

        # If params is not None, we've done a curve fit
        if self.optimum_params is not None:
            # Create predicted numbers
            predicted = self.predict_cases(self.dates)
            ax.plot(self.dates, predicted / 1000.0, "--", label="Predicted Numbers")

        ax.legend()
        return fig, ax

    def visualise_cases_interactive(self) -> go.Figure:
        """Creates an interactive version of the case numbers on a
        graph showing the cumululative number.

        If the curve fit is available, it will plot the curve fit as well.


        Inputs:
            None

        Returns:
            fig [go.Figure]     - Interactive Plotly graph object
        """
        fig = go.Figure()

        # Plot Case numbers
        fig.add_trace(
            go.Scatter(
                x=self.dates,
                y=self.cases / 1000,
                mode="markers",
                marker=dict(color="#1f77b4", size=6),
                name="Data",
            )
        )

        # If params is not None, we've done a curve fit
        if self.optimum_params is not None:
            # Create predicted numbers
            predicted = self.predict_cases(self.dates)
            fig.add_trace(
                go.Scatter(
                    x=self.dates,
                    y=predicted / 1000,
                    mode="lines",
                    line=dict(dash="dash", color="#ff7f0e", width=2),
                    name="Predicted Numbers",
                )
            )

        # Layout settings
        fig.update_layout(
            title=f"COVID Case numbers in {self.country}",
            yaxis_title="Cumulative COVID Case numbers (1000s)",
            xaxis_title="Date",
        )
        return fig


def convert_to_datetime(numpy_time: np.datetime64) -> dt.datetime:
    """Converts time from numpy datetime64 object to Python built-in
    datetime object"""
    UNIX_EPOCH = np.datetime64(0, "s")
    ONE_SECOND = np.datetime64(1, "s")
    seconds_since_epoch = (numpy_time - UNIX_EPOCH) / ONE_SECOND

    return dt.datetime.fromtimestamp(seconds_since_epoch, timezone.utc)
