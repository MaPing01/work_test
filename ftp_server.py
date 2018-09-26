import socket

class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()

    def connect( self ):
        self.client.connect(h)