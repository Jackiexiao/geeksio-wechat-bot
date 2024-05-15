# geeksio-wechat-bot
A reciver of geeksio wechat bot


对接仓库 https://github.com/chaovinci/geeksio 的接口

python >= 3.8, <=3.11

## Usage

1. 请查看 [Geeksio](https://github.com/chaovinci/geeksio) 查看如何连接微信机器人
2. 请查看 `Makefile` 知道如何使用此服务

## .env
```
ROOM_ID=R:123456
TOKEN=3xxxxxxxxxxxxxx
```

- TOKEN 可以给机器人发送 /token 获取你的个人 token
- ROOM_ID 以及 群聊的 hook 接口设置 目前需要找 Geeksio 的开发者单独配置

## Todo
- [ ] 接入 chatgpt 生成对话, 生成群聊精华
