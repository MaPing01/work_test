import socketserver
import os
import json


'''
1. 创建一个请求处理的类，并且这个类要继承 BaseRequestHandlerclass ，并且还要重写父类里handle()方法；
2. 你必须实例化 TCPServer，并且传递server IP和你上面创建的请求处理类，给这个TCPServer；
3. server.handle_requese()#只处理一个请求，server.server_forever()处理多个一个请求，永远执行
4. 关闭连接server_close()
'''

class FtpHandler(socketserver.BaseRequestHandler):

    def cmd_put( self,*args ):
        msg_dict = args[0]
        filename = msg_dict['filename']
        filesize = msg_dict['filesize']
        if os.path.isfile(filename):
            f =open(filename+'.new','wb')
        else:
            f = open(filename,'wb')
        self.request.send(b'200 ok')
        receivesize = 0
        while receivesize < filesize:
            data = self.request.recv(1024)  #不能加strip()
            f.write(data)
            receivesize += len(data)
        else:
            print('file has uploaded')

    def cmd_get(self,*args):
        msg_dic = args[0]
        filename = msg_dic['filename']
        if os.path.isfile(filename):
            msg = os.stat(filename).st_size
            f = open (filename,'rb')
        else:
            msg = 400
        self.request.send(b'%d'%msg)
        self.request.recv(1024)
        for line in f:
            self.request.send(line)
        else:
            print(filename,'dowloaded success...')

    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            msg_dict = json.loads(self.data.decode('utf-8'))
            cmd = msg_dict['action']
            if hasattr(self,'cmd_%s'%cmd):
                func = getattr(self,'cmd_%s'%cmd)
                func(msg_dict)

if __name__ == '__main__':
    host,port = '0.0.0.0',9998
    server = socketserver.ThreadingTCPServer((host,port),FtpHandler)
    server.serve_forever()


