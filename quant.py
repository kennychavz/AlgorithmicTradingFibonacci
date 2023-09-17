import numpy as np

def get_beta(benchmark_returns, strategy_returns):

    # print(benchmark_returns)
    # print(strategy_returns)
    # input()

    covariance = np.cov(strategy_returns, benchmark_returns)[0, 1]

    variance = np.var(benchmark_returns)

    # Calculate beta
    beta = covariance / variance

    return float(beta)

def get_risk_free_rate(df, year):
    pass

def get_max_drawdown(profits):
    profits_copy = profits.copy()
    profits_copy.reset_index(drop=True, inplace=True)
    min_profit = 0
    p1 = profits_copy.index[0]
    p2 = profits_copy.index[1]
    while (p2 < len(profits_copy)):

        if profits_copy[p2] > profits_copy[p1]:
            p1 = p2
            p2 += 1
            continue
        pnl = profits_copy[p2] - profits_copy[p1]
        if pnl < min_profit:
            min_profit = pnl
        p2 += 1

    # import matplotlib.pyplot as plt
    # plt.plot(profits)
    # plt.show()

    return min_profit
