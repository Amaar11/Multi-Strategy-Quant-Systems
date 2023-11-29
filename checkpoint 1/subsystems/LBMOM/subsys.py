#[(185, 187), (94, 276), (55, 253), (36, 113), (127, 133), (65, 185), (62, 234), (149, 247), (263, 293), (113, 245),
# (200, 238), (27, 218), (260, 280), (69, 142), (161, 297), (219, 296), (95, 107), (19, 183), (180, 248), (40, 200), (189, 194)]

import json
import pandas as pd
import quantlib.indicators_cal as indicators_cal

class Lbmom:
    
    def __init__(self,instruments_config, historical_df, simulation_start, vol_target):
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
        portfolio_df = pd.DataFrame(index=historical_data[self.simulation_start:].index).reset_index()
        portfolio_df.loc[0,"capital"] = 10000
        print(portfolio_df)

        """
        run simulation
        """
        pass


    def get_subsys_pos(self):
        self.run_simulation(historical_data=self.historical_df)

