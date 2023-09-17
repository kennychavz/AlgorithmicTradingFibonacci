import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def filterBySymbol(df, symbols):
    return df[df['symbol'].isin(symbols)]
def filterBy(df, column, elements):
    return df[df[column].isin(elements)]
def groupBy(df, column):
    return df.groupby([column])

def get_montly_returns(df, interval):
    """
    Given a dataframe, return a dataframe with column return
    that contains the monthly gains for that instrument
    """
    df['return'] = df['close'].pct_change()
    df = df.tail(len(df) - 1)

    # aggregate by month
    # Convert the 'Date' column to datetime format
    df.loc[:, 'date'] = pd.to_datetime(df['date'])

    # Set the 'Date' column as the index
    df.set_index('date', inplace=True)

    # Resample and sum the returns by month
    monthly_returns = df.resample(interval).sum()

    monthly_returns['date'] = monthly_returns.index

    #monthly_returns.reset_index(inplace = True)

    return monthly_returns

def get_specific_yearly_return(df, year):
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    yearly_df = df[(df.index.year == year)]
    return yearly_df

def get_specific_month_return(df, year, month):
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    monthly_df = df[(df.index.year == year) & (df.index.month == month)]
    return monthly_df

def get_trading_period(start_date, end_date):

    # Calculate the difference between the two dates
    delta = end_date - start_date

    # Calculate years and days
    years = delta.days // 365
    days_remaining = delta.days % 365

    # Calculate months and days within the remaining days
    months = days_remaining // 30
    remaining_days = days_remaining % 30

    # Print the result
    return f"{years}, {months}, {remaining_days}"
    #print(f"Years: {years}, Months: {months}, Days: {remaining_days}")
