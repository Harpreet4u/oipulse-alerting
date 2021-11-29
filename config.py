import os

YAHOO_URL = "https://query1.finance.yahoo.com/v7/finance/download/%5ENSEBANK?period1=" \
            "{from_timestamp}&period2={end_timestamp}&interval=1d&" \
            "events=history&includeAdjustedClose=true"
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
EXPIRY = os.getenv("EXPIRY", "")
TIME_FRAME = os.getenv("TIME_FRAME", "")
DIFF_THRESHOLD = os.getenv("DIFF_THRESHOLD", "")
HOST_API = "https://api.oipulse.com"
HOST = "https://www.oipulse.com"
TRENDING_OI_HTML_PATH = "/app/options-analysis/trending-oi"
FUTURES_OI_HTML_PATH = "/app/futures-analysis"
TRENDING_OI_API_PATH = "/api/trending-oi-static/gettrendingoiforselectedstrikeprices"
FUTURES_OI_API_PATH = "/api/futures/getselectedfuturesalldata"
OI_TIME_FRAMES = {
    3: 3,
    5: 5,
    10: 5,
    15: 15,
    30: 15,
    60: 15
}
