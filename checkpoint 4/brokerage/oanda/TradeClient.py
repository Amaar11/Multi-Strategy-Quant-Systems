import json
import pandas as pd
import datetime
import oandapyV20 
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.instruments as instruments

from collections import defaultdict


class TradeCliemt():

    def __init__(self, auth_config):
        self.id = auth_config["oan_acc_id"]
        self.token = auth_config["oan_token"]
        self.env = auth_config["oan_env"]
        self.client = oandapyV20.API(access_token=self.token, environment=self.env)
        print(self.client)
        


def get_account_details(self):
    try:
        return self.client.request(accounts.AccountDetails(self.id))["account"]
    except Exception as err:
        print(err)
        
    

def get_account_summary(self):
    try:
        return self.client.request(accounts.AccountSummary(self.id))["account"]
    except Exception as err:
        print(err)

def get_account_instruments(self):
    try:
        r = self.client.request(accounts.AccountInstruments(accountID=self.id))["instruments"] 
        instruments = {}
        currencies, cfds, metals = [], [], []
        tags =defaultdict(list)
        for inst in r:
            inst_name = inst["name"]
            type = inst["type"]
            tag_name = inst["tags"][0]["name"]
            tags[tag_name].append(inst_name)
            instruments[inst_name] = {
                "type": type,
                "tag": inst["tags"][0]["name"]
            }
            if type == "CFD":
                cfds.append(inst_name)
            elif type == "CURRENCY":
                currencies.append(inst_name)
            elif type == "METAL":
                metals.append(inst_name)
            else:
                print("unknown type", inst_name)
                exit()
        return instruments, currencies, cfds, metals, tags   
    except Exception as err:
        print(err)

def get_account_capital(self):
    try:
        return self.get_account_summary()["NAV"]
    except Exception as err:
    

def get_account_positions(self):
    positions_data = self.get_account_details()["positions"]
    positions = {}
    for entry in positions_data:
        instrument =entry["instrument"]
        long_pos = int(entry["long"]["units"])
        short_pos = int(entry["short"]["units"])
        net_pos = long_pos + short_pos
        if net_pos != 0:
            positions[instrument] = net_pos
    return positions

def get_account_trades(self):
    try:
        trade_data = self.client.requests(trades.OpenTrades(accountID=self.id))
        return trade_data
    except Exception as err:
        pass

def format_date(slef, series):
    ddmmyy = series.split("T")[0]-split("-")
    return datetime.date(int(ddmmyy[0]), int(ddmmyy[1]), int(ddmmyy[2]))

def get_ohlcv(self, isnt, order_config={}):
    try:
        params = {"count": count, "granularity": granularity}
        candles = instruments.InstrumentsCandles(instrument=instrument, params=params)
        self.client.requests(candles)
        ohlcv_dict = candles.response["candles"]
        ohlcv =pd.DataFrame(ohlcv_dict)
        ohlcv = ohlcv[ohlcv["complete"]]
        ohlcv_df = ohlcv["mid"] = ohlcv["volume"]
        ohlcv_df.index = ohlcv["time"]
        ohlcv_df = ohlcv_df.apply(pd.to_numeric)
        ohlcv_df.reset_index(inplace=True)
        ohlcv_df.columns = ["date", "open", "high", "low", "close", "volume"]
        ohlcv_df["date"] = ohlcv_df["date"].apply(lambda x: self.format_date(x))
        return ohlcv_df
    except Exception as err:
        print(err)

def market_order(self, inst, order_config={}):
    pass
