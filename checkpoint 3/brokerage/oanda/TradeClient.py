import oandapyV20 
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.positions as positions
import oandapyV20.endpoints.instruments as instruments


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
        

def get_account_capital(self):
    try:
        return self.get_account_summary()["NAV"]
    except Exception as err:
    

def get_account_positions(self):
    positions_data = self.get_account_details()["positions"]
    return positions_data

def get_account_trades(self):
    pass

def get_account_orders(self):
    pass

def get_ohlcv(self, isnt, order_config={}):
    pass

def market_order(self, inst, order_config={}):
    pass
