import base64
import io
import json
import logging
import os
import re
import sys
from datetime import datetime
from time import sleep

import pytesseract
from PIL import Image, ImageOps
from playsound import playsound

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s:%(name)s: %(message)s (%(asctime)s; %(filename)s:%(lineno)d)"
)


def parse_string(text):
    """Only parses the In signal"""
    # TODO: Improve upon to fetch stop loss (Out) and trigger order automatically
    in_pattern = re.compile(r"In: ([0-9.]+)", re.M)
    match = in_pattern.findall(text)
    return match


def detect_signal():
    with open("ospl_image.txt") as f:
        base64_image = f.read()
        if not base64_image:
            return
        image_string = io.BytesIO(base64.b64decode(base64_image.split('base64,')[-1].strip()))
        image = Image.open(image_string)
        image = image.convert('L')
        image = ImageOps.invert(image)
        # Optimization: https://stackoverflow.com/questions/61134400/pytesseract-ocr-on-image-with-text-in-different-colors

        logger.info("========= Signals found in image ===========")
        parsed_signals = parse_string(pytesseract.image_to_string(image))
        logger.info(f"{parsed_signals}")

        # Save the image passed to pytesseract for debugging purposes
        image.save('pic.png')
        return parsed_signals


def load_saved_signals():
    try:
        with open(f"signals_{datetime.today().strftime('%Y-%m-%d')}.txt", 'r') as f:
            signals_json = f.read()
            signals = json.loads(signals_json)
            return signals
    except Exception as e:
        logger.error(f"Error loading signals: {str(e)}")
    return {}


def alert():
    playsound("alert.wav")


def notify(parsed_signals):
    for signal in parsed_signals:
        signal = signal.strip()
        if not __signals_found.get(signal):
            __signals_found[signal] = 1
            logger.info(f"New signal detected: In {signal}")
            alert()


if __name__ == "__main__":
    __signals_found = {}
    __signals_found.update(load_saved_signals())
    while True:
        try:
            notify(detect_signal())
            os.remove("ospl_image.txt")
        except Exception:
            pass
        finally:
            with open(f"signals_{datetime.today().strftime('%Y-%m-%d')}.txt", 'w+') as f:
                f.write(json.dumps(__signals_found))
        sleep(1)



