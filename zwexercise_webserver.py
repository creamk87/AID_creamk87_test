"""
  1. 主要功能 ：
     【1】 接收客户端（浏览器）请求
     【2】 解析客户端发送的请求
     【3】 根据请求组织数据内容
     【4】 将数据内容形成http响应格式返回给浏览器

  2. 特点 ：
     【1】 采用IO并发，可以满足多个客户端同时发起请求情况

     【2】 通过类接口形式进行功能封装

     【3】 做基本的请求解析，根据具体请求返回具体内容，同时处理客户端的非网页请求行为

  1. 功能分析

    实现 请求解析， 响应组织， 响应发送

  2. 技术分析

    网络：TCP套接字

    并发模型：IO多路复用  select 方法

    http协议请求响应格式

  3. 封装模型：类封装

    封装接口的设计： 1. 使用者需要什么功能

                  2. 有什么能够替使用者完成的

                  3. 有什么需要使用者提供的（需要使用者在使用我的类时，以某种形式传递给我）

  4. 协议设定：http协议

  5. 代码实现

  6. 细节处理
"""

from socket import *
from select import select
import re


# 主体功能
class HttpServer:
    # 自定义属性
    def __init__(self, host="0.0.0.0", port=80, html=None):
        self.host = host
        self.port = port
        self.html = html
        # 多路服用列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        # 创建套接字和地址绑定工作
        self.creat_socket()
        self.bind()

    # 创建套接字
    def creat_socket(self):
        self.sockfd = socket()
        self.sockfd.setblocking(False)

    # 绑定地址
    def bind(self):
        self.address = (self.host, self.port)
        self.sockfd.bind(self.address)

    # 启动方法
    def start(self):
        self.sockfd.listen(5)
        print("Listening the port %s" % self.port)
        # tcp并发服务
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for item in rs:
                if item is self.sockfd:
                    connfd, addr = item.accept()
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    self.handle(item)

    def response(self):
        pass

    # 对每个客户端具体的处理
    def handle(self, connfd):
        # 接受客户端请求 request --> http请求
        request = connfd.recv(1024).decode()
        pattern = r"[A-Z]+\s+(/\S*)"
        try:
            # 获取请求路径
            info = re.match(pattern, request).group(1)
        except:
            # 客户端已经断开
            self.rlist.remove(connfd)
            connfd.close()
            return
        else:
            self.get_html(connfd, info)

    def get_html(self, connfd, info):
        """
        根据请求，整理数据，发送给客户端
        :param connfd: 客户端连接套接字
        :param info: 请求路径
        :return: 发送数据
        """
        if info == "/":
            filename = self.html + "/index.html"
        else:
            filename = self.html + info

        try:
            f = open(filename, "rb")
        except:
            # 考虑访问的网页不存在
            response_headers = "HTTP/1.1 404 NOT FOUND\r\n"
            response_headers += "Content-Type:text/html\r\n"
            response_headers += "\r\n"
            response_content = "<h1>Sorry...</h1>"
            response = (response_headers + response_content).encode()
        else:
            data = f.read()
            response_content = data
            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type:text/html\r\n"
            response_headers += "Content-Length:%d\r\n" % len(response_content)
            response_headers += "\r\n"
            response = response_headers.encode() + response_content
        finally:
            connfd.send(response)


if __name__ == '__main__':
    """
    通过HttpServer类快速搭建服务
    展示static中的网页
    """

    # 需要使用者提供：网络地址  网页位置
    host = "0.0.0.0"
    port = 9527
    htmldir = "./day17/static"

    # 实例化对象
    httpd = HttpServer(host=host, port=port, html=htmldir)

    # 调用其方法启动服务
    httpd.start()
