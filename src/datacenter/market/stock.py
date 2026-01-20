import akshare as ak
import pandas as pd
from log import logger
from datetime import datetime
from utils.stock import identify_market
from config.const import MarketType
import yfinance as yf


class StockDataSource:
    """
    基于 AkShare 的股票数据源模块
    提供 Kline、财务指标、公司资料等原始数据访问接口
    """

    def get_kline(self, symbol: str, period: str = "daily", adjust: str = "qfq") -> pd.DataFrame:
        """
        获取股票历史 K 线数据
        :param symbol: 股票代码，例如 '000001'
        :param period: 'daily', 'weekly', 'monthly'
        :param adjust: 复权类型 'qfq' 前复权, 'hfq' 后复权, 'none' 不复权
        :return: pd.DataFrame 包含 date, open, high, low, close, volume 等
        """
        try:
            if period == "daily":
                market_type = identify_market(symbol=symbol)
                if market_type == MarketType.SH or market_type == MarketType.SZ:
                        df = ak.stock_zh_a_daily(symbol=symbol, start_date="20200101", adjust=adjust)
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


    def get_last_n_years_financials(self, symbol: str, n: int = 3) -> pd.DataFrame:
        """
        获取财务指标数据，例如 ROE, EPS, 净利润等
        :param symbol: 股票代码
        :return: pd.DataFrame 包含财务指标
            "日期": "2025-03-31",
            "摊薄每股收益(元)": 22.1101,
            "加权每股收益(元)": 21.38,
            "每股收益_调整后(元)": 21.38,
            "扣除非经常性损益后的每股收益(元)": null,
            "每股净资产_调整前(元)": 213.4937,
            "每股净资产_调整后(元)": 205.6665,
            "每股经营性现金流(元)": 7.0126,
            "每股资本公积金(元)": 1.0945,
            "每股未分配利润(元)": 166.8805,
            "调整后的每股净资产(元)": null,
            "总资产利润率(%)": 8.8916,
            "主营业务利润率(%)": 77.8142,
            "总资产净利润率(%)": 9.0869,
            "成本费用利润率(%)": 257.8975,
            "营业利润率(%)": 73.1935,
            "主营业务成本率(%)": 8.0264,
            "销售净利率(%)": 54.8895,
            "股本报酬率(%)": 2211.0082,
            "净资产报酬率(%)": 10.3563,
            "资产报酬率(%)": 8.8916,
            "销售毛利率(%)": null,
            "三项费用比重": 6.1911,
            "非主营比重": -0.0132,
            "主营利润比重": 106.3277,
            "股息发放率(%)": null,
            "投资收益率(%)": null,
            "主营业务利润(元)": 39374708061.87,
            "净资产收益率(%)": 10.39,
            "加权净资产收益率(%)": 10.92,
            "扣除非经常性损益后的净利润(元)": 26849883702.9,
            "主营业务收入增长率(%)": 10.5415,
            "净利润增长率(%)": 11.6239,
            "净资产增长率(%)": 7.9077,
            "总资产增长率(%)": 9.4017,
            "应收账款周转率(次)": 2961.4146,
            "应收账款周转天数(天)": 0.0304,
            "存货周转天数(天)": 1209.6774,
            "存货周转率(次)": 0.0744,
            "固定资产周转率(次)": null,
            "总资产周转率(次)": 0.1655,
            "总资产周转天数(天)": 543.8066,
            "流动资产周转率(次)": 0.1953,
            "流动资产周转天数(天)": 460.8295,
            "股东权益周转率(次)": 0.1984,
            "流动比率": 6.0749,
            "速动比率": 4.8258,
            "现金比率(%)": 122.8858,
            "利息支付倍数": -13006.181,
            "长期债务与营运资金比率(%)": null,
            "股东权益比率(%)": 85.857,
            "长期负债比率(%)": null,
            "股东权益与固定资产比率(%)": null,
            "负债与所有者权益比率(%)": 16.4728,
            "长期资产与长期资金比率(%)": null,
            "资本化比率(%)": null,
            "固定资产净值率(%)": null,
            "资本固定化比率(%)": 17.1005,
            "产权比率(%)": 16.3579,
            "清算价值比率(%)": null,
            "固定资产比重(%)": null,
            "资产负债率(%)": 14.143,
            "总资产(元)": 312368697395.05,
            "经营现金净流量对销售收入比率(%)": 0.1741,
            "资产的经营现金流量回报率(%)": 0.0282,
            "经营现金净流量与净利润的比率(%)": 0.3172,
            "经营现金净流量对负债比率(%)": 0.1994,
            "现金流量比率(%)": 20.0801,
            "短期股票投资(元)": null,
            "短期债券投资(元)": null,
            "短期其它经营性投资(元)": null,
            "长期股票投资(元)": null,
            "长期债券投资(元)": 1001954410.51,
            "长期其它经营性投资(元)": null,
            "1年以内应收帐款(元)": null,
            "1-2年以内应收帐款(元)": null,
            "2-3年以内应收帐款(元)": null,
            "3年以内应收帐款(元)": null,
            "1年以内预付货款(元)": null,
            "1-2年以内预付货款(元)": null,
            "2-3年以内预付货款(元)": null,
            "3年以内预付货款(元)": null,
            "1年以内其它应收款(元)": null,
            "1-2年以内其它应收款(元)": null,
            "2-3年以内其它应收款(元)": null,
            "3年以内其它应收款(元)": null
        """
        try:
            start_year = str(datetime.now().year - n)
            df = ak.stock_financial_analysis_indicator(symbol=symbol, start_year=start_year)
            # 可以根据需要提取最新一行数据
            if not df.empty:
                return df
            else:
                logger.warning(f"未获取到 {symbol} 的财务指标数据。")
                return {}
        except Exception as e:
            logger.error(f"Error fetching financials: {e}")
            return {}

    # 获取个股概要信息
    def get_company_profile(self, symbol: str):
        """
        通过东方财富接口获取指定股票代码的公司基本信息。
        :param symbol: 股票代码，如 '600519' (贵州茅台)
        :return: 
        {
            "最新": 1467.11,
            "股票代码": "600519",
            "股票简称": "贵州茅台",
            "总股本": 1252270215.0,
            "流通股": 1252270215.0,
            "总市值": 1837218155128.65,
            "流通市值": 1837218155128.65,
            "行业": "酿酒行业",
            "上市时间": 20010827
        }
        """
        try:
            # 获取个股的概要信息
            # symbol: 股票代码
            # indicator: 用于指定获取信息的类型，这里用 '基本情况'
            market_type = identify_market(symbol)
            if market_type == MarketType.SH or market_type == MarketType.SZ:
                company_info_df = ak.stock_individual_info_em(symbol=symbol)
                
                if not company_info_df.empty:
                    info_dict = company_info_df.set_index('item')['value'].to_dict()
                    return {
                        "name": info_dict.get('股票简称'),
                    }
                else:
                    logger.warning(f"未获取到 {symbol} 的东方财富个股基本情况。")
                    return None
            else:
                ticker = yf.Ticker("AAPL")
                info = ticker.info
                name = info.get("longName") or info.get("shortName")
                return {
                    "name": name,
                }
        except Exception as e:
            logger.error(f"获取 {symbol} 东方财富个股基本情况失败: {e}")
            return None


    def get_pe_pb(self, symbol: str) -> pd.DataFrame:
        """
        获取估值指标 PE 和 PB 数据
        :param symbol: 股票代码，如 '600519' (贵州茅台)
        :return: 
        数据日期    当日收盘价     当日涨跌幅           总市值          流通市值         总股本  ...    PE(TTM)      PE(静)       市净率      PEG值        市现率        市销率
1908  2025-11-14  1456.60 -0.937173  1.824057e+12  1.824057e+12  1252270215  ...  20.261143  21.153844  7.095566  1.263247  21.151156  10.026399
1909  2025-11-17  1471.00  0.988604  1.842089e+12  1.842089e+12  1252270215  ...  20.461445  21.362972  7.165713  1.275736  21.360257  10.125520
1910  2025-11-18  1476.00  0.339905  1.848351e+12  1.848351e+12  1252270215  ...  20.530994  21.435586  7.190069  1.280072  21.432861  10.159937
1911  2025-11-19  1471.01 -0.338076  1.842102e+12  1.842102e+12  1252270215  ...  20.461584  21.363117  7.165761  1.275744  21.360402  10.125589
1912  2025-11-20  1467.11 -0.265124  1.837218e+12  1.837218e+12  1252270215  ...  20.407336  21.306479  7.146763  1.272362  21.303770  10.098744
        """
        try:
            df = ak.stock_value_em(symbol=symbol)
            return df
        except Exception as e:
            logger.error(f"Error fetching PE/PB: {e}")
            return pd.DataFrame()
    
    def get_all_a_shares(self) -> pd.DataFrame:
        """
        获取中国A股市场所有上市公司的股票列表。
        数据源：东方财富-A股实时行情
        :return: 
                code  name
            5446  920978  开特股份
            5447  920981  晶赛科技
            5448  920982  锦波生物
            5449  920985  海泰新能
            5450  920992  中科美菱
        """
        try:
            # 实际返回的是所有A股的列表及实时数据
            stock_list_df = ak.stock_info_a_code_name()
            return stock_list_df
        except Exception as e:
            logger.error(f"获取A股股票列表失败: {e}")
            return pd.DataFrame()


stock_data_source = StockDataSource()


if __name__ == "__main__":
    import orjson
    # res = stock_data_source.get_company_profile("300181")
    # logger.info(orjson.dumps(res,option=orjson.OPT_INDENT_2).decode())
    # df = stock_data_source.get_pe_pb("600519")
    # df = stock_data_source.get_all_a_shares()
    # df = stock_data_source.get_last_n_years_financials("600519")
    df = stock_data_source.get_kline("AAPL")
    logger.info(df.tail())