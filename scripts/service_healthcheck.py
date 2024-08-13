import argparse
import logging
import time

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)


parser = argparse.ArgumentParser(description="Check if port is open")
parser.add_argument("--service-name", required=True)
parser.add_argument("--ip", required=True)
parser.add_argument("--port", required=True)

args = parser.parse_args()

# Get arguments
SERVICE_NAME = str(args.service_name)
IP = str(args.ip)
PORT = int(args.port)
PROTOCOL = "http"

# Infinite loop
while True:
    try:
        response = requests.get(f"{PROTOCOL}://{SERVICE_NAME}:{PORT}/")
        logger.info(
            "Port is open! Bye! Service:{} Ip:{} Port:{}".format(SERVICE_NAME, IP, PORT)
        )
        break

    except Exception:
        logger.critical(
            "Port is not open! I'll check it soon! Service:{} Ip:{}"
            " Port:{}".format(SERVICE_NAME, IP, PORT)
        )
        time.sleep(5)
