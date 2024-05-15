import datetime
import json
import os
from datetime import datetime, timedelta
from typing import List, Optional

from loguru import logger
from sqlmodel import Session, select

from .bot_utils import send_get_group_member_request, send_message_to_group
from .models import Message, RoomInfo, engine

ROOM_ID = os.getenv("ROOM_ID")


def get_room_info_from_db() -> Optional[RoomInfo]:
    with Session(engine) as session:
        statement = select(RoomInfo).where(RoomInfo.room_id == ROOM_ID)
        room_info = session.exec(statement).first()
        return room_info


def summary_by_chatgpt(msg: str):
    return "还没实现自动总结群聊精华[Doge]"


# 创建一个函数，用于获取数据库中的消息
def get_messages(start_time, end_time, session: Session):
    """time_stamp in milliseconds"""
    messages = session.exec(
        select(Message).where(Message.timestamp.between(start_time, end_time))
    ).all()
    logger.debug(f"last day message: {len(messages)}")
    return messages


# 创建一个函数，用于拼接消息并调用summary_func函数
def summarize_messages(messages):
    msgs = "\n".join([f"{msg.talkerName}\n{msg.text}" for msg in messages])
    summary = summary_by_chatgpt(msgs)
    return summary


# 用于统计每个人的打卡次数和发言次数
def count_activities(messages: List[Message]):
    room_info = get_room_info_from_db()
    members = json.loads(room_info.members)

    member_dict = {member["id"]: member["name"] for member in members}
    check_in_counts = {member["id"]: 0 for member in members}
    talk_counts = {member["id"]: 0 for member in members}

    for msg in messages:
        if "#打卡" in msg.text:
            check_in_counts[msg.talkerId] += 1
        talk_counts[msg.talkerId] += 1

    # rename id to name
    check_in_counts = {
        member_dict[id]: count
        for id, count in check_in_counts.items()
        if id in member_dict
    }
    talk_counts = {
        member_dict[id]: count for id, count in talk_counts.items() if id in member_dict
    }

    return check_in_counts, talk_counts


def readable_counts(counts: dict):
    astr = ""
    for name, count in counts.items():
        astr += f"{name}: {count}\n"
    return astr


def five_seconds_task():
    pass


def daily_task():
    now = datetime.now()
    start_time = int((now - timedelta(days=1)).timestamp() * 1000)
    end_time = int(now.timestamp() * 1000)

    with Session(engine) as session:
        messages = get_messages(start_time, end_time, session)
        if len(messages) > 99:
            summary = summarize_messages(messages)
            send_message_to_group("今日群聊总结：\n" + summary)

        # for test:
        check_in_counts, talk_counts = count_activities(messages)
        send_message_to_group(
            f"本日打卡情况: \n {check_in_counts=} \n\n {talk_counts=}"
        )


def weekly_task():
    now = datetime.now()
    start_time = int((now - timedelta(days=7)).timestamp() * 1000)
    end_time = int(now.timestamp() * 1000)

    with Session(engine) as session:
        messages = get_messages(start_time, end_time, session)
        # if len(messages) > 700:
        #     summary = summarize_messages(messages)
        #     send_message_to_group("本周群聊总结：\n" + summary)

        check_in_counts, talk_counts = count_activities(messages)
        inactive_members = [name for name, count in talk_counts.items() if count == 0]
        less_check_in_members = [
            (name, count) for name, count in check_in_counts.items() if count < 2
        ]

        if inactive_members:
            send_message_to_group("本周不活跃的人： " + ", ".join(inactive_members))
        if less_check_in_members:
            send_message_to_group(
                "本周打卡次数小于2次的人： "
                + ", ".join(
                    [f"{name}，{count}" for name, count in less_check_in_members]
                )
            )
    send_get_group_member_request()  # refresh group members every week
