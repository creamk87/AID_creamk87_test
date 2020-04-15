"""
tcp 客户端
重点代码
"""

from socket import *

server_addr = ("127.0.0.1",8888)

# 创建tcp套接字  默认参数就是创建tcp套接字
tcp_socket = socket()

# 发起链接
tcp_socket.connect(server_addr)

# 发送接收消息
while True:
    msg = input(">>") # 输入##退出
    if not msg:
        break
    tcp_socket.send(msg.encode())
    data = tcp_socket.recv(20)
    print("从服务器收到:",data.decode())


tcp_socket.close()






