
import warnings
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

plt.style.use('dark_background')
#plt.style.use('bmh')

# removing warnings
# Filter out the specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# plot function
import mplfinance as mpf
binance_dark = {
    "base_mpl_style": "dark_background",
    "marketcolors": {
        "candle": {"up": "#3dc985", "down": "#ef4f60"},
        "edge": {"up": "#3dc985", "down": "#ef4f60"},
        "wick": {"up": "#3dc985", "down": "#ef4f60"},
        "ohlc": {"up": "green", "down": "red"},
        "volume": {"up": "#247252", "down": "#82333f"},
        "vcedge": {"up": "green", "down": "red"},
        "vcdopcod": False,
        "alpha": 1,
    },
    "mavcolors": ("#ad7739", "#a63ab2", "#62b8ba"),
    "facecolor": "#1b1f24",
    "gridcolor": "#2c2e31",
    "gridstyle": "--",
    "y_on_right": True,
    "rc": {
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.edgecolor": "#474d56",
        "axes.titlecolor": "red",
        "figure.facecolor": "#161a1e",
        "figure.titlesize": "x-large",
        "figure.titleweight": "semibold",
    },
    "base_mpf_style": "binance-dark",
}




def plot_candlestick_and_marker(df, pattern, symbol, pattern_type):
    # # Convert the 'Date' column to a pandas DatetimeIndex
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    #mpf.plot(df, type='candle', style=binance_dark, title='OHLC Plot', ylabel='Price')

    # Add annotations at index 4 and index 5
    # annotations = [
    #     dict(x= pattern["dates"][0], y=pattern["prices"][0], text='Annotation at index 4', fontsize=12, color='red'),
    #     dict(x= pattern["dates"][1], y=pattern["prices"][1], text='Annotation at index 5', fontsize=12, color='green')
    # ]
    # two_points  = [(pattern["dates"][0],pattern["prices"][0]),(pattern["dates"][1],pattern["prices"][1])]

    mpf.plot(df, type='candle', style=binance_dark, title=f'Sample Harmonic Pattern: {symbol} - {pattern_type.capitalize()}', ylabel='Price',
             alines=dict(alines=pattern, colors = ["b"]),
             volume=True)

def harmonic_plot(filtered_df, ohlc_df):
    # print patterns
    counter = 0
    for index, pattern in filtered_df.iterrows():



        if pattern["symbol"] != "AAPL":
            continue

        # counter
        if counter == 20:
            break
        else:
            counter += 1

        print(f"the date at index {pattern.indexA} is {pattern.dateA}")
#         date_value = ohlc_df.loc[pattern.indexA, 'date']
#         print(f"the data at index {pattern.indexA} is {date_value}")

        h_pattern = [(pattern.dateX, pattern.priceX),
                     (pattern.dateA, pattern.priceA),
                     (pattern.dateB, pattern.priceB),
                     (pattern.dateC, pattern.priceC),
                     (pattern.dateD, pattern.priceD),
                     (pattern.dateB, pattern.priceB),
                     (pattern.dateX, pattern.priceX)
                     ]
        harmonic_pattern = {
            "index": [pattern.indexX, pattern.indexA, pattern.indexB,
                     pattern.indexC, pattern.indexD],
            "dates": [pattern.dateX, pattern.dateA, pattern.dateB,
                     pattern.dateC, pattern.dateD],
            "prices": [pattern.priceX, pattern.priceA, pattern.priceB,
                     pattern.priceC, pattern.priceD]
        }
        # filter the df to around the pattern
        delta = harmonic_pattern["index"][4] - harmonic_pattern["index"][0]
        start_idx = round(harmonic_pattern["index"][0] - delta/4)
        end_idx = round(harmonic_pattern["index"][4] + delta/4)

        #print(start_idx)
        #print(end_idx)
        sliced_df = ohlc_df.iloc[start_idx:end_idx + 1]

        #print(sliced_df)

        # get the patterns with same symbol
        plot_candlestick_and_marker(sliced_df, h_pattern, pattern["symbol"], pattern["pattern"])  # Call the main function if this script is run directly




def plot_alpha(alpha_list):

    # turn values into percentages
    # for key in alpha_list:
    #     alpha_list[key] *= 100

    plt.bar(alpha_list.keys(), alpha_list.values())
    #plt.hist(alpha_list.values(), bins=len(alpha_list), alpha=0.7, color='blue', edgecolor='black')
    plt.xlabel('Date')
    plt.ylabel('Strategy Return (%)')
    plt.title("Annual Strategy Returns")

    # set percentage
    plt.gca().set_yticklabels([f'{x:.0%}' for x in plt.gca().get_yticks()])

    plt.show()

def plot_number_of_trades(df):
    # ~~~~~~~~ histogram
    # Create a histogram by grouping trades by 1-week intervals

    # Resample the DataFrame to 1-month intervals and count the rows in each month
    monthly_counts = df.resample('Y').count()
    monthly_counts.index = monthly_counts.index.to_period('Y').year

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    monthly_counts.commodity.plot(kind='bar', width=1.0, align='edge')
    plt.xlabel('Date (Year)')
    plt.ylabel('Number of Trades')
    plt.title('Frequency of Trades per Year')
    plt.xticks(range(len(monthly_counts.index)), monthly_counts.index, rotation=45)
    plt.tight_layout()
    plt.show()
    #~~~~~~~~~

def plot_benchmark(strategy, benchmark):

    plt.plot(strategy.index, strategy.values, label = "Strategy Returns")
    plt.plot(benchmark.index, benchmark.values, label = "S&P 500 Returns")

    plt.legend()
    plt.ylabel('Percentage Gain')
    plt.xlabel('Time')
    plt.title('Strategy Returns vs S&P 500 Returns')

    # set to percentage
    plt.gca().set_yticklabels([f'{x:.0%}' for x in plt.gca().get_yticks()])

    plt.show()
