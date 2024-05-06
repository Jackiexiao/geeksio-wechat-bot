
from fastapi import FastAPI, Request
from loguru import logger
from pydantic import BaseModel
import httpx

class WechatMessage(BaseModel):
    id: str
    timestamp: int
    type: int
    text: str
    filePath: str
    content: dict
    token:str

app = FastAPI(
    title="wechat bot msg handler",
    description="Wechat bot msg handler, https://github.com/Jackiexiao/geeksio-wechat-bot",
    version="1.0.0",
)

class WechatMessage(BaseModel):
    id: str
    timestamp: int
    type: int
    text: str
    filePath: str
    content: dict
    token:str

@app.post("/msg/")
async def update_msg(message: WechatMessage):
    logger.debug(message)

    # 构造新的消息
    new_message = {
        "text": f"I received a message: {message.text}",
        "token": message.token
    }

    # 使用httpx库异步发送新的消息到指定的URL
    async with httpx.AsyncClient() as client:
        response = await client.post("https://msg.io.sapling.pro", json=new_message)

    # 检查请求是否成功
    if response.status_code == 200:
        logger.debug("Message sent successfully.")
    else:
        logger.error(f"Failed to send message. Status code: {response.status_code}")

    return {"hello": "world"}