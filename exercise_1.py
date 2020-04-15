"""
练习: 编写一个程序,将index.html这个网页通过浏览器访问并且展示
"""

from socket import *

# 处理浏览器请求
def request(connfd):
    # 接收http请求
    data = connfd.recv(1024)

    # 去出网页内容
    f = open("index.html")
    info = f.read() # 网页内容获取
    f.close()

    # 组织响应的格式
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:text/html\r\n"
    response += "\r\n"
    response += info

    connfd.send(response.encode()) # 发送给客户端
    connfd.close()


def main():
    sockfd = socket()
    sockfd.bind(('0.0.0.0',8000))
    sockfd.listen(3)

    while True:
        # 循环接收客户端请求
        connfd,addr = sockfd.accept()
        print("Connect from",addr)
        request(connfd) # 处理浏览器请求

if __name__ == '__main__':
    main()