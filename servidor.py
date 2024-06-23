import socket 

servidor =  socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
servidor.bind(("0c:d2:92:95:53:a7", 4))#MAC do servidor e canal
servidor.listen(1)#Quantidade de dispositivos que podem se comunicar no canal

cliente, addr = servidor.accept()#Aceitar conexao com o cliente

try:
    while True:
        if not data:
            break
        client.send('Teste')
except OSError as e:
    pass

cliente.close()
servidor.close()
