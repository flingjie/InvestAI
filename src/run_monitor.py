from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BlockingScheduler
from engine.monitor import StockMonitor
from tools.index_tool import load_index_pool
from tools.watch_list import load_watchlist
from config import WATCHLIST_PATH, INDEX_POOL_PATH
from log import logger
from datetime import datetime
from config import SCHEDULE_CONFIG
from notifiers.manager import notification_manager

def format_time_marker() -> str:
    date = datetime.now()
    return f"=== {date.strftime('%Y-%m-%d')} ==="

def start_monitor():
    marker = format_time_marker()
    logger.info(marker)
    notification_manager.notify(marker)
    watchlist = load_watchlist(WATCHLIST_PATH)
    index_pool = load_index_pool(INDEX_POOL_PATH)   
    monitor = StockMonitor(
        watchlist=watchlist,
        index_pool=index_pool,
    )
    monitor.run()

def start_scheduler():
    logger.info(f"Start scheduler at {SCHEDULE_CONFIG.hour}:{SCHEDULE_CONFIG.minute}")
    scheduler = BlockingScheduler()
    scheduler.add_job(
        start_monitor,
        CronTrigger(hour=SCHEDULE_CONFIG.hour, minute=SCHEDULE_CONFIG.minute),
        coalesce=True
    )
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()