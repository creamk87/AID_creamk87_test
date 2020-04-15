from socket import *


def request(connfd):
    data = connfd.recv(2048)
    print(data.decode())
    # 读取前端页面文件
    f = open("./day17/index.html", "rb")
    file_data = f.read()
    f.close()

    # 组织相应格式
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type:text/html\r\n"
    response += "\r\n"
    response += file_data.decode()
    # 发送给客户端
    connfd.send(response.encode())


def main():
    s = socket()
    s.bind(("127.0.0.1", 9527))
    s.listen(2)
    while True:
        connfd, addr = s.accept()
        print("Connect from", addr)
        request(connfd)
    s.close()


if __name__ == '__main__':
    main()