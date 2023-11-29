import json
import pandas as pd

from dateutil.relativedelta import relativedelta

import quantlib.data_utils as du
import quantlib.general_utils as gu

from subsystems.LBMOM.subsys import Lbmom
from brokerage.oanda.oanda import Oanda

with open("config/auth_config.json", "r") as f:
    auth_config = json.load(f)

df, instruments = gu.save_file("./Data/data.obj")
print(df, instruments)

VOL_TARGET = 0.20
print(df.index[-1])
sim_start = df.index[-1] - relativedelta(years=5)

oanda = Oanda(auth_config=auth_config)

trade_client = oanda.get_trade_client()

instruments = trade_client.get_account_instruments()

#summary = trade_client.get_account_summary()
#print(json.dumps(summary, indent=2))
exit()

strat = Lbmom(instruments_config="./subsystems/LBMOM/config.json", historical_df=df, simulation_start=sim_start, vol_target=VOL_TARGET)
strat = get_subsys_pos()


"""
import random

pairs = []
while len(pairs) <=20:
    pair = random.sample(list(range(16, 300)), 2)
    if pair[0] == pair [1]: continue
    pairs.append((min(pair[0], pair[1]), max(pair[0], pair[1])))
print(pairs)
"""
