import socketserver
import os
import json

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


