import pandas as pd
import datetime
import numpy as np


def dates_range(samples, print_dates=False):
    # creates range of dates
    dates = pd.date_range(
        '14-08-2001', str(datetime.date.today()), periods=samples)
    for date in dates:
        if print_dates:
            print(date)
    return dates


def dataframes():
    # dataframes, similar to SQL tables
    dates = dates_range(3)
    df = pd.DataFrame(np.random.random((3, 3)), dates)
    # selecting columns in dataframe
    print(df[0:3])
    # print(df.describe())


def main():
    # dates_range()
    dataframes()


if __name__ == "__main__":
    main()
