"""
select 并发模型处理IO
"""
import re
from socket import *
from select import select


class HttpServer:
    def __init__(self, host, port, htmlpath):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.html_path = htmlpath
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def start(self):
        self.create_socket()
        self.bind()
        self.rlist.append(self.sockfd)
        self.sockfd.listen(5)
        print("Listening the port ", self.port)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:
                    connfd, addr = self.sockfd.accept()  # 创建客户端连接套接字
                    print("Connect from", addr)
                    connfd.setblocking(False)   # 设置非阻塞IO
                    self.rlist.append(connfd)   # 加入监听
                else:
                    self.handle(r)

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setblocking(False)

    def bind(self):
        self.sockfd.bind(self.address)

    def handle(self, connfd):
        info = connfd.recv(2048).decode()
        # print(info)
        pattern = r"[A-Z]+\s+(/\S*)"
        try:
            path = re.match(pattern, info).group(1)
        except:
            self.rlist.remove(connfd)
            connfd.close()
        else:
            self.get_html(connfd, path)

    def get_html(self, connfd, path):
        if path == "/":
            file_name = self.html_path + "index.html"
        else:
            file_name = self.html_path + path
        try:
            file = open(file_name, "rb")
        except:
            response_header = "HTTP/1.1 404 NOT FOUND\r\n"
            response_header += "Content-Type:text/html\r\n"
            response_header += "\r\n"
            response_content = "Sorry......."
            response = response_header + response_content
            connfd.send(response.encode())
        else:
            response_content = file.read()
            response_header = "HTTP/1.1 200 OK\r\n"
            response_header += "Content-Type:text/html\r\n"
            response_header += "Content-Length:%d\r\n" % len(response_content)
            response_header += "\r\n"
            response = response_header.encode() + response_content
            connfd.send(response)


if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 9527
    PATH = "./day17/static"

    server = HttpServer(host=HOST, port=PORT, htmlpath=PATH)
    server.start()

