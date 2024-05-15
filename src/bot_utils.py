import json
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

bot_url = "https://msg.io.sapling.pro"
ROOM_ID = os.getenv("ROOM_ID")
TOKEN = os.getenv("TOKEN")
logger.debug(f"ROOM_ID: {ROOM_ID}, TOKEN: {TOKEN}")


def send_get_group_member_request() -> List[Dict[str, str]]:
    data = {"text": "", "type": 35, "roomId": ROOM_ID, "token": TOKEN}
    logger.debug(data)
    response = requests.post(bot_url, json=data)
    if response.status_code != 200:
        logger.error(response.text)

    return response.status_code == 200


def send_message_to_group(msg: str):
    data = {"text": msg, "type": 7, "roomId": ROOM_ID, "token": TOKEN}
    logger.debug(data)
    response = requests.post(bot_url, json=data)
    if response.status_code != 200:
        logger.error(response.text)
    return response.status_code == 200
