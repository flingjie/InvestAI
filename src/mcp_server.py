# server.py
from fastmcp import FastMCP
from log import logger
from tools.watch_list import add_to_watchlist, load_watchlist
from config import WATCHLIST_PATH
from utils.stock import get_fullcode, extract_code
from datacenter.market.stock import stock_data_source
from notifiers.formater.stock import format_trend_signal_message
from engine.signal_engine import SignalEngine
from agents.strategy_editor import edit_strategy
from agents.strategy_explainer import explain_strategy
from config import STRATEGY_CONFIG_PATH, STRATEGY_CONFIG
import yaml



mcp = FastMCP("InvestAI 🚀")

@mcp.tool()
async def analyze_stock_tool(code: str):
    """
    Analyze a specific stock by its code

    Parameters:

    * code: stock ticker symbol

    Returns:

    * A string containing the stock analysis result.
    """
    fullcode = get_fullcode(code)
    logger.info(f"Analyzing stock {fullcode}")
    signal_engine = SignalEngine()
    context = signal_engine.evaluate(fullcode)
    result = context['result']
    logger.info(f"Stock {fullcode} analysis result: {result}")
    data = stock_data_source.get_company_profile(extract_code(fullcode))
    stock_name = data.get('name') 
    result.update({
        "name": stock_name,
    })
    message = format_trend_signal_message(result)
    logger.info(message)
    return message


@mcp.tool()
async def add_watchlist_tool(code: str):
    """
    Add a specific stock code to the watchlist

    Parameters:

    * code: stock ticker symbol

    Returns:

    * A string containing the success message.
    """
    fullcode = get_fullcode(code)
    logger.info(f"get company profile for {code}")
    data = stock_data_source.get_company_profile(extract_code(fullcode))
    name = data.get('name') 
    logger.info(f"Add stock {fullcode}({name}) to watchlist")
    add_to_watchlist(WATCHLIST_PATH, {"code": fullcode, "name": name})
    return f"{fullcode}({name}) has been added to watchlist"

@mcp.tool()
async def get_watchlist_tool():
    """
    Get the current watchlist

    Returns:

    * A string containing the watchlist.
    """
    watchlist = load_watchlist(WATCHLIST_PATH)
    return watchlist


@mcp.tool()
async def explain_strategy_tool():
    """
    Explain the current strategy configuration in a readable manner

    Returns:    

    * A string containing the strategy explanation.
    """
    strategy = explain_strategy(STRATEGY_CONFIG)
    return strategy

@mcp.tool()
async def edit_strategy_tool(user_input: str):
    """
    Edit the strategy configuration based on user input

    Parameters:

    * user_input: user input describing the preferences or adjustments

    Returns:    

    * A string containing the edited strategy configuration.
    """
    with open(STRATEGY_CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
        strategy = edit_strategy(raw, user_input)
    return strategy


# ----------- start server ------------
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8888)