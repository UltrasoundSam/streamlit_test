import numpy as np
import datetime as dt

from analysis.covid_analysis import convert_to_datetime
from analysis.covid_analysis import COVIDAnalysis


def test_convert_to_datetime():
    dt64 = np.datetime64("2020-01-01T00:00:00.0")
    result = convert_to_datetime(dt64)

    assert isinstance(result, dt.datetime)
    assert result.year == 2020
    assert result.month == 1
    assert result.day == 1


def test_gompertz_computation():
    a = COVIDAnalysis("X")
    result = a._gompertz(1, 2, 3, 4)
    expected = 2 * np.exp(-3 * np.exp(-4))
    assert np.isclose(result, expected)
