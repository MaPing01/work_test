#!usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Ma Ping
import socket

server = socket.socket()
server.bind(('0.0.0.0',9997))      #绑定要监听的端口
server.listen()                     #监听
while True:
    # conn 为客户端连过来，服务端生成的连接实例，addr为连接地址
    conn, addr = server.accept()  # 等待接收数据
    while True:
        data = conn.recv(1024)  # 接收数据
        print('server receive: ', data)
        conn.send(data.upper())  # 发送数据
server.close()


#http://idea.lanyus.com/