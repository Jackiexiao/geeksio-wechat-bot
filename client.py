import requests
from src.models import WechatMessage

url = "http://jackiexiao.com:8012/msg"

data = {"key": "value"}  # 随意的内容

msg = WechatMessage(
    id="123",
    timestamp=123456789,
    type=7,
    text="Hello, world!",
    filePath="",
    talkerId="456",
    talkerName="Jackie",
    content={},
    token="123",
)

data = msg.model_dump()
print(data)
data["extra"] = "xxxx"


response = requests.post(url, json=data)

print(response.status_code)
print(response.text)
