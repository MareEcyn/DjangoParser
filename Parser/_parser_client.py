import socket

# возвращает null если не достучался

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 80))
client_sock.sendall(b'httdfps://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7')
data = client_sock.recv(1024)
client_sock.close()
print('Recieved', data)