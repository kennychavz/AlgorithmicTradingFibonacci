import pandas as pd

from quant import *
from alpha import get_alpha

def metrics(df):
    # print("\n\nMetrics ~~~~~~~~~~~~~~~~~~~")
    metrics = {}
    sides = ['all', 'long', 'short']
    initial_balance = 100000

    # long vs short
    for side in sides:

        # where we store the row
        row = {}

        #filter by side
        if side == "long" or side == "short":
            print(side)
            side_df = df[df['side'] == side].copy()
            # print(f"\n{side}: ")
        else:
            side_df = df.copy()



        # cumulative gains
        side_df['gains'] = side_df['profit'].cumsum()

        # gains
        side_df['profit']
        # losses

        # profits to balnace gains
        side_df['profit_dollars'] = side_df['profit'] * initial_balance

        # number of trades
        # print(f"\tTotal number of trades: {len(side_df)}")

        # total profit
        total_profit = side_df.gains.iloc[-1]
        total_profit_dollars = total_profit * initial_balance
        # print(f"\tTotal Profits: {round(total_profit_dollars, 2)}$")
        # gross profit
        gross_profit = (side_df.profit[side_df.profit > 0].sum() * initial_balance)
        gross_loss = (side_df.profit[side_df.profit < 0].sum() * initial_balance)
        # average profit per trade
        avg_winning_profit = side_df[side_df['profit_dollars'] > 0].profit_dollars.mean()
        # print(f"\tAverage Winning Trade: {round(avg_winning_profit, 2)}$")
        # average loss per trade
        avg_losing_profit = side_df[side_df['profit_dollars'] < 0].profit_dollars.mean()
        # print(f"\tAverage Losing Trade: {round(avg_losing_profit, 2)}$")
        # largest winnign trade
        max_trade = max(side_df.profit_dollars)
        # print(f"\tMax Winning Trade: {round(max_trade, 2)}$")
        # largest losing trade
        min_trade = min(side_df.profit_dollars)
        # print(f"\tMax Losing Trade: {round(min_trade, 2)}$")

        # max drawdown
        max_drawdown = get_max_drawdown(side_df.gains) * 100
        # print(f"\tMax Drawdown: {round(max_drawdown, 2)}%")

        # alpha & sharpe
        alpha, alpha_list, sharpe, sharpe_list = get_alpha(side_df, 1)
        # print(f"\tAnnualized Alpha: {round(alpha * 100, 2)}%")
        # print(f"\tAnnualized Sharpe: {round(sharpe, 2)}")

        # annualized return
        # Calculate the number of years the investment has been held
        investment_duration_years = (side_df.index[-1] - side_df.index[0]).days / 362.25
        annualized_return = (total_profit / investment_duration_years) * 100
        # print(f"\tAnnualized Return: {round(annualized_return * 100, 2)}%")

        # average time between trades
        side_df['time_diff'] = pd.to_datetime(side_df.dateD).diff()
        trade_frequency = side_df['time_diff'].mean()
        # Extract days, hours, and minutes
        days = trade_frequency.days
        hours, remainder = divmod(trade_frequency.seconds, 3600)
        minutes = remainder // 60

        # Format the result as a string
        trade_frequency = f"{days}D-{hours}H-{minutes}M"


        # row
        row['Initial Balance'] = f"{format(initial_balance, ',')}$"
        row['Total Net Profit'] = f"{format(round(total_profit_dollars, 2), ',')}$"
        row['Gross Profit'] = f"{format(round(gross_profit, 2), ',')}$"
        row['Gross Loss'] = f"{format(round(gross_loss, 2), ',')}$"

        row['Return on Initial Capital'] = f"{format(round(total_profit * 100, 2), ',')}%"
        row['Sharpe Ratio'] = f"{round(sharpe, 2)}"
        row['Annualized Alpha'] = f"{format(round(alpha * 100, 2), ',')}%"
        row['Annualized Return'] = f"{format(round(annualized_return, 2), ',')}%"
        row['Max Drawdown'] = f"{format(round(max_drawdown, 2), ',')}%"
        row[""] = ""
        row['Number of Trades'] = f"{format(len(side_df), ',')}"
        row['Avg Winning Trade'] = f"{format(round(avg_winning_profit, 2), ',')}$"
        row['Avg Losing Trade'] = f"{format(round(avg_losing_profit, 2), ',')}$"
        row['Largest Winning Trade'] = f"{format(round(max_trade, 2), ',')}$"
        row['Largest Losing Trade'] = f"{format(round(min_trade, 2), ',')}$"
        row['Average Time Between Trades'] = trade_frequency

        # store the row
        metrics[f"{side.capitalize()} Trades"] = row

    metrics_df = pd.DataFrame.from_dict(metrics).round(2)
    # print(metrics_df)

    return metrics_df
