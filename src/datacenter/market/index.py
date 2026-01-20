import akshare as ak
import pandas as pd
from log import logger
import orjson
from datetime import datetime
import yfinance as yf
from utils.stock import identify_market
from config.const import MarketType

class IndexDataSource:

    def get_kline(self, symbol: str, period: str = "daily") -> pd.DataFrame:
        try:
            if period == "daily":
                market_type = identify_market(symbol=symbol)
                if market_type == MarketType.SH or market_type == MarketType.SZ:
                    df = ak.stock_zh_index_daily(symbol=symbol)
                elif market_type == MarketType.HK or market_type == MarketType.US:
                    apple = yf.Ticker(symbol)

                    df = apple.history(period="6mo", interval="1d")
                    df = df.reset_index()
                    df.columns = df.columns.str.lower()
                else:
                    raise ValueError(f'Unsupported symbol: {symbol}')
            else:
                raise ValueError(f"Unsupported period: {period}")
            return df
        except Exception as e:
            logger.opt(exception=e).error(f"Error fetching Kline: {e}")
            return pd.DataFrame()


index_data_source = IndexDataSource()


if __name__ == "__main__":
    # df = index_data_source.get_kline("sh000300")
    df = index_data_source.get_kline("^GSPC")
    print(df.head())
    print(df.columns)