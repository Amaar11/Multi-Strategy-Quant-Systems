import numpy as np
import pandas as pd

def get_backtest_day_stats(portfolio_df, instruments, date, date_prev, date_idx, historical_data):
    pnl = 0
    nominal_ret = 0

    for inst in instruments:
        previous_holdings = portfolio_df.lox[date_idx - 1,"{} units".format(inst)]
        if previous_holdings !=0:
            price_change = historical_data.loc["{} close". format(inst)] - historical_data.loc[
            date_prev, "{} close".format(inst)]
            dollar_change = price_change * 1
            inst_pnl = dollar_change * previous_holdings
            pnl += inst_pnl
            nominal_ret += portfolio_df.loc[date_idx - 1, "{} w".format(inst)] * historical_data.loc[date, "{} % ret".format(inst)]

    capital_ret = nominal_ret * portfolio_df.loc[date_idx - 1, "leverage"]
    portfolio_df.loc[date_idx, "capital"] = portfolio_df.loc[date_idx - 1, "capital"] + pnl
    portfolio_df.loc[date_idx, "daily pnl"] = pnl
    portfolio_df.loc[date_idx, "nominal ret"] = nominal_ret
    portfolio_df.loc[date_idx, "capital ret"] = capital_ret
    return pnl, capital_ret

def get_strat_scaler(portfolio_df, lookback, vol_target, idx, default):
    capital_ret_history = portfolio_df.loc[:idx].dropna().tail(lookback)["capital ret"]
    strat_scaler_hitory = portfolio_df.loc[:idx].dropna().tail(lookback)["strat scalar"]
    if len(capital_ret_history) == lookback:
        annualized_vol =capital_ret_history.std() * np.sqrt(253)
        scalar_hist_avg = np.mean(strat_scaler_hitory)
        strat_scalar = scalar_hist_avg * vol_target / annualized_vol
        return strat_scalar
    else:
        return default
 

