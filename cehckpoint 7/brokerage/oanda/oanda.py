from brokerage.oanda.TradeClient import TradeCliemt

class Oanda():

    def __init__(self, auth_confih={}):
        self.trade_client = TradeCliemt(auth_config=auth_config)

    def get_service_client(self):
        pass
      
    def get_trade_client(self):
        return self.trade_client
