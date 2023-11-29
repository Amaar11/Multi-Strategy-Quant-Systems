import json
import pandas as pd

from dateutil.relativedelta import relativedelta

import quantlib.data_utils as du
import quantlib.general_utils as gu

from subsystems.LBMOM.subsys import Lbmom
from brokerage.oanda.oanda import Oanda

with open("config/auth_config.json", "r") as f:
    auth_config = json.load(f)

with open("config/oan_config.json", "r") as f:
    brokerage_config = json.load(f)

#df, instruments = gu.save_file("./Data/data.obj")
#print(df, instruments)
VOL_TARGET = 0.20
brokerage = Oanda(auth_config=auth_config)
db_instruments = brokerage_config["fx"] + brokerage_config["indices"] + brokerage_config["commodities"] + brokerage_config["metals"] + brokerage_config["bonds"] brokerage_config["crypto"] 

database_df = gu.read_file("./Data/oan_ohlcv.obj")
#database_df = pd.read_excel("./Data/oan_ohlcv.xlsx").set_index("date")

print(database_df)

historical_data = du.extend_dataframe(traded=db_instruments, df=database_df)

exit()
sim_start = df.index[-1] - relativedelta(years=5)


strat = Lbmom(instruments_config="./subsystems/LBMOM/config.json", historical_df=df, simulation_start=sim_start, vol_target=VOL_TARGET)
strat = get_subsys_pos()



