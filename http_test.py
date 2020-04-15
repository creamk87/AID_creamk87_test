"""
http请求响应演示
"""

from socket import *

# tcp服务端
s = socket()
s.bind(("0.0.0.0",8000))
s.listen(3)

c,addr = s.accept()
print("Connect from",addr)

data = c.recv(2048)  # 接收到来自浏览器的请求内容
print(data.decode())

# 组织为http响应的格式发送
http_data = """HTTP/1.1 200 OK
Content-Type:text/html

Hello World
"""

c.send(http_data.encode())  # 发送响应

c.close()
s.close()