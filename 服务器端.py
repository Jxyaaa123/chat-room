
from socket import socket,AF_INET,SOCK_STREAM#用于internet之间通信SOCK_STREAM#表示用的是TCP协议
#创建对象
server_socket=socket(AF_INET,SOCK_STREAM)
#绑定ip地址和接口
ip='127.0.0.1'#相当于local
port=8888
server_socket.bind((ip,port))
#开始监听
server_socket.listen(5)
print('服务器已经启动')
#等待客户端连接
clinent_socket,client_addr=server_socket.accept()#系列解包赋值
#接受数据
date=clinent_socket.recv(1024)
print('客户端发送过来的数据:',date.decode('utf-8'))
server_socket.close()