import requests

from config import AUTH_TOKEN, HOST_API, TRENDING_OI_API_PATH, FUTURES_OI_API_PATH, TRENDING_OI_HTML_PATH, \
    FUTURES_OI_HTML_PATH, HOST
from utils import DataType


def get(url, payload, headers):
    response = requests.get(url, params=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def post(url, payload, headers):
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def get_oi_pulse_app_headers():
    return {
        "authorization": f"Bearer {AUTH_TOKEN}",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.63 Safari/537.36",
        "origin": "https://oipulse.com"
    }


def get_oi_pulse_request_headers():
    return {
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "accept": "application/json, text/plain, /",
        "authorization": f"Bearer {AUTH_TOKEN}",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/93.0.4577.63 Safari/537.36",
        "origin": "https://oipulse.com"
    }


def get_oi_html_url(data_type):
    if data_type == DataType.TRENDING_OI:
        return f"{HOST}{TRENDING_OI_HTML_PATH}"
    if data_type == DataType.FUTURES_OI:
        return f"{HOST}{FUTURES_OI_HTML_PATH}"


def get_oi_url(data_type):
    if data_type == DataType.TRENDING_OI:
        return f"{HOST_API}{TRENDING_OI_API_PATH}"
    if data_type == DataType.FUTURES_OI:
        return f"{HOST_API}{FUTURES_OI_API_PATH}"


def get_trending_oi_payload(bn_date, strikes, expiry, mode="historical"):
    return {
        "stSelectedAsset": "BANKNIFTY",
        "stSelectedAvailableDate": bn_date.strftime("%Y-%m-%d"),
        "stSelectedAvailableExpiryDate": expiry,
        "selectedStrikePrices": strikes,
        "stSelectedModeOfData": mode
    }


def get_futures_oi_payload(bn_date, mode="historical"):
    bn_date_str = bn_date.strftime("%Y-%m-%d")
    return {
        "stSelectedFutures": "BANKNIFTY",
        "stSelectedAvailableDate": bn_date_str,
        "stSelectedExpiry": "I",
        "stSelectedModeOfData": mode
    }


def get_payload(bn_date, strikes, expiry, data_type, mode="historical"):
    if data_type == DataType.TRENDING_OI:
        return get_trending_oi_payload(bn_date, strikes, expiry, mode)
    if data_type == DataType.FUTURES_OI:
        return get_futures_oi_payload(bn_date, mode)
