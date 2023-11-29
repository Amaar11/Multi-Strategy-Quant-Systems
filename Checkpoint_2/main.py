import json
import pandas as pd

from dateutil.relativedelta import relativedelta

import quantlib.data_utils as du
import quantlib.general_utils as gu
from subsystems.LBMOM.subsys import Lbmom 

df, instruments = gu.load_file("./data.obj")
print(df, instruments)

VOL_TARGET = 0.20
print(df.index[-1]) #date today: 2023-10-26
sim_strat = df.index[-1] - relativedelta(years=5)
print(sim_strat) #start trading backtest 2018-10-26

strat = Lbmom(instruments_config="./subsystems/LBMOM/config.json", historical_df=df,simulation_start=sim_strat, vol_target=VOL_TARGET)
strat.get_subsys_pos()
