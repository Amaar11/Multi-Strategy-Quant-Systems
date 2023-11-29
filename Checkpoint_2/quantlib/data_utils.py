import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import datetime

def get_sp500_instruments():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    return list(df[0]['Symbol'])

def get_sp500_df():
    symbol = get_sp500_instruments()
    symbol = symbol[:30]
    ohclvs = {}
    for symbol in symbol:
        symbol_df = yf.Ticker(symbol).history(period="10y")
        ohclvs[symbol] = symbol_df[["Open", "High", "Low", "Close", "Volume"]].rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            }
        )
        print(symbol)
        print(ohclvs[symbol])
    df = pd.DataFrame(index=ohclvs["GOOGL"].index)
    df.index.name = "date"
    instruments = list(ohclvs.keys())

    for inst in instruments:
        inst_df = ohclvs[inst]
        columns = list(map(lambda x: "{} {}".format(inst, x), inst_df.columns))
        df[columns] = inst_df
        dataframes_to_concat = [df, inst_df]
        df = pd.concat(dataframes_to_concat, axis=1)

    # Convert datetime values to timezone-unaware
    df.index = df.index.tz_localize(None)

    return df, instruments


"""
def extend_dataframe(traded, df):
    #df.index = pd.Series(df.index).apply(lambda x: format_date(x))
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
    return historical_data
    """

def extend_dataframe(traded, df):
    historical_data = df.copy()
    open_cols = [f"{inst} open" for inst in traded]
    high_cols = [f"{inst} high" for inst in traded]
    low_cols = [f"{inst} low" for inst in traded]
    close_cols = [f"{inst} close" for inst in traded]
    volume_cols = [f"{inst} volume" for inst in traded]

    # Check if these columns exist in the DataFrame before selecting
    all_columns = historical_data.columns
    selected_columns = open_cols + high_cols + low_cols + close_cols + volume_cols
    missing_columns = [col for col in selected_columns if col not in all_columns]

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return historical_data

    historical_data = historical_data[selected_columns]
    historical_data.fillna(method="ffill", inplace=True)
    historical_data.fillna(method="bfill", inplace=True)

    for inst in traded:
        historical_data[f"{inst} % ret"] = historical_data[f"{inst} close"] / historical_data[f"{inst} close"].shift(1) - 1
        historical_data[f"{inst} % ret vol"] = historical_data[f"{inst} % ret"].rolling(25).std()
        historical_data[f"{inst} % active"] = historical_data[f"{inst} close"] != historical_data[f"{inst} close"].shift(1)

    return historical_data


df, instruments = get_sp500_df()
df = extend_dataframe(traded=instruments, df=df)
print(df)
df.to_excel("./hist.xlsx")

