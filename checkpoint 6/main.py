import json
import datetime
import pandas as pd

from dateutil.relativedelta import relativedelta

import quantlib.data_utils as du
import quantlib.general_utils as gu

from brokerage.oanda.oanda import Oanda
from subsystems.LBMOM.subsys import Lbmom
from subsystems.LSMOM.subsys import Lsmom

with open("config/auth_config.json", "r") as f:
    auth_config = json.load(f)

with open("config/portfolio_config.json", "r") as f:
    portfolio_config = json.load(f)    

with open("config/oan_config.json", "r") as f:
    brokerage_config = json.load(f)

def main():
    

    #df, instruments = gu.save_file("./Data/data.obj")
    #print(df, instruments)
    #VOL_TARGET = portfolio_config["vol_target"]
    brokerage = Oanda(auth_config=auth_config)
    db_instruments = brokerage_config["fx"] + brokerage_config["indices"] + brokerage_config["commodities"] + brokerage_config["metals"] + brokerage_config["bonds"] +  brokerage_config["crypto"] 

    database_df = gu.read_file("./Data/oan_ohlcv.obj")
    #database_df = pd.read_excel("./Data/oan_ohlcv.xlsx").set_index("date")

    print(database_df)



   
    #poll_df.to_excel("./Data/oan_ohlcv.xlsx")

    historical_data = du.extend_dataframe(traded=db_instruments, df=database_df, fx_codes=brokerage_config["fx_codes"])
    print(list(historical_data))

    """
    risk parameters
    """

    VOL_TARGET = portfolio_config["vol_target"]
    sim_start = datetime.date.today() - relativedelta(years=portfolio_config["sim_years"])

    """
    Get existing positions and capital
    """
    capital = brokerage.get_trade_client().get_account_capital()
    positions = brokerage.get_trade_client().get_account_positions()
    print(capital,positions)


    """
    Get position of subsystems
    """

  
    subsystems_config = portfolio_config["subsystems"]["oan"]
    strats = {}

    for subsystem in subsystems_config.keys():
        if subsystem == "Lbmom":
            strat = Lbmom(
                instruments_config=portfolio_config["instrumenst_config"] [subsystem] ["oan"], 
                historical_df=historical_data, 
                simulation_start=sim_start, 
                vol_target=VOL_TARGET, 
                brokerage_used="oan"
            )
        elif subsystem == "lsmom":
            strat = Lsmom(
                instruments_config=portfolio_config["instrumenst_config"] [subsystem] ["oan"], 
                historical_df=historical_data, 
                simulation_start=sim_start, 
                vol_target=VOL_TARGET, 
                brokerage_used="oan"
            )
        else:
            pass
        strats[subsystem] = strat

    for k, v in strats.items():
        print("run", k, v)
        strat_db, strat_inst = v.get_subsys_pos(debug=True)
        print(strat_db, strat_inst)

if __name__ == "__main__":
    main()

