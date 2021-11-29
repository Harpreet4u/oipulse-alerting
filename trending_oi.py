import logging
import sys
from collections import ChainMap
from datetime import datetime
from time import sleep

import pandas as pd
from playsound import playsound

from config import OI_TIME_FRAMES, EXPIRY, TIME_FRAME, DIFF_THRESHOLD
from utils import DataType
from utils.api import post, get_oi_pulse_request_headers, get_payload, \
    get_oi_url

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s:%(name)s: %(message)s (%(asctime)s; %(filename)s:%(lineno)d)"
)


def is_data_loaded(data_type, data):
    if data_type == DataType.TRENDING_OI:
        return data.get("data") and data.get("data").get("data")
    if data_type == DataType.FUTURES_OI:
        return data.get("data")
    return None


def load_oi_data(data_type=DataType.TRENDING_OI):
    bn_date_str = datetime.today().strftime("%Y-%m-%d")
    logger.info(f"Data date: {bn_date_str}, expiry date: {EXPIRY}")
    logger.info(f"Loading {data_type.value} data: {bn_date_str}")
    data = post(
        url=get_oi_url(data_type),
        headers=get_oi_pulse_request_headers(),
        payload=get_payload(datetime.today(), [], EXPIRY, data_type, mode="live")
    )

    if data.get("status") == "fail" or not is_data_loaded(data_type, data):
        logger.error(f"Unable to load {data_type.value} data for date: {bn_date_str}, Error: {data.get('msg')}"
                     f" or empty data key in json response")
        return None
    return data


def load_oi_data_frames(data, data_type):
    bn_date_str = datetime.today().strftime("%Y-%m-%d")
    logger.info(f"Data date: {bn_date_str}")
    rows = get_data_frame_records(data, data_type)
    compute_data_frames(rows, data_type)


def parse_trending_oi_record(dt, record):
    obj_oi_data = [{"CE": 0}, {"PE": 0}] if not record.get("objOiData") else record.get("objOiData")
    return {"LTP": record.get("inClose"), "DT": dt, **dict(ChainMap(*obj_oi_data))}


def parse_futures_oi_record(dt, record):
    for key in ["stDate", "stTime", "stName", "stDataFetchType"]:
        record.pop(key, None)
    return {"DT": dt, **record}


def extract_records(records, data_type):
    if data_type == DataType.TRENDING_OI:
        return records["data"]["data"]
    if data_type == DataType.FUTURES_OI:
        return records["data"]
    return []


def parse_record(dt, record, data_type):
    if data_type == DataType.TRENDING_OI:
        return parse_trending_oi_record(dt, record)
    if data_type == DataType.FUTURES_OI:
        return parse_futures_oi_record(dt, record)
    return None


def get_data_frame_records(records, data_type):
    rows = []
    for record in extract_records(records, data_type):
        if record["stDataFetchType"] == "EOD":
            continue
        hour, minute, second = map(int, record["stTime"].split(":"))
        st_date = datetime.strptime(record.get("stFetchDate") or record.get("stDate"), "%Y-%m-%d")
        dt = datetime(
            day=st_date.day, year=st_date.year, month=st_date.month, hour=hour,
            minute=minute, second=second)
        new_record = parse_record(dt, record, data_type)
        if new_record:
            rows.append(new_record)
    return rows


def compute_trending_oi_data_frames(df, prev_day_df):
    k = int(TIME_FRAME)
    v = OI_TIME_FRAMES.get(k)

    toi_df = prev_day_df.append(df.iloc[v::k, :]).diff(1).dropna().cumsum()
    toi_df["DIFF"] = toi_df["PE"] - toi_df["CE"]
    toi_df["CHG_IN_LTP"] = toi_df["LTP"].diff(1)
    toi_df["CHG_IN_LTP_PER"] = toi_df["CHG_IN_LTP"].div(toi_df["LTP"].shift(1).abs()).mul(100).round(2)
    toi_df["CHG_IN_DIR"] = toi_df["DIFF"].diff(1)
    toi_df["CHG_IN_DIR_PER"] = toi_df["CHG_IN_DIR"].div(toi_df["DIFF"].shift(1).abs()).mul(100).round(2)
    toi_df["PCR"] = toi_df["PE"].div(toi_df["CE"]).round(2)
    notify(toi_df)


def notify(toi_df):
    global is_threshold_detected
    if abs(toi_df["DIFF"][-1]) >= int(DIFF_THRESHOLD):
        logger.info(f"Trending OI threshold reached")
        is_threshold_detected = True
        playsound("alert.wav")


def compute_data_frames(rows, data_type):
    df = pd.DataFrame(rows)
    df.sort_values(by="DT", inplace=True)
    df = df.set_index("DT").reset_index().drop_duplicates(subset="DT", keep="first").set_index("DT")
    prev_day_df = df[:1]
    if data_type == DataType.TRENDING_OI:
        compute_trending_oi_data_frames(df, prev_day_df)


def main():
    data = load_oi_data(DataType.TRENDING_OI)
    if data:
        load_oi_data_frames(data, DataType.TRENDING_OI)


if __name__ == "__main__":
    is_threshold_detected = False
    while not is_threshold_detected:
        main()
        sleep(int(TIME_FRAME)*60)
