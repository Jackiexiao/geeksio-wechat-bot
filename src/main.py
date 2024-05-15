from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends, FastAPI, Request
from loguru import logger
from sqlmodel import Session

from .bot_utils import send_get_group_member_request
from .models import Message, RoomInfo, get_session
from .schedule_tasks import daily_task, five_seconds_task, weekly_task

app = FastAPI(
    title="wechat bot msg handler",
    description="Wechat bot msg handler, https://github.com/Jackiexiao/geeksio-wechat-bot",
    version="1.0.0",
)


@app.on_event("startup")
def start_scheduler():
    send_get_group_member_request()
    scheduler = BackgroundScheduler()
    scheduler.add_job(five_seconds_task, "interval", seconds=5)
    scheduler.add_job(
        daily_task, "cron", hour=0
    )  # run daily_task every day at midnight
    scheduler.add_job(
        weekly_task, "cron", day_of_week="sat", hour=12
    )  # run weekly_task every Saturday at noon
    scheduler.start()


@app.post("/msg")
async def save_msg(request: Request, session: Session = Depends(get_session)):
    message = await request.json()
    logger.debug(message)
    if "members" in message:  # type: room info
        room_id = message["roomId"]
        members = message["members"]
        room_info = session.get(RoomInfo, room_id)
        if room_info is None:
            room_info = RoomInfo(room_id=room_id, members=members)
            session.add(room_info)
        else:
            room_info.members = members
        session.commit()
        logger.info(f"{room_info=}")
    else:  # type: chat message
        message = Message(**message)
        session.add(message)
        session.commit()

        # user = message.talkerName
        # msg = message.text
        # response_msg = f"已收到 用户:{user} 的消息: {msg}"
        # send_message_to_group(response_msg)
