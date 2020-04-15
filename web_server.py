"""
web server

提供一个服务端使用类,通过这个类可以快速的搭建一个web server服务,用以展示自己的简单网页
"""

from socket import *
from select import select
import re

#　主体功能　
class HTTPServer:
    def __init__(self,host='0.0.0.0',port=80,html=None):
        self.host = host
        self.port = port
        self.html = html
        # 多路服用列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        # 创建套接字和地址绑定工作
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setblocking(False)

    def bind(self):
        self.address = (self.host,self.port)
        self.sockfd.bind(self.address)

    # 启动服务 准备接受链接的过程
    def start(self):
        self.sockfd.listen(3)
        print("Listen the port %s"%self.port)
        # select TCP并发服务
        self.rlist.append(self.sockfd)
        while True:
            # 对IO进行监控
            rs,ws,xs = select(self.rlist, self.wlist, self.xlist)
            # 遍历列表分情况讨论
            for r in rs:
                if r is self.sockfd:
                    # 监听套接字就绪
                    c, addr = r.accept()
                    print("Connect from", addr)
                    # 添加客户端链接套接字作为监控对象
                    c.setblocking(False)
                    self.rlist.append(c)
                else:
                    # 客户端链接套接字就绪
                    self.handle(r)

    # 对每一个客户端请求的具体处理
    def handle(self,connfd):
        # 接受客户端请求 request --> http请求
        request = connfd.recv(1024).decode()
        # print(request) # 打印请求
        pattern = r"[A-Z]+\s+(/\S*)"
        try:
            # 获取请求内容
            info = re.match(pattern,request).group(1) # 只取子组内容
        except:
            # 客户端已经断开
            self.rlist.remove(connfd)
            connfd.close()
            return
        else:
            # 根据请求整理数据,发送给客户端
            self.get_html(connfd,info)

    # 网页处理
    def get_html(self,connfd,info):
        # info :  /     /xxxxx.html
        if info == '/':
            filename = self.html + '/index.html'
        else:
            filename = self.html + info

        # 打开网页
        try:
            f = open(filename,'rb')
        except:
            # 考虑请求的网页可能不存在
            response_headers = "HTTP/1.1 404 NOT FOUND\r\n"
            response_headers += "Content-Type:text/html\r\n"
            response_headers += "\r\n"
            response_content = "<h1>Sorry......</h1>"
            response = (response_headers + response_content).encode()
        else:
            # 请求的网页存在
            response_content = f.read()
            response_headers = "HTTP/1.1 200 OK\r\n"
            response_headers += "Content-Type:text/html\r\n"
            response_headers += "Content-Length:%d\r\n"%len(response_content)
            response_headers += "\r\n"
            response = response_headers.encode() + response_content
            f.close()
        finally:
            # 将http响应发送给浏览器
            connfd.send(response)


if __name__ == '__main__':
    """
    通过HTTPServer类快速搭建服务
    static中有一组网页,我为了展示我的这组网页
    """

    # 需要使用者提供 : 网络地址   网页位置
    host = "0.0.0.0"
    port = 8000
    dir = "./static"

    # 实例化对象
    httpd = HTTPServer(host=host,port=port,html=dir)

    # 调用方法启动服务
    httpd.start()

