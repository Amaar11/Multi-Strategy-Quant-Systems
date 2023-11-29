import json
import numpy as np
import pandas as pd

from scpiy.stats import skew

import quantlib.indicators_cal as indicators_cal
import quantlib.backtest_utils as backtest_utils
import quantlib.general_utils as general_utils
import quantlib.diagnostics_utils as diagnostics_utils


class Skprm:

    def __init__(self,instruments_config, historical_df, simulation_start, vol_target, brokerage_used):
        self.historical_df = historical_df
        self.simulation_start = simulation_start
        self.vol_target = vol_target
        with open(instruments_config) as f:
            self.instruments_config = json.load(f)
        self.brokerage_used = brokerage_used
        self.sysname = "LSMOM,"


    def extend_historicals(self, instruments, historical_data):
        for data in historical_data.index:
            for inst in instruments:
                rolling_returns = historical_data.loc[:date].tail(68)["{} % ret".format(inst)]
                skewness = skew(rolling_returns)
                historical_data.loc[date, "{} skew", format(inst)] = skewness
        return historical_data

pass
    def run_simulation(self, historical_data, debug=False, use_disk=False):
        """
        init params + pre-processing
       """
        instruments = self.instruments_config["fx"] + self.instruments_config["indices"] + self.instruments_config["commodities"] \
           + self.instruments_config["metals"] + self.instruments_config["bonds"] self.instruments_config["crypto"] 
        
       
        if not use_disk:

            historical_data = self.extend_historicals(instruments=instruments, historical_data=historical_data)
            print(historical_data)
            #portfolio_df = pd.DataFrame(index=self.historical_data(self.simulation_start:).index).reset_index()
            portfolio_df = pd.DataFrame(index=self.historical_df[self.simulation_start:].index).reset_index()

            portfolio_df.loc[0,"capital"] = 10000
            is_halted = lambda inst, date: not np.isnan(historical_data.loc[date, "{} active".format(inst)]) and (~historical_data[:date].tail(3)["{} active".format(inst)]).any()
            print(portfolio_df)

            """
            run simulation
            """
            for i in portfolio_df.index:
                date = portfolio_df.loc[i, "date"]
                strat_scalar = 2

                tradable = [inst for inst in instruments if not is_halted(inst, date)]
                non_tradable = [inst for inst in instruments if inst not in tradable]

                """
                Get PnL, Scalars
                """
                if i !=0:
                    date_prev = portfolio_df.loc[i - 1, "date"]
                    pnl, nominal_ret = backtest_utils.get_backtest_day_stats(portfolio_df, instruments, date, date_prev, date_idx, historical_data)
                    strat_scalar = backtest_utils.get_strat_scaler(portfolio_df, lookback=100, vol_target=self.vol_target, idx=i, default=strat_scalar)

                portfolio_df.loc[i, "strat scalar"] = strat_scalar

                """
                Get Positions
                """
                for inst in non_tradable:
                    portfolio_df.loc[i, "{} units".format(inst)] = 0
                    portfolio_df.loc[i, "{} w".format(inst)] = 0

                skews = {}
                for inst in tradable:
                    skews[inst] = historical_data.loc[date, "{} skew".format(inst)]
                skew = {k:v for k,v in sorted(skews.items(), key=lambda pair:pair[1])}
                quantile_size = int(len(tradable) * 0.25)
                high_skewness = list(skews.keys())[-quantile_size:]
                low_skewness = list(skews.keys())[quantile_size:]

                nominal_total = 0
                for inst in tradable:
                    forecast = 0
                    forecast = 1 in inst in low_skewness else forecast
                    forecast = -1 if inst in high_skewness else forecast

                    position_vol_target = (1/len(tradable)) * portfolio_df.loc[i,"capital"] * self.vol_target / np.sqrt(253)
                    inst_price = historical_data.loc[date, "{} close".format(inst)]
                    percent_ret_vol = historical_data.loc[date, "{} % ret vol".format(inst)] if historical_data.loc[:date].tail(20)["{} active".format(inst)].all() else 0.025
                    dollar_volatility = inst_price *percent_ret_vol
                    position =strat_scalar * forecast * position_vol_target /dollar_volatility
                    portfolio_df.loc[i, "{} units".format(inst)] = position
                    #print(inst, position, forecast)
                    nominal_total += abs(position*inst_price)

                nominal_total = backtest_utils.set_leverage_cap(portfolio_df, instruments, date, i, nominal_total, 10, historical_data):
                for inst in tradable:
                    units = portfolio_df.loc[i, "{} units".format(inst)]
                    normal_inst = units * historical_data.loc[date, "{} close".format(inst)]
                    inst_v = normal_inst/nominal_total
                    portfolio_df.loc[i, "{} w".format(inst)] = inst_w



                """
                Perforom Calculations for Date
                """
                portfolio_df.loc[i, "nominal"] = nominal_total
                portfolio_df.loc[i, "levrage"] = nominal_total / portfolio_df.loc[i, "capital"]
                if debug: print(portfolio_df.loc[i])

            portfolio_df.set_index("date", inplace=True)
            diagnostics_utils.save_backtests(
                portfolio_df=portfolio_df, instruments=instruments, brokerage_used=self.brokerage_used, sysname=self.sysname
            )
        
            diagnostics_utils.save_diagnostics(
                portfolio_df=portfolio_df, instruments=instruments, brokerage_used=self.brokerage_used, sysname=self.sysname
            )
        else:
            portfolio_df = general_utils.load_file("./backtests/{}_{}.obj".format(self.brokerage_used, self.sysname))
    

        return portfolio_df, instruments



    def get_subsys_pos(self, debug, use_disk):
        portfolio_df, instruments = self.run_simulation(historical_data=self.historical_df, debug=debug, use_disk=use_disk)
        return portfolio_df, instruments 