#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: maping01

import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):  #所有请求的交互都是在handle里执行的,
        while True:
            try:
                self.data = self.request.recv(1024).strip()#每一个请求都会实例化MyTCPHandler(socketserver.BaseRequestHandler):
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                if self.data.decode("utf-8") == 'hi':
                    send_data = 'hello'
                self.request.sendall(send_data.encode("utf-8"))#sendall是重复调用send.
            except ConnectionResetError as e:
                print("err ",e)
                break

if __name__ == "__main__":
    # HOST, PORT = "localhost", 9999 #windows
    HOST, PORT = "0.0.0.0", 8900 #Linux
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)   #线程
    server.serve_forever()