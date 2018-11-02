import socket

server = socket.socket()
server.bind(('0.0.0.0',9997))
server.listen(3)

while True:
    conn, address = server.accept()
    while True:
        data = conn.recv(1024)    # print(data)
        if not data:
            print('client has lost......')
            break
        conn.send(data.upper())
server.close()