# libraries
import pandas as pd


# local imports
from alpha import get_alpha
from commons import *
from quant import *
from plotting import *
from metrics import metrics


def main():
    #df = pd.read_json("data/backtesting_json/momentum.json")
    filtered_df = pd.read_json("data/backtest.json")
    filtered_df = filtered_df.sort_values(by='date')
    filtered_df.set_index('date', inplace=True)
    # ~~~~~~~~~~~~~~ config ~~~~~~~~~~~~~~~~~~
    # print("~~~~~~~~~~~~~~~Config ~~~~~~~~~~~~~~~~~")
    # filter by stocks
    # print("Dataframe length: ", len(filtered_df))


    # portfolio exposition
    filtered_df['profit'] *= 0.05
    profit_df = filtered_df['profit'] # only expose 10% of portfolio
    print("profit df", profit_df)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~ metrics ~~~~~~~~~~
    # print("~~~~~~~~~~~~~~~ Metrics ~~~~~~~~~~~~~~~~")
    metrics_df = metrics(filtered_df)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # average time between trades
    filtered_df['time_diff'] = pd.to_datetime(filtered_df.dateD).diff()
    # print(filtered_df['time_diff'].mean())
    #input()


    # cumulative gain df
    cumulative_gain_df = profit_df.cumsum()
    cumulative_gain_df += 1
    cumulative_gain_df.index = pd.to_datetime(cumulative_gain_df.index)
    print("cumulative", cumulative_gain_df)

    # benchmark gains
    benchmark_df = pd.read_csv("data/hist_data/benchmarks/spx_2000.csv")
    benchmark_df.date = pd.to_datetime(benchmark_df.date)
    benchmark_df.set_index("date", inplace=True)

    # Calculate the cumulative product of the 'Price' column
    benchmark_df['return'] = (1 + benchmark_df['close'].pct_change()).cumprod().tail(len(benchmark_df - 1))
    print(benchmark_df)
    benchmark_gains = benchmark_df["return"]

    print(filtered_df)

    #print the unique values of trades of type x
    print(filtered_df.symbol.unique())

    # overall winrate
    winrate_overall =filtered_df['winLoss'].mean()
    # print("overall winrate: ", winrate_overall)

    # win rate by symbol
    winrate_symbols = filtered_df.groupby(['symbol'])['winLoss'].mean()
    print("winrate", winrate_symbols)

    # profit by symbol
    profit_symbols = filtered_df.groupby(['symbol'])['profit'].sum()
    print("profit", profit_symbols)

    # profit total
    pnl_total = filtered_df['profit'].sum()
    # print("pnl total", pnl_total)

    # profit by year
    strat_returns_yearly = profit_df.resample('Y').sum()
    print("strat returns yearly", strat_returns_yearly)

    # max drawdown
    max_drawdown = get_max_drawdown(cumulative_gain_df)
    # print("max drawdown", max_drawdown)

    # get alpha
    alpha, alpha_list = get_alpha(filtered_df, 1)
    # print("alpha", alpha)
    # print(alpha_list)

    # ~~~~~~~~~ plotting ~~~~~~~~~~~~~~~~
    plot_benchmark(cumulative_gain_df, benchmark_gains)
    plot_alpha(alpha_list)
    plot_number_of_trades(filtered_df)





if __name__ == "__main__":
    main()
