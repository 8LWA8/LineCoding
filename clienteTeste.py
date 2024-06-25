import socket
  
cliente =  socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
cliente.connect(("0c:d2:92:95:53:a7", 4))#MAC do servidor e canal

try:
    while True:
        data = cliente.recv(1024)
        if not data:
            break
        print(data)
except OSError as e:
    pass

cliente.close()

