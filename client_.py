#!usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Ma Ping
import socket

client = socket.socket()           #声明socket类型并生成socket连接对象
client.connect(('0.0.0.0',9997))  #连接服务端
while True:
    msg = input('>>>:').strip()
    client.send(msg.encode('utf-8'))   #发送数据,python3只能发送bytes类型
    data = client.recv(1024).decode()            #接收数据，接收最大字节数为1024
    print('client reveive: ',data)    #打印接收到的数据
client.close()