import json
import numpy as np
import pandas as pd
import quantlib.indicators_cal as indicators_cal
import quantlib.backtest_utils as backtest_utils


class Lbmom:

    def __init__(self,instruments_config, historical_df, simulation_start, vol_target ):
        self.pairs = [(185, 187), (94, 276), (55, 253), (36, 113), (127, 133), (65, 185), (62, 234), (149, 247), (263, 293), (113, 245), (200, 238), (27, 218), (260, 280), (69, 142), (161, 297), (219, 296), (95, 107), (19, 183), (180, 248), (40, 200), (189, 194)]
        self.historical_df = historical_df
        self.simulation_start = simulation_start
        self.vol_target = vol_target
        with open(instruments_config) as f:
            self.instruments_config = json.load(f)
        self.sysname = "LBMOM,"


    def extend_historicals(self, instruments, historical_data):
        for inst in instruments:
            historical_data["{} adx".format(inst)] = indicators_cal.adx_series(
                high=historical_data["{} high".format(inst)],
                low=historical_data["{} low".format(inst)],
                close=historical_data["{} close".format(inst)],
                n=14
            )
            for pair in self.pairs:
                historical_data["{} ema{}".format(inst, str(pair))] = indicators_cal.ema_series(historical_data["{} close".format(inst)], n=pair[0]) - \
                indicators_cal.ema_series(historical_data["{} close".format(inst)], n=pair[1])

        return historical_data

    def run_simulation(self, historical_data):
        """
        init params
        """
        instruments = self.instruments_config["instruments"]

        """
        pre-procesing
        """
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

            nominal_total = 0
            for inst in tradable:
                votes = [1 if (historical_data.loc[date, "{} ema{}".format(inst, str(pair))]>0) else 0 for pair in self.pairs]
               # print(votes)
                forecast = np.sum(votes)/len(votes)
                forecast = 0 if historical_data.loc[date, "{} adx".format(inst)]<25 else forecast

                position_vol_target = (1/len(tradable)) * portfolio_df.loc[i,"capital"] * self.vol_target / np.sqrt(253)
                inst_price = historical_data.loc[date, "{} close".format(inst)]
                percent_ret_vol = historical_data.loc[date, "{} % ret vol".format(inst)] if historical_data.loc[:date].tail(20)["{} active".format(inst)].all() else 0.025
                dollar_volatility = inst_price *percent_ret_vol
                position =strat_scalar * forecast * position_vol_target /dollar_volatility
                portfolio_df.loc[i, "{} units".format(inst)] = position
                #print(inst, position, forecast)
                nominal_total += abs(position*inst_price)

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
            print(portfolio_df.loc[i])

        portfolio_df.to_excel("lbmom.xlsx")

        return portfolio_df, instruments



    def get_subsys_pos(self):
        self.run_simulation(historical_data=self.historical_df) 
        portfolio_df, instruments = self.run_simulation(historical_data=self.historical_df)