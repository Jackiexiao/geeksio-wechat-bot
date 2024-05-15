import asyncio
import time
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, Request
from loguru import logger
from sqlmodel import Session, select
from apscheduler.schedulers.background import BackgroundScheduler

from .models import Message, engine, get_session

bot_url = 'https://msg.io.sapling.pro'

def send_message_to_group(msg: str):
    pass


def summary_by_chatgpt(msg: str):
    return "summary"


def get_group_members():
    return ["jackie", "amy"]


app = FastAPI(
    title="wechat bot msg handler",
    description="Wechat bot msg handler, https://github.com/Jackiexiao/geeksio-wechat-bot",
    version="1.0.0",
)


async def repeat_task(wait_time, task, *args, **kwargs):
    while True:
        await asyncio.sleep(wait_time)
        await task(*args, **kwargs)


# 计算从现在开始到下一个24点的秒数
def seconds_until_midnight():
    now = datetime.now()
    midnight = datetime.combine(now + timedelta(days=1), time(0))
    return (midnight - now).seconds


# 计算从现在开始到下一个周六中午12点的秒数
def seconds_until_next_saturday_noon():
    now = datetime.now()
    next_saturday_noon = (
        now + timedelta((5 - now.weekday() + 7) % 7) + timedelta(hours=12)
    )
    return (next_saturday_noon - now).seconds


# 修改update_msg函数，将每条消息保存到数据库
@app.post("/msg/")
async def update_msg(request: Request, session: Session = Depends(get_session)):
    message = await request.json()
    logger.debug(message)


@app.post("/msg/")
async def update_msg(request: Request, session: Session = Depends(get_session)):
    message = await request.json()
    logger.debug(message)

    message = Message(**message)
    session.add(message)
    session.commit()

    # # 构造新的消息
    # new_message = {
    #     "text": f"I received a message: {message.text}",
    #     "token": message.token
    # }

    # # 使用httpx库异步发送新的消息到指定的URL
    # async with httpx.AsyncClient() as client:
    #     response = await client.post("https://msg.io.sapling.pro", json=new_message)

    # # 检查请求是否成功
    # if response.status_code == 200:
    #     logger.debug("Message sent successfully.")
    # else:
    #     logger.error(f"Failed to send message. Status code: {response.status_code}")

    return {"hello": "world"}


# 创建一个函数，用于获取数据库中的消息
def get_messages(start_time, end_time, session: Session):
    messages = session.exec(
        select(Message).where(Message.timestamp.between(start_time, end_time))
    ).all()
    return messages


# 创建一个函数，用于拼接消息并调用summary_func函数
def summarize_messages(messages):
    msgs = "\n".join([f"{msg.talkerName}\n{msg.text}" for msg in messages])
    summary = summary_by_chatgpt(msgs)
    return summary


# 创建一个函数，用于统计每个人的打卡次数和发言次数
def count_activities(messages):
    talkers = get_group_members()
    check_in_counts = {talker: 0 for talker in talkers}
    talk_counts = {talker: 0 for talker in talkers}

    for msg in messages:
        if "#打卡" in msg.text:
            check_in_counts[msg.talkerName] += 1
        talk_counts[msg.talkerName] += 1

    return check_in_counts, talk_counts

def daily_task():
    now = datetime.now()
    start_time = int((now - timedelta(days=1)).timestamp())
    end_time = int(now.timestamp())

    with Session(engine) as session:
        messages = get_messages(start_time, end_time, session)
        if len(messages) > 99:
            summary = summarize_messages(messages)
            send_message_to_group("今日群聊总结：\n" + summary)


def weekly_task():
    now = datetime.now()
    start_time = int((now - timedelta(days=7)).timestamp())
    end_time = int(now.timestamp())

    with Session(engine) as session:
        messages = get_messages(start_time, end_time, session)
        if len(messages) > 700:
            summary = summarize_messages(messages)
            send_message_to_group("本周群聊总结：\n" + summary)

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


@app.on_event('startup')
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_task, 'cron', hour=0)  # run daily_task every day at midnight
    scheduler.add_job(weekly_task, 'cron', day_of_week='sat', hour=12)  # run weekly_task every Saturday at noon
    scheduler.start()