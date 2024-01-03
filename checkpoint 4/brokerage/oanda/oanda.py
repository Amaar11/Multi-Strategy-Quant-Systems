from brokerage.oanda.TradeClient import TradeCliemt

class Oanda():

    def __init__(self, auth_config={}):
        self.trade_client = TradeClient(auth_config=auth_config)

    def get_service_client(self):
        pass
      
    def get_trade_client(self):
        return self.trade_client
