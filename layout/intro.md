Putting your data pre-processing and analysis pipelines into a class can help you apply consistent analysis to different datasets. This means you can easily analyse a new dataset by creating a new instance of a class. It also means that you can store relevant metadata as class attribute, meaning that the important context is also bundled with the data.

In this example, we'll use a fairly naïve curve fitting approach to try to predict what the case numbers would be on a given day. This is obviously a highly complicated problem, but we'll try keep it simple to see how we can use classes to break down our analysis into three distinct packages of work:

- Reading in data
- Performing analysis/curve fitting
- Predicting COVID case numbers at a given date

The parameters should be protected from modification and should only be changed by performing least-square curve fitting (c.f. [scipy curve fit](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)) - with the implementation hidden from the end users - they should just be able to call a sensibly named method to fit the data.

For the curve fitting, we will use the [Gompertz curve](https://en.wikipedia.org/wiki/Gompertz_function), which has been used for centuries in biology and actuary science to describe populations. Trying to model any form of human behaviour is incredibly difficult, so we will look at the start of the pandemic, before people got 'used' to the virus and in a short-enough timeframe that only (broadly) a single public health initiative was tried.

The Gompertz curve is described by the following equation:

$$ \Large f\left(t\right) = a e^{-be^{-ct}} $$

where $a$, $b$ and $c$ are all parameters that describe the shape of the curve.

I have included a couple of datafiles on the Moodle page, which I have obtained from the World Health Organisation (WHO), I've filtered the data and split it into different files. For the full original dataset, you can navigate to the [WHO website](https://data.who.int/dashboards/covid19/data).


The class should at least contain the following methods:

- ```load_data(filename: str)``` to load the data from a given csv file location
- ```fit_data(initial_guess: tuple[float, float, float])``` to fit the Gompertz curve to the data, with some initial guesses of the parameters a, b, c
- ```predict_cases(date: datetime)``` to predict the case numbers on a given date using the curve fit.

You can also store any relevant metainformation about the data as attributes to the class, as well as the parameters a, b, & c.

