import socket

client = socket.socket()
client.connect(('0.0.0.0',9997))
while True:
    data = input('>>>').strip()
    # print(data)
    client.send(data.encode('utf-8'))
    data = client.recv(1024)
    print('I received %s'%(data.decode()))
##