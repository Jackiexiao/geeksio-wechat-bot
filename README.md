# geeksio-wechat-bot
A reciver of geeksio wechat bot


对接仓库 https://github.com/chaovinci/geeksio 的接口

python >= 3.8, <=3.11

## Usage

1. 请查看 [Geeksio](https://github.com/chaovinci/geeksio) 查看如何连接微信机器人
2. 请查看 `Makefile` 知道如何使用此服务


比如这里的给机器人发 hook 地址
@hook http://150.158.107.114:8012/msg

获取群名单：post: https://msg.io.sapling.pro/  
 {
  "text": "",
  "type": 35,
  "roomId": "R:xxxxxxxxxxxxxx",
  "token": ""
}
发送群消息：post: https://msg.io.sapling.pro/  
 {
  "text": "something",
  "type": 7,
  "roomId": "R:xxxxxxxxxxxxxx",
  "token": ""
}