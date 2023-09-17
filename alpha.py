# packages
import pandas as pd
import matplotlib.pyplot as plt

# local imports
from quant import *
from commons import *

def get_alpha(df, leverage):

    # ~~~~~~~~~~~~~ vars ~~~~~~~~~~~~
    # bond returns
    risk_free_df = pd.read_csv("data/3month.csv")
    risk_free_df['date'] = pd.to_datetime(risk_free_df['date'])
    risk_free_df.set_index('date', inplace=True)
    # benchmark returns
    benchmark_df = pd.read_csv("data/spx_2000.csv")
    benchmark_df = get_montly_returns(benchmark_df, "M")

    # ~~~~~~~~~~ get strategy return ~~~~~~~~~~~
    #df = pd.read_json("data/backtesting_json/momentum.json")

    # filter by spx data
    #df = filterBy(df, 'symbol', ["XLP"])
    #df = filterBy(df, 'symbol', ["NAS100_USD"])
    #df = filterBy(df, 'symbol', ["QQQ"])
    #df = df[(df['dateD'] >= "2005-01-01")]
    #df = filterBy(df, 'symbol', ["XLP", "XLF", "XLRE", "XLY", "XLK", "XLU", "XLV", "XME", "KRE"])
    #df = filterBy(df, 'symbol', ["AAPL", "MSFT", "AMZN", "META", "GOOG", "ADBE", "BAC"])
    #df = filterBy(df, 'commodity', ["forex"])
    # df = filterBy(df, 'symbol', ['AUD_CAD', 'AUD_CHF', 'AUD_JPY', 'AUD_NZD', 'AUD_USD', 'CAD_JPY',
    #                     'CAD_CHF', 'CHF_JPY', 'EUR_AUD', 'EUR_CAD', 'EUR_CHF', 'EUR_GBP',
    #                     'EUR_NZD', 'EUR_JPY', 'EUR_USD', 'GBP_AUD', 'GBP_CAD', 'GBP_CHF',
    #                     'GBP_JPY', 'GBP_NZD', 'GBP_USD', 'NZD_CAD', 'NZD_CHF', 'NZD_JPY',
    #                     'NZD_USD', 'USD_CAD', 'USD_CHF'])

    df.profit *= leverage

    # filter by patterns --------> here you can switch to long and short strategy
    # long_patterns = ["gartley", "cypher", "anti_shark", "anti_butterfly"]
    # short_patterns = ["anti_gartley", "anti_nenstar", "anti_shark", "bat", "deep_crab", "shark"]
    # df = df[
    #     ((df['side'] == 'long') & (df['pattern'].isin(long_patterns))) |
    #     ((df['side'] == 'short') & (df['pattern'].isin(short_patterns)))
    # ]

    # aggregate by month
    #df['dateD'] = pd.to_datetime(df['dateD'])
    #df.set_index('dateD', inplace=True)
    #print(df)
    df = df.resample('M').sum()

    # filter by date, profit, pattern
    df = df[['profit']]

    df['cumulative_gain'] = df['profit'].cumsum()
    df['prod_gain'] = (1 + df['profit']).cumprod()

    # plt.plot(df.cumulative_gain)
    # #plt.plot(df.prod_gain)
    # plt.show()

    # alpha
    alpha_list = []
    alpha_dict = {}
    # sharpe
    sharpe_list = []
    sharpe_dict = {}

    # get year of df
    lowest_year = max(benchmark_df.date[0].year, df.index[0].year)
    highest_year = min(benchmark_df.date[-1].year,  df.index[-1].year)

    for i in range(lowest_year + 1, highest_year):
        #print(i)
        # ~~~~~~~~~~ beta ~~~~~~~~~
        # get monthly returns
        benchmark_returns_monthly = benchmark_df[benchmark_df.index.year == i].resample('M').sum()['return']
        strat_returns_monthly = df[df.index.year == i].resample('M').sum()['profit']
        #strat_returns_monthly = df[df.index.year == i].resample('M').prod()['profit']
        Bi = get_beta(benchmark_returns_monthly, strat_returns_monthly)
        #print("Bi: ", Bi)

        # ~~~~~~~~~~ alpha ~~~~~~~~~~~~
        # strategy return for the year
        strat_yearly_returns = df[df.index.year == i]
        Ri = (strat_yearly_returns['profit']).sum()
        #print("Ri: ",Ri)
        #print(Ri)

        # risk free return
        Rf_series = risk_free_df[risk_free_df.index.year == i]['value']
        Rf =  risk_free_df[risk_free_df.index.year == i]['value'][0]
        #print("Rf: ", Rf)

        # benchmark return
        bench_yearly_returns = benchmark_df[benchmark_df.index.year == i]
        #print(bench_yearly_returns)
        Rm = (bench_yearly_returns['return'] + 1).prod() - 1
        #print("Rm: ", Rm)

        # alpha
        alpha = Ri - Rf - Bi * (Rm - Rf)

        #print("alpha: ", alpha)

        alpha_list.append(alpha)
        alpha_dict[i] = alpha


        # ~~~~~~~~~~~ sharpe ratio ~~~~~~~~~~~
        Ri_mean = np.mean(strat_returns_monthly)
        # risk free rate
        monthly_rate = (pow(1 + Rf, 1/12) - 1)
        #print(strat_returns_monthly)
        #print(Rf_series)
        excess_return = strat_returns_monthly.values - monthly_rate
        #print(excess_return)
        excess_return_mean = np.mean(excess_return)
        #print(excess_return_mean)
        excess_return_std = np.std(excess_return)
        #rint(excess_return_std)
        sharpe = excess_return_mean / excess_return_std
        # print(excess_return_std)
        # print("ri: ", Ri)
        # print("rf: ", Rf)

        sharpe_list.append(sharpe)
        sharpe_dict[i] = sharpe


    # plt.plot(df.index, df['cumulative_gain']*100)
    # #plt.plot(df.index, df['prod_gain'])

    # plt.show()



    #print(df)

    # print(alpha_list)
    # print(np.mean(alpha_list))

    return np.mean(alpha_list), alpha_dict, np.mean(sharpe_list), sharpe_dict

# def main(df):
#     alphas = {}

#     #for leverage in range(1,30):
#     for leverage in range(1,30):
#         alphas[leverage] = get_alpha(df, leverage)

#     print(alphas)

#     plt.plot(alphas.keys(), alphas.values())
#     plt.show()


# if __name__ == "__main__":

#     df = pd.read_json("data/backtesting_json/5m_ml.json")

#     main(df)
