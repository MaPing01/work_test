import socket
import os
import json

class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()

    def connect( self,ip,port ):
        self.client.connect((ip,port))

    def interactive( self ):
        while True:
            cmd = input('>>>').strip()
            if len(cmd)==0:continue
            cmd_str = cmd.split()[0]
            if hasattr(self,'cmd_%s'%cmd_str):
                func = getattr(self,'cmd_%s'%cmd_str)
                func(cmd_str)


    def cmd_put( self,*args ):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    'filename':filename,
                    'filesize':filesize
                }
                self.client.send(json.dumps(msg_dic).encode('utf-8'))
                server_response = self.client.recv(1024)
                f = open(filename,'rb')
                for line in f:
                    self.client.send(line)
                else:
                    print(filename,'upload success...')
                    f.close()
            else:
                print(filename,'is not exist')


    def cmd_get( self ):
        pass


ftp = FtpClient()
ftp.connect('0.0.0.0',9999)
ftp.interactive()