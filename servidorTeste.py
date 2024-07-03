import socket 

servidor =  socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
servidor.bind(("0c:d2:92:95:53:a7", 4))#MAC do servidor e canal
servidor.listen(1)#Quantidade de dispositivos que podem se comunicar no canal

cliente, addr = servidor.accept()#Aceitar conexao com o cliente

try:
    while True:
        print('AQUI')
        m = "Teste\n"
        cliente.send(m.encode('utf-7'))
except OSError as e:
    pass

cliente.close()
servidor.close()
