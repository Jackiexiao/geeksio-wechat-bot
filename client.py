import requests

url = "http://jackiexiao.com:8011/msg"
data = {"key": "value"}  # 随意的内容

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)