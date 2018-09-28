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
                func(cmd)


    def cmd_put( self,*args ):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    'action':'put',
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


    def cmd_get( self ,*args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            msg_dic = {
                'action': 'get',
                'filename': filename
            }
            if os.path.isfile(filename):
                f = open(filename+'.get','wb')
            else:
                f = open(filename,'wb')
            self.client.send(json.dumps(msg_dic).encode('utf-8'))
            self.data = self.client.recv(1024)
            msg_dic = json.loads(self.data.decode('utf-8'))
            filesize = msg_dic['filesize']
            self.client.send(b'200 ok')
            receivesize = 0
            while receivesize < filesize:
                data = self.client.recv(1024)
                f.write(data)
                lenth = len(data)
                receivesize += lenth
            else:
                print(filename,'dowloaded sucess....')
                f.close()

ftp = FtpClient()
ftp.connect('0.0.0.0',9998)
ftp.interactive()