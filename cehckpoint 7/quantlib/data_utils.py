import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import datetime


def get_sp500_instruments():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    return list (df[0]['Symbol'])

#tickers = get_sp500_instruments()
#print(tickers)
   # print(df[0].to_json(orient='records'))

def get_sp500_df():
    symbol = get_sp500_instruments()
    symbol = symbol[:30]
    ohclvs = {}
    for symbol in symbol:
        symbol_df = yf.Ticker(symbol).history(period="10y")
        ohclvs[symbol] = symbol_df[["Open", "High","Low", "Close","Volume"]].rename(
            columns={
                "Open":"open",
                "High":"high",
                "Low":"low",
                "Close":"close",
                "Volume":"volume"
            }
        )
        print(symbol)
        print(ohclvs[symbol])   
    df = pd.DataFrame(index=ohclvs["GOOGLE"].index)
    df.index.name = "date"
    instruments = list(ohclvs.keys())

    for inst in instruments:
        inst_df=ohclvs[inst]
        columns = list(map(lambda : "{} {}".format(inst, x), inst_df.columns))
        df[columns] = inst_df

    return df, instruments


df, instruments = get_sp500_df()

#df.to_excel('./C:/Users/pc/Desktop/projekat/sp500_data.xlsx')

def extend_dataframe(traded, df, fx_codes):
    df.index = pd.Series(df.index).apply(lambda x: format_date(x))
    open_cols = list(map(lambda x: str(x) + "open", traded))
    high_cols = list(map(lambda x: str(x) + "high", traded))
    low_cols = list(map(lambda x: str(x) + "low", traded))
    close_cols = list(map(lambda x: str(x) + "close", traded))
    volume_cols = list(map(lambda x: str(x) + "volume", traded))
    historical_data = df.copy()
    historical_data = historical_data[open_cols + high_cols + low_cols + close_cols + volume_cols]
    historical_data.fillna(method="ffill",inplace=True)
    historical_data.fillna(method="bfill",inplace=True)
    for inst in traded:
        historical_data["{} % ret".format(inst)] = historical_data["{} % close".format(inst)] / historical_data["{} % close".format(inst)].shift(1) - 1
        historical_data["{} % ret vol".format(inst)] = historical_data["{} % ret".format(inst)].rolling(25).std()
        historical_data["{} % active".format(inst)] = historical_data["{} % close".format(inst)] != historical_data["{} % close".format(inst)].shift(1)

        if is_fx(inst, fx_codes):
            inst_rev = "{}_{}".format(inst.split("_")[1], inst.split("_")[0])
            historical_data["{} close".format(inst_rev)] = 1 / historical_data["{} close".format(inst)]
            historical_data["{} % ret".format(inst_rev)] = historical_data["{} % close".format(inst_rev)] / historical_data["{} % close".format(inst_rev)].shift(1) - 1   
            historical_data["{} % ret vol".format(inst_rev)] = historical_data["{} % ret".format(inst_rev)].rolling(25).std()     
            historical_data["{} % active".format(inst_rev)] = historical_data["{} % close".format(inst_rev)] != historical_data["{} % close".format(inst_rev)].shift(1)    
    return historical_data

def is_fx(inst, fx_codes):
    return len(inst.split("_")) == 2 and inst.split("_")[0] in fx_codes and inst.split("_")[1] in fx_codes

def format_date(date):
    yymmdd = list(map(lambda x: int(x), str(date).split(" ")[0].split("-")))
    return datetime.date(yymmdd[0], yymmdd[1], yymmdd[2])

#df, instruments = get_sp500_df
#df = extend_dataframe(traded=instruments,df=df)
#print(df)
#df = pd.read_excel("./projekat/hist.xlsx").set_index("date")
#df.to_excel("./hist.xlsx")